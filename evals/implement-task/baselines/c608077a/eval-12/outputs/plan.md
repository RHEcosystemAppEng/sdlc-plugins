# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

This is an eval dry run. No repository files were changed. Jira, git and Serena were not
called. Each step says what would happen.

## Step 0 – Project Configuration validation

The mock CLAUDE.md contains all three required sections:
- Repository Registry: `trustify-backend`, Serena `serena_backend`, path `./`
- Jira Configuration: project TC, Cloud ID, Feature type 10142, PR field
  `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<instance>__<tool>`, instance `serena_backend` (rust-analyzer)

All present, so the skill proceeds.

## Steps 1–3 – Task parsing, integrity, dependencies, Jira transition (simulated)

- Parsed sections: Repository (`trustify-backend`), Target Branch (`main`), Description,
  Files to Modify (2), Files to Create (1), Implementation Notes, Acceptance Criteria (4),
  Test Requirements (3), Dependencies (None).
- No Target PR and no Bookend Type, so the default flow applies.
- Step 1.5: would fetch comments, find the `[sdlc-workflow] Description digest:` comment and compare digests.
- Step 2: no dependencies to verify.
- Step 3: would assign the task to the current user and transition it to In Progress (not executed).
- GitHub Issue field (`customfield_10747`): would read it. If set, add `Closes <owner>/<repo>#<n>` to the PR body.

## Step 4 – Understand the code (planned Serena calls)

- `get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`.
- `find_symbol("SbomService", include_body=true)` to find the existing method that
  fetches related advisories (the Implementation Notes say to follow this pattern). It
  probably joins `sbom_advisory` to `advisory` and maps rows to `AdvisorySummary`.
- `find_symbol("AdvisorySummary")` in `advisory/model/summary.rs` to confirm the
  `severity` field type (most likely `Option<String>`) and the available id, title and
  fix-version fields.
- `find_symbol("SbomDetails")` in `sbom/model/details.rs` and
  `find_referencing_symbols` on it, to see how `get.rs` builds the response.
- **Symbol deduplication searches for `SEVERITY_ORDER` and `RemediationItem`.** Full
  details are in `symbol-search.md`.
- Sibling analysis: `advisory/service/advisory.rs`, `advisory/endpoints/get.rs`,
  `sbom/endpoints/list.rs`, `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Read `CONVENTIONS.md` at the repo root and extract the CI check commands (for example
  `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI
  generation command.
- Docs to check: `README.md`, `docs/api.md`. The `GET /api/v2/sbom/{id}` response shape
  changes, so `docs/api.md` may need a note.

### Conventions found (binding for Steps 6–7)
- Handlers return `Result<T, AppError>` and wrap errors with `.context()`.
- Each module uses the `model/ + service/ + endpoints/` layout. Services hold the DB logic and endpoints stay thin.
- Response structs derive `Serialize`, plus `utoipa::ToSchema` if siblings do.
- Tests in `tests/api/` run against a real PostgreSQL database and assert with `assert_eq!(resp.status(), StatusCode::OK)`.
- Skill rules take precedence: value-based assertions, a `///` doc comment on every test, and given/when/then comments.

## Step 5 – Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 – Changes per file

### Handling the `SEVERITY_ORDER` constant (key decision)

- **Reuse the existing constant. Never redeclare it.** It is defined in
  `modules/fundamental/src/advisory/service/advisory.rs` as
  `&["critical", "high", "medium", "low", "none"]`, which is in the same crate as the SBOM
  service. No new dependency is needed, so reuse is required.
- In `sbom/service/sbom.rs`:
  `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- If Serena shows the constant (or its parent module) is private, make the smallest change,
  `pub(crate)`. Because `advisory.rs` is **not** in Files to Modify, that one-line edit is
  flagged in Step 9's scope containment check and needs explicit user approval. It is not
  silently added to scope. If approval is refused, stop and ask. Do not fall back to a
  duplicate, because that breaks AC3.
- The sort key is the index of the severity in `SEVERITY_ORDER`, compared without regard
  to case. Missing or unknown severities sort last. This is done through a small private
  helper that only looks values up in the shared constant (see `symbol-search.md` §6).

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)

- Add the import `use crate::advisory::service::advisory::SEVERITY_ORDER;`.
- Add a new struct, unless the dedup search finds an existing one:
  ```rust
  /// One remediation entry for an SBOM: an affecting advisory and its fix version.
  #[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, ToSchema)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: Option<String>,
      pub title: Option<String>,
      pub fix_version: Option<String>,
  }
  ```
  Field types follow `AdvisorySummary`. The natural home would be `sbom/model/`, but that
  is outside the listed scope, so the struct goes in `sbom.rs`. Moving it to
  `sbom/model/details.rs` would be raised with the user during Step 9 and not done on my own.
- Add a private helper `fn severity_rank(severity: Option<&str>) -> usize`, which looks the value up in `SEVERITY_ORDER`.
- Add a method to `SbomService`, following the pattern of the existing advisory-fetching method:
  ```rust
  /// Builds the remediation list for an SBOM: its related advisories, sorted from
  /// most to least severe using `SEVERITY_ORDER`. Ties keep their original order.
  pub async fn fetch_remediations(&self, sbom_id: Id, tx: &impl ConnectionTrait)
      -> Result<Vec<RemediationItem>, AppError>
  ```
  - Reuse the existing related-advisory query (`sbom_advisory` join `advisory`). Do not write a new query.
  - Map each advisory to `RemediationItem`, with null guards on `severity`, `title` and
    `fix_version` (`.clone()` of `Option`, no unwraps).
  - Sort with `items.sort_by_key(|i| severity_rank(i.severity.as_deref()))`. `sort_by_key`
    is stable, which covers the "same severity keeps stable order" requirement. The input
    order comes from the existing query. If that query has no deterministic `ORDER BY`,
    order by advisory id first so ties are reproducible.
  - Return `Ok(vec![])` when there are no advisories.
  - Wrap errors with `.context("fetching remediations for SBOM")`, following the convention.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)

- After loading the SBOM details, call `service.fetch_remediations(id, &tx).await?` and add
  the result to the response as a `remediations` field (a JSON array that is always
  present and empty when there is nothing to report).
- Response shape: this needs a `remediations: Vec<RemediationItem>` field on the response.
  `SbomDetails` lives in `sbom/model/details.rs`, which is out of scope. Two options:
  (a) add the field to `SbomDetails`, which is a one-file scope expansion flagged for
  approval in Step 9, or (b) return a wrapper in `get.rs` that uses `#[serde(flatten)]` on
  `SbomDetails` and adds `remediations`. I would prefer (a) if the user approves, since it
  keeps the OpenAPI schema clean, and use (b) otherwise. Either way I would check whether
  the OpenAPI spec needs regenerating with the CONVENTIONS.md command.
