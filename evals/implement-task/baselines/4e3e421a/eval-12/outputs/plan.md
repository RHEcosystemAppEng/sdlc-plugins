# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

Simulated run. No Jira, git, or Serena calls were made. The steps below describe what the
implement-task skill would do.

## Step 0 — Project Configuration check
`claude-md-mock.md` has all three required sections:
- Repository Registry: `trustify-backend` → Serena `serena_backend`, path `./`
- Jira Configuration: project key, cloud ID, and feature type ID are present. PR field is
  `customfield_10875`, GitHub Issue field is `customfield_10747`.
- Code Intelligence: naming convention is `mcp__serena_backend__<tool>`. Limitation: rust-analyzer
  needs 30-60s to index.

Result: pass, proceed.

## Step 1 — Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs` |
| Files to Create | `tests/api/sbom_remediation.rs` |
| Target PR / Bookend | none, so the default flow applies |
| Dependencies | none |
| GitHub Issue (customfield_10747) | would be read from the issue. Not present in the mock, so skipped |

All required sections are present, so no clarification is needed.

## Steps 1.5 / 2 / 3 — simulated
- Digest check: would fetch comments and look for `[sdlc-workflow] Description digest:`.
- Dependencies: none.
- Would assign TC-9210 to the current user and move it to In Progress.

## Step 4 — Understand the code (planned Serena calls)
- `get_symbols_overview` on `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`, `sbom/model/details.rs`.
- `find_symbol("SbomService", depth=1)`, then read the existing advisory-fetch method body. The
  Implementation Notes say to follow "the existing pattern for fetching related advisories"
  (probably a join through `entity::sbom_advisory`).
- `find_symbol("SEVERITY_ORDER", include_body=true)` in `advisory/service/advisory.rs`, then
  `find_referencing_symbols` on it. Details are in `symbol-search.md`.
- `find_symbol("AdvisorySummary")` in `advisory/model/summary.rs` to confirm the type of the
  `severity` field (`String` vs `Option<String>`).
- Sibling conventions: `advisory/endpoints/get.rs` and `sbom/endpoints/list.rs` for handler
  shape, `tests/api/sbom.rs` and `tests/api/advisory.rs` for test patterns.
- Read `CONVENTIONS.md` at the repo root and extract the CI check commands (likely
  `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI generation command.
- Docs to check for impact: `docs/api.md` (REST API reference), `README.md`.

Expected conventions: handlers return `Result<T, AppError>` with `.context()`. Services are
`impl SbomService { async fn ...(&self, ..., db) }`. Tests use
`assert_eq!(resp.status(), StatusCode::OK)` against a real Postgres test DB.

## Handling the SEVERITY_ORDER constant (key decision)

**Reuse the existing constant. Do not redeclare it.**

- It is defined in `modules/fundamental/src/advisory/service/advisory.rs` as
  `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]`.
- `sbom` and `advisory` are in the same crate (`fundamental`), so no new dependency is needed.
- In `sbom/service/sbom.rs`:
  ```rust
  use crate::advisory::service::advisory::SEVERITY_ORDER;
  ```
- If the constant is private, widen it to `pub(crate) const SEVERITY_ORDER`. This is a one-word
  visibility change. If `advisory/service/mod.rs` declares a private `mod advisory;`, that needs
  a `pub(crate)` too.
  - `advisory.rs` and `advisory/service/mod.rs` are **not** in Files to Modify. I would flag them
    in Step 9 scope containment and get user approval before committing. The visibility change
    is the only way to meet acceptance criterion 3 ("no duplicate definition") if the constant
    is private. Copying it is not an option.
- Sort key: the constant's index. Matching is case-insensitive, and unknown or missing severities
  sort after `"none"`:
  ```rust
  /// Returns the sort rank of a severity string based on `SEVERITY_ORDER`
  /// (0 = critical). Unknown or missing severities rank after all known values.
  fn severity_rank(severity: Option<&str>) -> usize {
      severity
          .and_then(|s| {
              let s = s.to_ascii_lowercase();
              SEVERITY_ORDER.iter().position(|o| *o == s)
          })
          .unwrap_or(SEVERITY_ORDER.len())
  }
  ```
  If `advisory.rs` already has an equivalent helper, reuse it instead of adding this one.
- Sorting uses `Vec::sort_by_key(|r| severity_rank(r.severity.as_deref()))`. Rust's `sort_by_key`
  is stable, which meets the "same severity keeps stable ordering" requirement. The input order
  comes from the existing advisory-fetch query, so I would check that the query has a
  deterministic `ORDER BY` (for example by advisory id) to make ties reproducible. If it does
  not, I would add a secondary `order_by` on the remediation query only.

## Step 5 — Branch
```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)
- Add `use crate::advisory::service::advisory::SEVERITY_ORDER;`.
- Add a new struct, with a doc comment:
  ```rust
  /// A single remediation entry for an SBOM: one related advisory with its severity and fix version.
  #[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: Option<String>,
      pub title: Option<String>,
      pub fix_version: Option<String>,
  }
  ```
  The field types follow `AdvisorySummary`/the entity. Use `ToSchema` only if siblings derive it.
