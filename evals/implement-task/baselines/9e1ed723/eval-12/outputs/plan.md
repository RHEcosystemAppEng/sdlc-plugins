# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

## Step 0 — Project Configuration validation

`claude-md-mock.md` contains Repository Registry (trustify-backend, Serena `serena_backend`,
path `./`), Jira Configuration (project key TC, Cloud ID, Feature issue type ID 10142), and
Code Intelligence (naming convention `mcp__<instance>__<tool>`). Validation passes.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none — default flow |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/get.rs` |
| Files to Create | `tests/api/sbom_remediation.rs` |
| Dependencies | None |
| GitHub Issue (customfield_10747) | read from issue if present -> `Closes owner/repo#N` in PR body |

All required sections present. (Steps 1.5–3 — digest check, dependency check, assign +
transition to In Progress — would be performed against Jira; skipped in this eval.)

## Step 4 — Code understanding (planned Serena calls on `serena_backend`)

- `get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/get.rs`.
- `find_symbol("SbomService", include_body=true)` — locate the existing advisory-fetching
  method (Implementation Notes: "follow the existing pattern ... for fetching related advisories").
- `find_symbol("SbomDetails")` in `sbom/model/details.rs` and
  `find_symbol("AdvisorySummary")` in `advisory/model/summary.rs` — confirm `severity`
  field type (`String` vs `Option<String>`) and title/fix-version availability.
- `find_referencing_symbols` on the get handler and on any `SbomService` method touched,
  to preserve backward compatibility.
- Symbol dedup for `SEVERITY_ORDER` — see `symbol-search.md`.
- Siblings for conventions: `advisory/service/advisory.rs`, `sbom/endpoints/list.rs`,
  `advisory/endpoints/get.rs`; tests: `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Read `CONVENTIONS.md` at repo root; extract CI check commands (e.g. `cargo fmt --check`,
  `cargo clippy -- -D warnings`) and any codegen commands (OpenAPI generation).
- Docs to track: `README.md`, `docs/api.md` (REST API reference — `GET /api/v2/sbom/{id}`
  response shape changes).

Expected conventions (binding): handlers return `Result<T, AppError>` with `.context()`;
`model/ + service/ + endpoints/` layout; SeaORM queries via `common/src/db/query.rs`;
tests assert `assert_eq!(resp.status(), StatusCode::OK)`; serde-derived response structs.

## SEVERITY_ORDER handling (key decision)

**Reuse, do not redeclare.** The constant already exists in the same crate at
`modules/fundamental/src/advisory/service/advisory.rs`:

```rust
SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]
```

- In `sbom.rs`: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- No new constant, enum, match table, or map is introduced anywhere.
- Sort key = index of the (lower-cased) severity in `SEVERITY_ORDER`; unknown severities map
  to `SEVERITY_ORDER.len()` so they sort after `"none"` rather than panicking.
- Use `sort_by_key` (stable sort) so equal-severity advisories keep their fetch order
  (satisfies the stable-ordering test requirement).
- Same crate => no Cargo dependency change; the "Reuse over duplication" rule clearly favors
  importing.
- **If the constant is private**: change it to `pub(crate) const` (and ensure the
  `service::advisory` module is `pub(crate)`-reachable). This edits `advisory.rs`, which is
  outside Files to Modify, so it is flagged for explicit user approval in Step 9 scope
  containment — never resolved by copying the constant. Rationale noted in the commit body
  and PR description.

## Step 5 — Branch

```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (modify)

- Add import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- Add struct (with doc comment, serde + utoipa derives matching sibling model structs):

  ```rust
  /// A single remediation entry derived from an advisory affecting an SBOM.
  #[derive(Clone, Debug, Serialize, Deserialize, ToSchema, PartialEq, Eq)]
  pub struct RemediationItem {
      pub advisory_id: String,
      pub severity: String,
      pub title: String,
      pub fix_version: Option<String>,
  }
  ```
  (Placed here because `sbom/model/` is out of scope; if the user prefers it in
  `sbom/model/details.rs`, that would be an approved scope extension.)

- Add a private helper:

  ```rust
  /// Returns the sort rank of a severity per `SEVERITY_ORDER` (0 = most severe);
  /// unknown values rank last.
  fn severity_rank(severity: &str) -> usize {
      let s = severity.to_ascii_lowercase();
      SEVERITY_ORDER.iter().position(|o| *o == s).unwrap_or(SEVERITY_ORDER.len())
  }
  ```

