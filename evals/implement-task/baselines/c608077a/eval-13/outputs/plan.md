# Implementation Plan — TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, path `./`)
**Target Branch**: `main` (no Target PR, no Bookend Type → default flow)
**Branch to create**: `TC-9211`

---

## Step 0 – Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) contains all three required sections:

| Section | Status |
|---|---|
| Repository Registry | trustify-backend → `serena_backend`, path `./` |
| Jira Configuration | Project key TC, Cloud ID, Feature issue type ID 10142 all present (also PR field `customfield_10875`, GitHub Issue field `customfield_10747`) |
| Code Intelligence | Present, tool naming convention `mcp__<serena-instance>__<tool>`; limitation: rust-analyzer may need 30-60s to index |

Validation passes, so execution continues.

## Step 1 – Parse task (simulated `jira.get_issue(TC-9211)`)

All required sections are present: Repository, Target Branch, Description, Files to Modify,
Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies.
There's no API Changes section, which is expected: this is a service-level method with no new endpoint.
- Target PR: none, Bookend Type: none
- GitHub Issue custom field `customfield_10747`: would be read from the issue. Nothing is supplied in the mock, so it's skipped silently and there's no `Closes` line.

## Step 1.5 – Description integrity (simulated)

The mock has no digest comment. I'd log "No description digest found — skipping integrity check" and continue.

## Step 2 – Dependencies

"Depends on: None", so there's nothing to verify.

## Step 3 – Jira transition (simulated, not executed)

`jira.user_info()` → `jira.edit_issue(TC-9211, assignee=<me>)` → `jira.transition_issue → In Progress`.

## Step 4 – Understand the code (planned Serena calls)

| Purpose | Call |
|---|---|
| Structure of service file | `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` |
| Existing method pattern | `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true, depth=1)` |
| Upstream struct definition | `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs` |
| Element type | `mcp__serena_backend__find_symbol("AffectedPackage", include_body=true)` |
| Producer | `mcp__serena_backend__find_symbol("IngestorService/ingest_advisory", include_body=true)` to confirm when each field comes back `None` |
| Sibling models | `get_symbols_overview` on `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs` (derives, serde attributes, doc comments) |
| Model registration | `get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` (are submodules declared `pub mod x;` and re-exported?) |
| Test conventions | `get_symbols_overview` on `tests/api/advisory.rs`, `tests/api/sbom.rs` and inspect `tests/Cargo.toml` for how test files are registered |
| Crate dependency | Read `modules/fundamental/Cargo.toml` to check whether `trustify-module-ingestor` (or equivalent) is already a dependency |
| Duplication | `search_for_pattern("severity_counts|severity_breakdown|VulnerabilitySummary|cve_count")` across the workspace |
| Conventions | Read `CONVENTIONS.md` at repo root and extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) |

### Discovered / expected conventions (from repo-backend.md)
- **Module pattern**: `model/ + service/ + endpoints/`. The new struct goes in `advisory/model/`.
- **Error handling**: service methods return `Result<T, AppError>` (AppError is in `common/src/error.rs`), with `.context()` wrapping where fallible.
- **Naming**: `verb_noun` methods (`fetch`, `list`, `search`, so `extract_vulnerability_summary`), `XxxSummary` structs.
- **Model derives** (to confirm against `AdvisorySummary`): `#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]`.
- **Tests**: integration tests under `tests/api/`, run against a real PostgreSQL test DB, status checks use `assert_eq!(resp.status(), StatusCode::OK)`. The new tests call the service directly, so they use value assertions on the returned struct.

### Documentation files identified
- `CONVENTIONS.md` (root): followed throughout.
- `README.md`, `docs/architecture.md`, `docs/api.md`: no public endpoint is added, so I don't expect any doc changes (re-checked in Step 9).

## Step 5 – Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6 – Implement changes

### 6.1 Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if sibling models derive ToSchema

/// Digest-ready vulnerability summary for a single ingested advisory, used by
/// email notifications. All fields are non-optional; missing upstream data is
/// represented by zero counts and empty collections.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers; always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty when none).
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory (0 when unknown).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty when severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

`#[derive(Default)]` makes the "all-None gives a zeroed summary" contract explicit and
lets tests compare against `VulnerabilitySummary::default()`.

### 6.2 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add imports:
```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;
use trustify_module_ingestor::service::AdvisoryIngestResult; // exact path confirmed via Serena
```

