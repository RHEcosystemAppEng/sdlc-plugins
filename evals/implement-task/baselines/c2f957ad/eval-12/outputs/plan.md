# Implementation Plan — TC-9210

**Summary:** Add severity-sorted remediation list to SBOM risk report
**Repository:** trustify-backend (Serena instance `serena_backend`, path `./`)
**Target Branch:** `main`
**Branch to create:** `TC-9210`

## Step 0 — Project Configuration validation

`claude-md-mock.md` contains all required sections: Repository Registry (trustify-backend /
serena_backend), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142),
and Code Intelligence (naming convention `mcp__<instance>__<tool>`). Validation passes.

## Steps 1–3 — Jira (simulated, no external calls)

- Step 1: Task parsed. All required sections present: Repository, Target Branch (`main`),
  Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria,
  Test Requirements, Dependencies. No Target PR, no Bookend Type -> default flow. GitHub
  Issue field (customfield_10747) would be read; skip if empty.
- Step 1.5: Would fetch comments and verify `[sdlc-workflow] Description digest:`; warn and
  continue if absent.
- Step 2: Dependencies = None — nothing to verify.
- Step 3: Would assign to current user and transition to In Progress.

## Step 4 — Understand the code (what I would inspect)

- `get_symbols_overview` on `sbom/service/sbom.rs`, `sbom/endpoints/get.rs`,
  `advisory/service/advisory.rs`, `sbom/model/details.rs`.
- `find_symbol(include_body=true)` on `SbomService` advisory-fetching method (pattern the
  task tells us to follow), the `get` handler, `SbomDetails`, and `SEVERITY_ORDER`.
- `find_referencing_symbols` on the `get` handler and `SbomDetails` to check backward
  compatibility (adding a field to a serialized response is additive/non-breaking).
- Read `CONVENTIONS.md` at repo root; extract CI check commands (fmt/clippy/check/test)
  and any OpenAPI generation command for Step 9.
- Sibling conventions: `advisory/service/advisory.rs`, `sbom/endpoints/list.rs`,
  `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Docs: `README.md`, `docs/api.md` (REST API reference — documents GET /api/v2/sbom/{id}).

### Expected conventions (binding during implementation)

- Handlers return `Result<T, AppError>` with `.context()` wrapping.
- Module layout `model/ + service/ + endpoints/`.
- Service methods take `&self` + DB connection/transaction, return `Result<_, Error>`.
- Tests: integration tests in `tests/api/` against real PostgreSQL;
  `assert_eq!(resp.status(), StatusCode::OK)`; value-based assertions on bodies.

## SEVERITY_ORDER handling (key decision)

Full analysis in `symbol-search.md`. Summary:

- **Do not redeclare `SEVERITY_ORDER`.** It already exists in
  `modules/fundamental/src/advisory/service/advisory.rs` as
  `&["critical", "high", "medium", "low", "none"]`.
- Source and target are in the **same crate** (`modules/fundamental`), so no Cargo
  dependency is needed — reuse is the correct choice per "Reuse over duplication".
- Import in `sbom.rs`:
  `use crate::advisory::service::advisory::SEVERITY_ORDER;`
- If the constant is private, change `const` to `pub(crate) const` (minimal visibility).
  Because `advisory.rs` is not in Files to Modify, this one-line visibility change would
  be **flagged for user approval** in Step 9 scope containment before committing. If it is
  already `pub`/`pub(crate)`, no change outside scope is needed.
- Sort key: the index of the advisory's lowercased severity in `SEVERITY_ORDER`; unknown or
  missing severities map to `SEVERITY_ORDER.len()` (sorted last, after "none").
- Use `slice::sort_by_key` (stable sort) so advisories with equal severity keep their
  original fetch order — satisfies the stable-ordering test requirement.

## Step 5 — Branch

```
git checkout main && git pull && git checkout -b TC-9210
```

## Step 6 — Changes per file

### Modify: `modules/fundamental/src/sbom/service/sbom.rs`

1. Add import: `use crate::advisory::service::advisory::SEVERITY_ORDER;`
2. Add `RemediationItem` struct (doc-commented), unless the user prefers it in
   `sbom/model/` (see "Scope questions" below):
   ```rust
   /// A single remediation entry for an SBOM, derived from an affecting advisory.
   #[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
   pub struct RemediationItem {
       pub advisory_id: String,
       pub severity: String,
       pub title: String,
       pub fix_version: Option<String>,
   }
   ```
   (Field types finalized against `AdvisorySummary`; `fix_version` is `Option` since not
   every advisory has a fix.)
3. Add a private helper (doc-commented):
   ```rust
   /// Returns the sort rank of a severity string using `SEVERITY_ORDER`
   /// (0 = critical); unknown severities rank after "none".
   fn severity_rank(severity: &str) -> usize {
       let s = severity.to_ascii_lowercase();
       SEVERITY_ORDER.iter().position(|o| *o == s).unwrap_or(SEVERITY_ORDER.len())
   }
   ```
4. Add `SbomService::remediations(&self, sbom_id, tx) -> Result<Vec<RemediationItem>, Error>`
   (doc-commented), following the existing advisory-fetching pattern in `SbomService`
   (query via `sbom_advisory` join -> `advisory` entity). Map each advisory to
   `RemediationItem`, using defensive access for nullable fields (`severity` defaults to
   `""` -> ranks last; `fix_version` stays `None`; `title` `unwrap_or_default()`).
   Then `items.sort_by_key(|i| severity_rank(&i.severity));` (stable). Empty advisory set
   -> returns `Ok(vec![])`.

### Modify: `modules/fundamental/src/sbom/endpoints/get.rs`

- In the GET `/api/v2/sbom/{id}` handler, after fetching details, call
  `service.remediations(id, &tx).await.context("fetching remediations")?` and include it in
  the response under a `remediations` field (always present; empty array when none).
- Keep `Result<_, AppError>` + `.context()` pattern; update the `utoipa` response
  annotation so the OpenAPI spec reflects the new field.

### Create: `tests/api/sbom_remediation.rs`

Each test has a `///` doc comment and Given/When/Then comments; value-based assertions.