- Keep returning `Result<_, AppError>` and keep the existing 404 handling unchanged.

### 3. `tests/api/sbom_remediation.rs` (create)

Follow the setup and fixtures of `tests/api/sbom.rs`. Each test gets a `///` doc comment and given/when/then comments.
- `test_remediations_sorted_by_severity`: ingest an SBOM with advisories rated low,
  critical, none, high and medium. GET `/api/v2/sbom/{id}`, assert `StatusCode::OK`, then
  assert the full ordered list of `(advisory_id, severity)` values equals
  critical, high, medium, low, none. This checks values, not just the count.
- `test_remediations_empty_when_no_advisories`: an SBOM with no advisories gives
  `remediations == []`, and the field is present.
- `test_remediations_same_severity_stable_order`: two or three "high" advisories plus one
  "critical". Assert critical comes first and the high advisories keep their input
  (query) order, compared by exact ids.
- Not parameterized: the three tests differ in setup and assertions (Meszaros heuristic).
- Registration: if `tests/Cargo.toml` or a test `main.rs`/`mod` list must declare the new
  file, flag that as out of scope in Step 9.

### Documentation impact

`GET /api/v2/sbom/{id}` gains a `remediations` field. `docs/api.md` would get a short
update, flagged for approval because it is outside the listed files.

## Step 7 – Tests

Run `cargo test -p <crate>` for `trustify-module-fundamental` and for the tests crate (the
package name comes from `cargo metadata`). Any non-zero exit is a hard stop.

## Step 8 – Acceptance criteria mapping

| AC | Covered by |
|---|---|
| `remediations` field in GET /api/v2/sbom/{id} | `get.rs` change plus the test asserting the field |
| Sorted Critical > High > Medium > Low > None | `severity_rank` over `SEVERITY_ORDER` with a stable sort, plus the sorting test |
| Uses the existing `SEVERITY_ORDER`, no duplicate | `use crate::advisory::service::advisory::SEVERITY_ORDER`, and the Step 9 grep shows one definition |
| RemediationItem has advisory_id, severity, title, fix_version | Struct in `sbom.rs` |

## Step 9 – Self-verification highlights

- Scope containment: the expected diff is `sbom.rs`, `get.rs` and `tests/api/sbom_remediation.rs`.
  Possible out-of-scope items, each needing user approval: `advisory/service/advisory.rs`
  (visibility only, if the constant is private), `sbom/model/details.rs` (response field),
  test registration, and `docs/api.md`.
- Duplication check: exactly one `SEVERITY_ORDER` definition, and no array literal
  `"critical", "high", ...` anywhere outside `advisory.rs`.
- Run the CONVENTIONS.md CI commands (fmt, clippy, test) and any OpenAPI generation. Any failure is a hard stop.
- Data flow: GET request, then `get.rs`, then `SbomService::fetch_remediations`, then the
  `sbom_advisory`/`advisory` query, then mapping to `RemediationItem`, then the
  severity sort, then JSON serialization. Every stage is connected.
- Parity: the new method matches the sibling advisory-fetch methods (connection param,
  `.context()`), and the endpoint matches existing handlers in how it calls the service.

## Steps 10–11 – Commit, PR, Jira (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Reuses SEVERITY_ORDER from advisory::service::advisory (same crate)
instead of redeclaring it.

Implements TC-9210"
```
- `gh pr create --base main` (adding `-R`/`--head` if an upstream remote exists). The PR
  body includes `Implements [TC-9210](<webUrl>)` and the reuse rationale.
- Set `customfield_10875` to the PR URL as ADF, add a Jira comment with the skill footnote,
  and transition the task to In Review.