- Add method on `SbomService`, following the existing related-advisory fetch pattern
  (join through `entity::sbom_advisory`):

  ```rust
  /// Builds the remediation list for an SBOM, sorted by descending severity
  /// (critical first, none last). Equal severities keep their original order.
  pub async fn remediations(&self, sbom_id: Uuid, tx: &impl ConnectionTrait)
      -> Result<Vec<RemediationItem>, AppError>
  ```
  - Fetch related advisories (reuse existing fetch helper rather than writing a new query).
  - Map each to `RemediationItem` with defensive access: `severity.unwrap_or_default()` /
    `"none"` when absent, `fix_version` stays `Option`, title `unwrap_or_default()`.
  - `items.sort_by_key(|i| severity_rank(&i.severity));`
  - Errors wrapped with `.context("fetching advisories for SBOM remediation list")`.

### 2. `modules/fundamental/src/sbom/endpoints/get.rs` (modify)

- In the `GET /api/v2/sbom/{id}` handler, after fetching details, call
  `service.remediations(id, &tx).await?` and include it in the response as a
  `remediations: Vec<RemediationItem>` field (always present; empty vec when no advisories).
- Update the `#[utoipa::path]` response annotation so the OpenAPI spec reflects the new field.
- Note: if the response type is `SbomDetails` (in `sbom/model/details.rs`, out of scope),
  adding the field there requires user approval in Step 9. Preferred alternative that stays
  in scope: if the handler already builds a response wrapper locally, add the field there.
  Decided after Step 4 inspection; flagged either way.

### 3. `tests/api/sbom_remediation.rs` (create)

Following `tests/api/sbom.rs` setup (real PostgreSQL test DB, ingest fixtures, HTTP call):

- `/// Verifies remediations are sorted critical first and none last.`
  `test_remediations_sorted_by_severity` — ingest SBOM linked to advisories of severities
  low, critical, none, high, medium; assert status OK and assert the exact `severity`
  sequence `["critical","high","medium","low","none"]` plus advisory_ids (value-based,
  not just length). Given/When/Then comments.
- `/// Verifies an SBOM with no advisories returns an empty remediations list.`
  `test_remediations_empty_for_sbom_without_advisories` — assert `remediations == []`
  (field present, not missing).
- `/// Verifies advisories with equal severity keep stable relative order.`
  `test_remediations_stable_for_equal_severity` — two "high" advisories A, B plus one
  "critical"; assert ids exactly `[C, A, B]`.
- Cases differ in setup/assertions, so separate tests rather than parameterized (Meszaros).
- Register the test module if `tests/` uses an explicit `mod` list / `[[test]]` entry in
  `tests/Cargo.toml` — flagged as out-of-scope if required.

### Documentation impact

`docs/api.md` documents `GET /api/v2/sbom/{id}`; the new `remediations` field should be
documented there. Out of Files to Modify — flag to user for approval. Regenerate OpenAPI
spec if CONVENTIONS.md lists a generation command, and commit the result.

## Step 7–8 — Tests and acceptance criteria

- `cargo test -p trustify-module-fundamental` and the tests crate (`cargo test -p <tests crate>`
  resolved via `cargo metadata`).
- AC mapping:
  - `remediations` field in GET response -> get.rs change + test 1/2
  - Critical > High > Medium > Low > None -> `severity_rank` + test 1
  - Uses existing `SEVERITY_ORDER`, no duplicate -> import only; verified by
    workspace grep showing a single definition
  - RemediationItem fields advisory_id, severity, title, fix_version -> struct above

## Step 9 — Self-verification

- Scope containment: expected diff = 2 modified + 1 created. Potential out-of-scope items
  requiring user approval: `advisory/service/advisory.rs` (visibility only, if private),
  `sbom/model/details.rs` (if response struct lives there), `docs/api.md`,
  test registration file.
- Duplication check: grep `(?i)severity_?order` and `"critical",\s*"high"` across the
  workspace — exactly one definition.
- CI checks from CONVENTIONS.md (hard stop on any failure); Rust module-level tests per crate.
- Data-flow trace: DB (`sbom_advisory` join) -> `SbomService::remediations` (map + sort by
  `SEVERITY_ORDER`) -> get handler -> JSON `remediations` field.
- Contract/sibling parity: error handling via `AppError` + `.context()`, same tx/connection
  pattern as other `SbomService` methods; serde/ToSchema derives match sibling models.

## Step 10–11 — Commit, PR, Jira

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Reuses SEVERITY_ORDER from the advisory module (same crate) instead of
redeclaring it.

Implements TC-9210"
```

- `gh pr create --base main` (or fork form if `upstream` remote exists); body includes
  `Implements [TC-9210](<webUrl>)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue
  field is set; PR notes the SEVERITY_ORDER reuse decision.
- Jira: set `customfield_10875` (ADF inlineCard with PR URL), add comment (PR link, summary,
  deviations, implement-task footnote), transition to In Review.