1. `test_remediations_sorted_by_severity` — SBOM linked to advisories with severities
   low, critical, none, high, medium (inserted out of order). Assert status OK and that
   `remediations` severities equal exactly
   `["critical", "high", "medium", "low", "none"]`, plus advisory_id of first/last item.
2. `test_remediations_empty_when_no_advisories` — SBOM with no advisories; assert
   `remediations == []` (field present, not missing).
3. `test_remediations_stable_for_equal_severity` — three "high" advisories inserted A, B, C
   plus one "critical"; assert ordering is `[critical, A, B, C]` by advisory_id.

Tests 1 and 3 differ in setup and assertion structure, so they stay separate (no
parameterization), matching sibling `tests/api/sbom.rs` style.

Integration: register the new test file the way siblings are wired (check `tests/Cargo.toml`
`[[test]]` entries or a `tests/api/main.rs`/`mod.rs`). If registration requires editing a
file not in scope, flag it for approval in Step 9.

### Documentation impact

`docs/api.md` documents GET /api/v2/sbom/{id}; the response gains a `remediations` field.
Not listed in scope -> flag to user in Step 9 as a recommended doc update rather than
editing silently. Regenerate OpenAPI spec if CONVENTIONS.md lists a generation command.

## Scope questions to raise with the user (Step 4/9)

1. `advisory/service/advisory.rs` — `pub(crate)` visibility on `SEVERITY_ORDER` if it is
   currently private (needed to satisfy AC #3 without duplication).
2. `sbom/model/details.rs` — the module convention places response structs in `model/`.
   If `SbomDetails` is the body returned by `get.rs`, adding `remediations: Vec<RemediationItem>`
   there (and placing `RemediationItem` in `sbom/model/`) is the conventional design but is
   out of scope. Fallback within scope: define `RemediationItem` in `service/sbom.rs` and
   wrap/flatten the response in `get.rs` (`#[serde(flatten)]` details + `remediations`).
   Ask user which they prefer.
3. Test registration file and `docs/api.md`, if needed.

## Steps 7–9 — Verification

- Run `cargo test -p <fundamental crate name from cargo metadata>` and the tests crate
  (`cargo test -p <tests crate> sbom_remediation`).
- Run all CI commands from `CONVENTIONS.md` (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`,
  `cargo check`); hard stop on any failure.
- AC check:
  - [x] `remediations` field in GET /api/v2/sbom/{id} response — get.rs change
  - [x] Sorted Critical > High > Medium > Low > None — `severity_rank` + stable sort
  - [x] Uses existing `SEVERITY_ORDER`, no duplicate — import from advisory module;
        verify with `grep -rn "SEVERITY_ORDER\s*:" modules/` showing exactly one definition
  - [x] `RemediationItem` has advisory_id, severity, title, fix_version
- Scope containment: `git diff --name-only` should show only the 3 in-scope files plus any
  user-approved items above.
- Duplication check: confirm no second severity-ordering array or rank helper was introduced.
- Data-flow trace: DB (`sbom_advisory` join -> `advisory`) -> `SbomService::remediations`
  (map + sort) -> `get.rs` handler -> JSON `remediations` field. Complete.
- Contract/sibling parity: new service method matches sibling error handling and tx
  parameter pattern; caller in `get.rs` uses `.context()` like other service calls.

## Step 10 — Commit / PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(sbom): add severity-sorted remediation list to SBOM details

Adds RemediationItem and SbomService::remediations, sorted by the existing
SEVERITY_ORDER constant from the advisory module (reused via crate import,
not redeclared - both modules are in the same crate).

Implements TC-9210"
```

`gh pr create --base main` (or fork form if `upstream` remote exists), body includes
`Implements [TC-9210](<webUrl>)`, the SEVERITY_ORDER reuse rationale, and
`Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 — Jira

Set customfield_10875 to the PR URL (ADF inlineCard), add comment (PR link, summary,
deviations — e.g. any approved out-of-scope visibility change) with the implement-task
footnote, transition to In Review.
