# Implementation Plan — TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, rust-analyzer)
**Target Branch**: `main`
**Task branch**: `TC-9211`
**Skill**: `/sdlc-workflow:implement-task` (followed from SKILL.md directly; the Skill tool did not recognise the skill name)

> This is a simulated run. No repository files were modified, and no calls were made to Jira, git, GitHub or Serena. Every step that would touch an external system says below what it would have done.

---

## Step 0 — Project Configuration validation

`claude-md-mock.md` has all the required sections under `# Project Configuration`:

- **Repository Registry**: present. 1 entry (`trustify-backend`, `serena_backend`, `./`).
- **Jira Configuration**: present. Project key `TC`, Cloud ID, and Feature issue type ID `10142` are all set. The optional fields are also set: Git PR field `customfield_10875` and GitHub Issue field `customfield_10747`.
- **Code Intelligence**: present, with the `mcp__<serena-instance>__<tool>` naming convention.

Result: PASS. Execution continues.

## Step 1 — Parse the task

| Section | Status | Value |
|---|---|---|
| Repository | present | trustify-backend |
| Target Branch | present | main |
| Description | present | Extractor for `AdvisoryIngestResult` producing a digest |
| Files to Modify | present | `modules/fundamental/src/advisory/service/advisory.rs` |
| Files to Create | present | `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | absent | No endpoint changes. This is a service-level method only, so the absence is consistent. |
| Implementation Notes | present | `Result<T, AppError>` pattern; defaults for each `None` field |
| Acceptance Criteria | present | 4 criteria |
| Test Requirements | present | 4 tests |
| Target PR | absent | Default flow: new branch and new PR |
| Bookend Type | absent | Normal implementation |
| Dependencies | present | None |

- **GitHub Issue custom field** (`customfield_10747`): would be read from the issue. Not available in the mock, so it is skipped silently and no `Closes` line is added.
- **webUrl**: would be captured from the issue response, e.g. `https://redhat.atlassian.net/browse/TC-9211`.

## Step 1.5 — Description integrity

Would fetch the comments, look for `[sdlc-workflow] Description digest:`, and compare it against the output of `python3 scripts/sha256-digest.py`. The mock has no digest comment, so the skill logs this warning and proceeds: "No description digest found — skipping integrity check."

## Step 2 — Dependencies

`Depends on: None`, so there is nothing to verify.

## Step 3 — Jira transition (simulated)

Would call `jira.user_info()`, then `jira.edit_issue(TC-9211, assignee=<me>)`, then transition the issue to **In Progress**.

## Step 4 — Understand the code (planned Serena calls)

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` to see the `AdvisoryService` methods (fetch, list, search) and their signatures.
2. `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs` to confirm the exact field types:
   - `cves: Option<Vec<String>>`
   - `affected_packages: Option<Vec<AffectedPackage>>`
   - `severity_counts: Option<HashMap<String, u32>>`
   - whether the struct derives `Clone`/`Default`, so test fixtures can be built
   - whether it is `pub` and re-exported from the `ingestor` crate root
3. `mcp__serena_backend__find_symbol("AffectedPackage")` to check its visibility. Tests need to construct it.
4. **Check the dependency relationship**: read `modules/fundamental/Cargo.toml` to see whether `fundamental` already depends on `ingestor`.
   - If it does, import `ingestor::service::AdvisoryIngestResult` directly.
   - If it does not, adding that dependency would mean editing `Cargo.toml`, which is out of scope. I would flag this to the user before implementing (see the risks below).
5. **Sibling conventions**: `get_symbols_overview` on `advisory/model/summary.rs`, `advisory/model/details.rs` and `sbom/model/summary.rs`, to pick up derive sets (likely `Serialize, Deserialize, Debug, Clone, PartialEq, ToSchema`), doc-comment style and field naming.
6. **Test conventions**: `get_symbols_overview` on `tests/api/advisory.rs` and `tests/api/sbom.rs` to pick up the test harness setup, how `AdvisoryService` is constructed in tests, and the assertion style.
7. **Symbol deduplication**: `search_for_pattern("VulnerabilitySummary|vulnerability_summary|severity_breakdown")` across `modules/` to make sure no equivalent struct or helper already exists. Also check whether `AdvisorySummary.severity` already has a severity-key type to reuse.
8. **CONVENTIONS.md**: read it at the repo root (it exists in the tree). Extract the CI check commands (likely `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) and any codegen commands (e.g. OpenAPI generation) for Step 9.
9. **Documentation files**: `README.md`, `docs/architecture.md`, `docs/api.md`. No public API or endpoint changes are expected, so no doc updates are anticipated.

**Expected conventions (to be confirmed from siblings):**