- Add the private helper `severity_rank` shown above.
- Add a method on `SbomService`:
  ```rust
  /// Builds the list of remediations for an SBOM, sorted by descending severity
  /// (critical first, none/unknown last). Ties keep the query order.
  pub async fn remediations(&self, sbom_id: Uuid, tx: &impl ConnectionTrait)
      -> Result<Vec<RemediationItem>, Error>
  ```
  Implementation: reuse the existing related-advisories fetch pattern (the
  `sbom_advisory` join), map each row to `RemediationItem`, using `.unwrap_or_default()` or
  `Option` for nullable columns (defensive access across the entity boundary), then call
  `sort_by_key(severity_rank)`. Errors are wrapped with `.context("fetching remediations for SBOM")`
  to match conventions.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)
- In the `GET /api/v2/sbom/{id}` handler, after fetching the SBOM details, call
  `service.remediations(id, &tx).await.context(...)?` and include the result in the response as
  `remediations: Vec<RemediationItem>`. An empty `Vec` is serialized as `[]`, never omitted.
- Update the handler's `#[utoipa::path]` response annotation if it exists.
- **Scope note:** the response body is `SbomDetails` in `sbom/model/details.rs`, which is not
  in Files to Modify. There are two options:
  (a) add `#[serde(default)] pub remediations: Vec<RemediationItem>` to `SbomDetails`. This is
  the cleanest and matches the module pattern, but it needs scope approval in Step 9.
  (b) wrap the response in get.rs with `#[serde(flatten)] details: SbomDetails` plus
  `remediations`, which stays within scope.
  I would prefer (a), flag `details.rs` for user approval, and fall back to (b) if the user
  declines. If an OpenAPI generation command is listed in CONVENTIONS.md, I would run it and
  commit the regenerated spec.

### 3. `tests/api/sbom_remediation.rs` (create)
This follows the patterns in `tests/api/sbom.rs` (test DB setup, ingest fixtures, HTTP calls,
`assert_eq!(resp.status(), StatusCode::OK)`). Every test gets a `///` doc comment and
Given/When/Then comments. The assertions check values, not just lengths.
- `/// Verifies remediations are sorted critical → high → medium → low → none.`
  `test_remediations_sorted_by_severity`: ingest an SBOM linked to advisories with severities
  in shuffled order, then assert `remediations.iter().map(|r| r.severity)` equals
  `["critical","high","medium","low","none"]`, and also assert on the `advisory_id` order.
- `/// Verifies an SBOM with no advisories returns an empty remediations list.`
  `test_remediations_empty_when_no_advisories`: assert status 200 and that `remediations` is
  present and equals `[]`.
- `/// Verifies advisories sharing a severity keep a stable relative order.`
  `test_remediations_stable_for_equal_severity`: several `high` advisories, then assert the
  exact `advisory_id` sequence matches the query order, and that it is the same across two requests.

The three tests have different setups and assertions, so they stay as separate functions
(Meszaros heuristic), not a parameterized test.
- Registration: if `tests/Cargo.toml` uses explicit `[[test]]` entries or a `tests/api/main.rs`
  `mod` list, the new file has to be registered there. That file is out of scope, so I would
  flag it in Step 9.

## Steps 7–9 — Verification
- `cargo test -p <fundamental crate name from cargo metadata>` and the tests crate, with a hard
  stop on failure.
- Run the CONVENTIONS.md CI commands (fmt, clippy, etc.), with a hard stop on any non-zero exit.
- Acceptance criteria:
  1. `remediations` field in GET /api/v2/sbom/{id}: get.rs change and tests.
  2. Sorted Critical > ... > None: `severity_rank` and test 1.
  3. Uses the existing `SEVERITY_ORDER`: single `use` import. A duplication grep confirms one declaration.
  4. `RemediationItem` has `advisory_id`, `severity`, `title`, `fix_version`.
- Scope containment: the expected diff is the 3 listed files, plus these flagged for approval:
  `advisory/service/advisory.rs` (visibility, only if private), `advisory/service/mod.rs`
  (only if needed), `sbom/model/details.rs` (option a), and test registration (only if needed).
- Data flow: GET request → handler → `SbomService::remediations` → DB join of sbom_advisory and
  advisory → map → sort → serialized `remediations` field. All stages connect.
- Query scope: filtered by `sbom_id`, not a full table scan.
- Sibling parity: same error-wrapping and transaction pattern as the existing advisory fetch.
- Docs: update `docs/api.md` with the new `remediations` field if it documents the SBOM details
  response. That file is out of scope, so I would flag it.

## Steps 10–11 — Commit and Jira (simulated)
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Reuses SEVERITY_ORDER from advisory::service::advisory (same crate) instead of
redeclaring it; visibility widened to pub(crate) if it was private.

Implements TC-9210"
```
- `gh pr create --base main`, with a fork-aware `-R`/`--head` if an `upstream` remote exists.
  The PR body includes `Implements [TC-9210](<webUrl>)` and a `Closes owner/repo#N` line if the
  GitHub Issue field is set.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment with the PR
  link, summary, and deviations (any approved out-of-scope visibility or model change) plus the
  skill footnote, then move the issue to In Review.
