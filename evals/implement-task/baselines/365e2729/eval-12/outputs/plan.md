# Implementation Plan — TC-9210

**Summary:** Add severity-sorted remediation list to SBOM risk report
**Repository:** trustify-backend (Serena instance `serena_backend`)
**Target Branch:** `main`, branch to create: `TC-9210`
**Mode:** default flow (no Target PR, no Bookend Type)

## Step 0 – Project Configuration validation
The mock CLAUDE.md has a Repository Registry (trustify-backend / serena_backend / ./),
Jira Configuration (project key, Cloud ID, feature issue type ID, PR field
`customfield_10875`, GitHub Issue field `customfield_10747`), and Code Intelligence
(naming convention `mcp__<instance>__<tool>`). Result: PASS.

## Step 1 – Parsed task
All required sections are present: Repository, Target Branch, Description, Files to
Modify, Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements,
Dependencies. No Target PR, no Bookend Type. The GitHub Issue field would be read from the
issue. If it is empty, it is skipped.

## Steps 1.5–3 (would run, not executed in this eval)
- Fetch comments and check the `[sdlc-workflow] Description digest:` comment against
  `scripts/sha256-digest.py`.
- Dependencies: "None", so no checks are needed.
- Assign to the current user and transition to In Progress.

## Step 4 – Understand the code (planned Serena calls)
- `get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`.
- `find_symbol` with body on `SbomService` and its advisory-fetching method. Implementation
  Notes say to follow the existing pattern there.
- `find_symbol` with body on `SEVERITY_ORDER` in `advisory/service/advisory.rs`.
- `find_symbol` on `AdvisorySummary` (`advisory/model/summary.rs`) to confirm the
  `severity` field type (`String` or `Option<String>`) and the fields available for
  `title` / `fix_version`.
- `find_symbol` on `SbomDetails` (`sbom/model/details.rs`) to see how the details response
  is shaped.
- `find_referencing_symbols` on the get handler and on `SbomDetails` to check backward
  compatibility.
- Siblings for conventions: `advisory/service/advisory.rs`, `advisory/endpoints/get.rs`,
  `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Read `CONVENTIONS.md` at the repo root and pull out its CI check commands for Step 9.
- Docs to check later: `README.md`, `docs/api.md` (it documents GET /api/v2/sbom/{id}).

Expected conventions (from repo-backend.md):
- Errors: `Result<T, AppError>` with `.context()`.
- Module layout: `model/ + service/ + endpoints/`.
- Tests: integration tests against real Postgres, `assert_eq!(resp.status(), StatusCode::OK)`.

## Handling the SEVERITY_ORDER constant (symbol deduplication)

Full analysis is in `symbol-search.md`. Summary:

1. Search the whole `fundamental` crate, then the whole workspace, for `SEVERITY_ORDER`,
   `severity_order`, `SeverityOrder`, and the literal value
   `["critical","high","medium","low","none"]`.
2. Result: it is defined in `modules/fundamental/src/advisory/service/advisory.rs`, which
   is the **same crate** as the consumer.
3. **Decision: reuse it with `use crate::advisory::service::advisory::SEVERITY_ORDER;`.
   Do not redeclare it.**
4. If the constant (or its module path) is private, change it to `pub(crate)`. The same
   crate means no new dependency, so the "make it visible" option applies. That is a
   one-token change in `advisory.rs`, which is out of scope. It is flagged in Step 9 for
   user approval and explained in the commit/PR. A duplicate is never introduced, per
   AC #3.
5. How it is used: rank = position of the lowercased severity in `SEVERITY_ORDER`. Unknown
   or missing severities get `SEVERITY_ORDER.len()` and sort last.

## Step 5 – Branch
```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)
- Add the import `use crate::advisory::service::advisory::SEVERITY_ORDER;`.
- Add a documented struct, defined here so the change stays within Files to Modify:
  ```rust
  /// A single remediation entry derived from an advisory affecting an SBOM.
  #[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: String,
      pub title: String,
      pub fix_version: Option<String>,
  }
  ```
  The derive list mirrors sibling model structs (e.g. `utoipa::ToSchema` if siblings use
  it). Convention note: siblings would normally put DTOs in `sbom/model/`. Putting it in
  `model/` would add an out-of-scope file, so it stays in the service file unless the
  user approves a move.
- Add a private helper:
  ```rust
  /// Returns the sort rank for a severity string using the shared `SEVERITY_ORDER`;
  /// unknown or missing severities rank last.
  fn severity_rank(severity: &str) -> usize {
      let s = severity.to_ascii_lowercase();
      SEVERITY_ORDER.iter().position(|o| *o == s).unwrap_or(SEVERITY_ORDER.len())
  }
  ```
- Add a method on `SbomService`:
  ```rust
  /// Builds the list of remediations for an SBOM, sorted from most to least severe.
  /// Advisories with equal severity keep their original (fetch) order.
  pub async fn remediations(&self, sbom_id: Id, tx: &impl ConnectionTrait)
      -> Result<Vec<RemediationItem>, AppError>
  ```
  It reuses the existing advisory-fetching pattern in `SbomService` (via the
  `sbom_advisory` join), maps each advisory to `RemediationItem`, and then calls
  `items.sort_by_key(|i| severity_rank(&i.severity))`. `sort_by_key` is a **stable**
  sort, so items with the same severity keep their order (Test Requirement 3). It guards
  optional fields from the advisory entity defensively, for example
  `severity.unwrap_or_default()` and `fix_version` as an `Option`. Errors are wrapped with
  `.context("fetching advisories for SBOM remediation list")`.