- Service methods return `Result<T, AppError>` and use `.context()` for wrapping.
- Model structs live one per file under `model/` and are declared in `model/mod.rs`.
- Naming follows `verb_noun` for methods and `snake_case` file names matching the struct.
- Integration tests in `tests/api/` use `assert_eq!` on concrete values.

## Step 5 — Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6 — Changes

### 6.1 Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Digest of an ingested advisory's vulnerability data, used for email notifications.
///
/// All fields are non-optional. Missing upstream data is represented by zero counts
/// and empty collections.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers. Always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty if none).
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory (0 if unknown).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty if severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

- The derive set will be aligned with the sibling `summary.rs`. If the siblings derive `utoipa::ToSchema`, I will add it too.
- `Default` is derived because it describes the all-`None` result exactly. That gives the "zeroed summary" a single canonical definition.

### 6.2 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `impl AdvisoryService`:

```rust
use std::collections::HashMap;
use ingestor::service::AdvisoryIngestResult; // exact path confirmed in Step 4
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    /// Builds a [`VulnerabilitySummary`] from an ingestor result for digest emails.
    ///
    /// Every `Option` field on `AdvisoryIngestResult` is treated as possibly absent:
    /// a missing `cves` gives an empty list with count 0, a missing `affected_packages`
    /// gives a count of 0, and a missing `severity_counts` gives an empty breakdown.
    /// This method never panics on missing data.
    pub fn extract_vulnerability_summary(
        &self,
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();

        let affected_package_count = result
            .affected_packages
            .as_ref()
            .map_or(0, |pkgs| saturating_u32(pkgs.len()));

        let severity_breakdown: HashMap<String, u32> =
            result.severity_counts.clone().unwrap_or_default();

        Ok(VulnerabilitySummary {
            // Derived from cve_list so the two can never disagree.
            cve_count: saturating_u32(cve_list.len()),
            cve_list,
            affected_package_count,
            severity_breakdown,
        })
    }
}

/// Converts a collection length to `u32`, saturating at `u32::MAX` instead of truncating.
fn saturating_u32(len: usize) -> u32 {
    u32::try_from(len).unwrap_or(u32::MAX)
}
```

Design notes:

- **Signature**: it returns `Result<VulnerabilitySummary, AppError>` to match the sibling service-method pattern required by the Implementation Notes, even though the current logic cannot fail. That keeps room for future validation without breaking callers.
- **Sync vs async**: siblings are `async` because they hit the database. This method is pure, so it is a sync `fn`. If the conventions require every service method to be `async`, I would make it `async fn` for consistency.
- **Borrowing**: it takes `&AdvisoryIngestResult` so the caller keeps ownership. It clones only the two collections that get copied into the output.
- **Helper reuse**: before adding `saturating_u32`, I would grep `common/` for an existing length-to-`u32` helper and reuse it if one exists. If none exists, it stays a private module-local function. It is too small to justify a shared utility.

### 6.3 Create `tests/api/advisory_summary.rs`

There are 4 test functions, one per Test Requirement. Each has a `///` doc comment and `// Given / // When / // Then` sections. A local `fn ingest_result(cves, pkgs, severity) -> AdvisoryIngestResult` fixture builder avoids repeating the struct literal.

| Test | Given | Then (value-based asserts) |
|---|---|---|
| `extracts_summary_from_fully_populated_result` | `cves=Some(["CVE-2024-0001","CVE-2024-0002"])`, `affected_packages=Some([pkgA,pkgB,pkgC])`, `severity_counts=Some({"critical":1,"high":2})` | `assert_eq!(summary, VulnerabilitySummary { cve_count: 2, cve_list: vec![..both..], affected_package_count: 3, severity_breakdown: {critical:1, high:2} })` |
| `all_none_fields_yield_zeroed_summary` | all three fields `None` | `assert_eq!(summary, VulnerabilitySummary::default())`, plus explicit `assert_eq!(summary.cve_list, Vec::<String>::new())` and `assert_eq!(summary.severity_breakdown, HashMap::new())` |
| `mixed_some_none_fields_default_independently` | parameterised over 3 rows: (cves Some, others None), (packages Some, others None), (severity Some, others None) | each row asserts the full expected `VulnerabilitySummary`. The `None` fields default and the `Some` field carries through. |
| `cve_count_matches_cve_list_length` | parameterised over `cves` = `None`, `Some([])`, `Some([1 item])`, `Some([3 items])` | `assert_eq!(summary.cve_count as usize, summary.cve_list.len())` and `assert_eq!(summary.cve_list, expected_list)` |