Add the method to `impl AdvisoryService`:

```rust
/// Builds a [`VulnerabilitySummary`] from an ingestor result for use in advisory
/// digest emails.
///
/// `AdvisoryIngestResult` comes from the ingestor module and every aggregate
/// field is `Option<T>`. Each `None` is replaced independently with a sensible
/// default: empty CVE list (count 0), affected package count 0, and an empty
/// severity breakdown. The method never panics on missing data.
pub fn extract_vulnerability_summary(
    &self,
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // cves: Option<Vec<String>>; None → empty list
    let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();
    // Derive the count from the list so cve_count == cve_list.len() always holds
    let cve_count = saturating_u32(cve_list.len());

    // affected_packages: Option<Vec<AffectedPackage>>; None → 0, no clone needed
    let affected_package_count =
        saturating_u32(result.affected_packages.as_ref().map_or(0, Vec::len));

    // severity_counts: Option<HashMap<String, u32>>; None → empty map
    let severity_breakdown = result.severity_counts.clone().unwrap_or_default();

    Ok(VulnerabilitySummary {
        cve_count,
        cve_list,
        affected_package_count,
        severity_breakdown,
    })
}
```

Plus a small private helper in the same file (no truncating `as` casts):

```rust
/// Converts a collection length to `u32`, saturating at `u32::MAX` instead of truncating.
fn saturating_u32(n: usize) -> u32 {
    u32::try_from(n).unwrap_or(u32::MAX)
}
```

Design notes:
- **Return type**: `Result<VulnerabilitySummary, AppError>`, following the Implementation Notes and sibling methods. The current body can't fail, but the `Result` keeps the API consistent and leaves room for future validation.
- **Sync, not async**: there's no DB access. If sibling methods are all `async` and take a `&Transactional`/connection, I'd keep it sync and note that in the PR, because adding an unused connection parameter would be a dead parameter.
- **Borrow input** (`&AdvisoryIngestResult`): the caller keeps ownership. Only the CVE list and severity map are cloned, because they go into the output. `affected_packages` is only counted, never cloned.
- **No `unwrap()` / `expect()` / indexing** anywhere on the upstream data.
- Before writing the helper, search for an existing `usize → u32` saturating helper in `common/` (symbol deduplication) and reuse it if one exists.

### 6.3 Create `tests/api/advisory_summary.rs`

Fixtures are built in-memory with an `AdvisoryIngestResult` constructor helper. Each test has a `///` doc comment and Given/When/Then sections. The helper builds `AdvisoryIngestResult { cves, affected_packages, severity_counts, ..Default::default() }`, or sets every field explicitly if the struct doesn't derive `Default`. Tests get `AdvisoryService` the same way `tests/api/advisory.rs` does (test DB context), because the service is constructed with a DB handle.

| Test | Given | Then (value-based assertions) |
|---|---|---|
| `test_extract_summary_fully_populated` | cves = `["CVE-2024-0001","CVE-2024-0002"]`, 3 affected packages, severity `{critical:1, high:2}` | `summary == VulnerabilitySummary { cve_count: 2, cve_list: vec!["CVE-2024-0001","CVE-2024-0002"], affected_package_count: 3, severity_breakdown: {critical:1, high:2} }` |
| `test_extract_summary_all_none` | all three fields `None` | `summary == VulnerabilitySummary::default()`, plus explicit checks `cve_count == 0`, `cve_list.is_empty()`, `affected_package_count == 0`, `severity_breakdown.is_empty()`, and no panic |
| `test_extract_summary_mixed_fields` (parameterized with `rstest` only if the tests crate already uses it; otherwise three separate tests) | each case sets exactly one field to `None`: (cves None), (affected_packages None), (severity_counts None) | the `None` field is defaulted and the other two carry their exact values, so each field defaults independently |
| `test_cve_count_matches_cve_list_len` | cases: `None`, `Some(vec![])`, `Some(vec![1 CVE])`, `Some(vec![3 CVEs])` | `summary.cve_count as usize == summary.cve_list.len()` **and** `cve_list` equals the expected values |
| `test_extract_summary_empty_vecs_vs_none` (extra edge case) | `Some(vec![])` / `Some(HashMap::new())` | gives the same result as `None` (zeroed summary) |

No uniqueness constraint is asserted on CVEs. The contract doesn't require dedup.