- No new sorting logic is added to `common/src/db/query.rs`. The sort happens in memory
  on an already-fetched, small per-SBOM list, and the ordering is not a DB column.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)
- In the GET `/api/v2/sbom/{id}` handler, call `service.remediations(id, &tx).await?`
  after fetching the details.
- Include it in the response as a `remediations: Vec<RemediationItem>` field. Planned
  approach: the handler returns a response that adds `remediations` to the SBOM details.
  If `SbomDetails` (`sbom/model/details.rs`) must carry the field directly, that file is
  out of scope and is flagged in Step 9 for approval. Preferred option, if approved: add
  `#[serde(default)] pub remediations: Vec<RemediationItem>` to `SbomDetails`, which keeps
  the OpenAPI schema clean.
- Keep the `Result<_, AppError>` return type and existing caching middleware unchanged.
- Update the utoipa/OpenAPI annotations if the handler declares a response schema.

### 3. `tests/api/sbom_remediation.rs` (create)
Follows `tests/api/sbom.rs` conventions (test DB setup, `assert_eq!(resp.status(), StatusCode::OK)`).
Every test gets a `///` doc comment and Given/When/Then comments:
- `test_remediations_sorted_by_severity`: ingest an SBOM linked to advisories with
  severities none, low, critical, medium, high (shuffled). Assert the full vector of
  `(advisory_id, severity)` equals the expected critical→none order (value-based, not
  length-only), and assert all four fields of one item.
- `test_remediations_empty_when_no_advisories`: SBOM with no advisories. Assert
  `remediations == []` and status 200.
- `test_remediations_same_severity_stable_order`: three "high" advisories inserted in
  order A, B, C. Assert the ids come back exactly `[A, B, C]`.
- Parameterization: these three tests differ in setup and assertions (Meszaros
  heuristic), so they stay separate tests. `rstest` is only added if siblings already use
  it.
- A unit test for `severity_rank` (case-insensitivity, unknown → last) in a
  `#[cfg(test)] mod tests` inside `sbom.rs`, if sibling services have inline unit tests.
- Possible registration: if `tests/` uses a `main.rs`/`mod` list or `[[test]]` entries in
  `tests/Cargo.toml`, registering the new file there is out of scope. Flag it in Step 9.

### Documentation impact
`docs/api.md` describes GET `/api/v2/sbom/{id}`. The new `remediations` field should be
documented there. That file is out of scope, so it is flagged for user approval and not
edited silently.

## Step 7 – Tests
`cargo test -p fundamental` and the integration test crate
(`cargo test -p <tests crate> --test ...`). The crate name comes from
`cargo metadata --no-deps`.

## Step 8 – Acceptance criteria mapping
| AC | How satisfied |
|---|---|
| `remediations` field in GET /api/v2/sbom/{id} | get.rs handler change (and SbomDetails field if approved) |
| Sorted Critical > High > Medium > Low > None | `sort_by_key(severity_rank)` driven by `SEVERITY_ORDER`; test 1 |
| Uses existing `SEVERITY_ORDER`, no duplicate | `use crate::advisory::service::advisory::SEVERITY_ORDER`; Step 9 duplication grep confirms one definition |
| RemediationItem has advisory_id, severity, title, fix_version | struct definition; asserted in test 1 |

## Step 9 – Self-verification highlights
- **Scope containment.** Expected diff: `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`,
  `tests/api/sbom_remediation.rs`. Possible out-of-scope files that need explicit user
  approval:
  - `advisory/service/advisory.rs` (and/or `advisory/service/mod.rs`): `pub(crate)`
    visibility, only if the constant is currently private.
  - `sbom/model/details.rs`: `remediations` field on `SbomDetails`, if needed.
  - `tests/Cargo.toml` or a test module index: registering the new test file, if needed.
  - `docs/api.md`: response field documentation.
- **Duplication check.** Grep `(?i)severity_?order` and the literal array after
  implementation. Exactly one definition must exist, in `advisory.rs`.
- Run the CI commands from `CONVENTIONS.md` (e.g. fmt, clippy, check) and stop hard on
  any failure. Run `cargo test -p fundamental` and the tests crate.
- **Data flow.** HTTP GET → handler → `SbomService::remediations` → sbom_advisory join
  query → map to RemediationItem → stable sort by SEVERITY_ORDER rank → serialized
  `remediations` in JSON. Complete.
- **Contract and sibling parity.** Error handling and `.context()` usage match the other
  `SbomService` methods. The handler matches the other get handlers.

## Step 10 – Commit / PR (would run)
```
feat(sbom): add severity-sorted remediation list to SBOM details

Reuses SEVERITY_ORDER from advisory::service::advisory (same crate) instead of
redeclaring it; visibility widened to pub(crate) if it was private.

Implements TC-9210
```
With `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`. The PR goes to
`--base main` (fork detection first), and the description contains
`Implements [TC-9210](<webUrl>)`.

## Step 11 – Jira (would run)
Set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment covering the PR
link, a summary, and any approved out-of-scope deviations, with the implement-task
footnote. Transition to In Review.