- **Parameterisation**: the mixed and cve_count cases share the same setup, action and assertion structure with different data (Meszaros heuristic). If the sibling tests use `rstest`, I would use `#[rstest] #[case(...)]`. If they do not use any parameterised mechanism, I would follow the project pattern and write separate functions instead.
- I also considered `Some(vec![])` for `affected_packages` and `Some(HashMap::new())` for `severity_counts`. An empty `Some` must produce the same result as `None`, so these are added as rows in the mixed table.
- No HTTP layer is involved, so the `assert_eq!(resp.status(), StatusCode::OK)` convention does not apply. The `AdvisoryService` instance is constructed the same way as in `tests/api/advisory.rs`.

### 6.4 Documentation impact

No endpoints, configuration or CLI changes. `docs/api.md` and the README need no update.

## Step 7 — Run tests (simulated)

```
cargo test -p trustify-module-fundamental   # crate name resolved via cargo metadata
cargo test -p <tests crate> advisory_summary
```

## Step 8 — Acceptance Criteria mapping

| AC | Covered by |
|---|---|
| Valid summary from fully-populated result | `extracts_summary_from_fully_populated_result` |
| Handles `None` for all three fields without panicking | `all_none_fields_yield_zeroed_summary`, mixed table. The implementation has no `unwrap()`/`expect()`/indexing. |
| Fields always populated with sensible defaults | Struct has no `Option` fields. `Default` = zeroed. |
| `cve_count == cve_list.len()` | `cve_count` is computed from `cve_list.len()` after defaulting, and `cve_count_matches_cve_list_length` checks it |

## Step 9 — Self-verification plan

- **Scope containment**: the expected diff covers `advisory/service/advisory.rs` (modify), `advisory/model/vulnerability_summary.rs` (new) and `tests/api/advisory_summary.rs` (new). **Out-of-scope files that will probably be needed, flagged for user approval rather than edited silently:**
  1. `modules/fundamental/src/advisory/model/mod.rs`: needs `pub mod vulnerability_summary;`, otherwise the new file is not compiled.
  2. `tests/Cargo.toml` (`[[test]]` entry) or the test crate's module root: needed if test files are registered explicitly.
  3. `modules/fundamental/Cargo.toml`: only if `fundamental` does not already depend on `ingestor`.
- **Untracked file check**: the new files will appear as `??`. Both are listed in Files to Create, so staging them is expected.
- **Dead parameters**: N/A. Nothing is removed.
- **Sensitive patterns**: run the grep on the staged diff. None are expected.
- **Duplication check**: grep for `unwrap_or_default` summary builders and any existing `VulnerabilitySummary`.
- **CI checks**: run every command extracted from CONVENTIONS.md. Any non-zero exit is a hard stop.
- **Rust module-level tests**: `cargo test -p <crate>` for `fundamental` and for the tests crate.
- **Data-flow trace**: `IngestorService::ingest_advisory()` → `AdvisoryIngestResult` (input) → `extract_vulnerability_summary` (defaulting and counting) → `VulnerabilitySummary` (output). The consumer that renders the digest email is not part of this task. That stage is intentionally out of scope and would be raised with the user.
- **Query scope**: N/A. No DB iteration.
- **Contract and sibling parity**:
  - Contract: no traits are implemented.
  - Sibling parity: return type and error type match. Check whether siblings log with `tracing` and add a `debug!` if they do.
  - Cross-module entity: no DB writes.
  - Caller-site: this is a new abstraction with no existing callers.

## Step 10 — Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds AdvisoryService::extract_vulnerability_summary(), which converts an
AdvisoryIngestResult into a VulnerabilitySummary with non-optional fields.
None values for cves, affected_packages and severity_counts default to
empty collections or zero counts.

Implements TC-9211"
```

- **Fork detection**: run `git remote get-url upstream`. If it exists, use `gh pr create -R <upstream> --head <fork-owner>:TC-9211 --base main`. Otherwise use `gh pr create --base main`.
- **PR body**: include `Implements [TC-9211](https://redhat.atlassian.net/browse/TC-9211)`. Add a `Closes owner/repo#N` line only if `customfield_10747` is set.

## Step 11 — Jira update (simulated)

- Set `customfield_10875` to the ADF `inlineCard` containing the PR URL.
- Add a comment with the PR link, a summary of the changes, and any deviations (e.g. approved changes to `model/mod.rs`). The comment ends with the footnote from `shared/comment-footnote.md` using skill name `implement-task`.
- Transition the issue to **In Review**.

## Open risks and questions

1. **Cross-crate dependency**: does `fundamental` already depend on `ingestor`? If not, adding the dependency (or moving the extractor) needs a user decision.
2. **Module registration**: `model/mod.rs` and possibly test registration are outside Files to Modify. User approval is needed.
3. **`AffectedPackage` constructibility**: if it has private fields and no constructor, the tests need a public builder or `Default`. This would be flagged if found.