Then run `cargo test -p <fundamental-crate>` and the tests crate (the package names are resolved with `cargo metadata --no-deps --format-version 1`).

### 6.4 Documentation impact
There's no endpoint, config, or CLI change and no Documentation Updates section, so no doc edits are planned.

## Step 7 – Tests
See 6.3. The tests follow the project test layout (`tests/api/`) and use value assertions on the whole struct instead of length-only checks.

## Step 8 – Acceptance criteria mapping

| Criterion | How it's satisfied |
|---|---|
| Valid summary from fully-populated result | Method maps every `Some` value; checked by `test_extract_summary_fully_populated` |
| Handles `None` for cves / affected_packages / severity_counts without panicking | `unwrap_or_default()` / `map_or(0, ..)`, with no unwrap or indexing; checked by the all-None and mixed tests |
| Output fields always populated with sensible defaults | `VulnerabilitySummary` has only non-`Option` fields and derives `Default` |
| `cve_count` matches `cve_list.len()` | Count is computed from the final `cve_list`, never from a separate source; checked by `test_cve_count_matches_cve_list_len` |

## Step 9 – Self-verification (planned)

### Scope containment: files that are probably needed but aren't listed
The task lists 1 file to modify and 2 to create. Wiring up the new files will probably also need
changes to these files, which **are not in Files to Modify**. I would **not** edit them silently.
I'd raise them for user approval:

1. `modules/fundamental/src/advisory/model/mod.rs`: needs `pub mod vulnerability_summary;` (and possibly a `pub use`), otherwise the new struct isn't compiled or reachable.
2. Test registration: depending on how `tests/` is set up, either `tests/Cargo.toml` (a `[[test]]` entry) or a test root module (e.g. `tests/api/main.rs` / `mod.rs`) needs `mod advisory_summary;`.
3. `modules/fundamental/Cargo.toml`: only if `fundamental` doesn't already depend on the ingestor crate. Adding a cross-crate dependency here is an architectural decision, so I'd check it before implementing and ask the user. One alternative is to move `AdvisoryIngestResult` into `common`, which is also out of scope.

### Other checks
- **Cross-section consistency**: `AdvisoryIngestResult` is named consistently in the Description and Implementation Notes (`modules/ingestor/src/service/mod.rs`). I'd verify the actual field types match the task (`Option<Vec<String>>`, `Option<Vec<AffectedPackage>>`, `Option<HashMap<String, u32>>`). If they differ (e.g. `u64` counts), I'd stop and report.
- **Duplication check**: grep for an existing CVE/severity aggregation helper (for example in `AdvisorySummary` construction) and reuse it if found.
- **Dead parameters**: none. The method uses both `&self`, for consistency, and `result`. Nothing is removed.
- **Sensitive patterns**: none expected.
- **CI checks**: run every command extracted from `CONVENTIONS.md`. Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p <fundamental crate>` plus the tests package. A failure is a hard stop.
- **Data-flow trace**: `IngestorService::ingest_advisory()` gives `AdvisoryIngestResult` (input), then `extract_vulnerability_summary()` applies the None-guards and counts (processing), then returns `VulnerabilitySummary` (output). The email digest consumer isn't in this task's scope, so I'd flag the output stage as intentionally terminal at the service API.
- **Contract & sibling parity**: no trait is implemented. Sibling parity covers `Result<_, AppError>`, doc comments, and model derives matching `AdvisorySummary`. Caller-site: `ingest_advisory()` callers are inspected to confirm that results are passed by reference/owned in a compatible way. No shared DB entity is written.

## Step 10 – Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for digest emails

Add VulnerabilitySummary model and AdvisoryService::extract_vulnerability_summary(),
which converts the ingestor's AdvisoryIngestResult into a non-optional summary.
None values for cves, affected_packages and severity_counts default independently
to empty/zero values.

Implements TC-9211"
```
- Fork detection with `git remote get-url upstream`, then `gh pr create --base main ...`
- PR body: `Implements [TC-9211](https://redhat.atlassian.net/browse/TC-9211)`. There's no `Closes` line because the GitHub Issue field is empty.

## Step 11 – Jira (simulated)
- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary of changes, and deviations: the out-of-scope registration files if approved, and the sync method if applicable. The comment ends with the `implement-task` footnote from `shared/comment-footnote.md`.
- Transition to **In Review**.
