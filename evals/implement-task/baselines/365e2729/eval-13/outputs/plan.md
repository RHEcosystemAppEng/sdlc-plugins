# Implementation Plan — TC-9211

**Summary:** Add vulnerability summary extractor for advisory digest emails
**Repository:** trustify-backend (Serena instance: `serena_backend`, rust-analyzer)
**Target Branch:** `main` (no Target PR, no Bookend Type, so this uses the default flow)

> Eval mode: no repository files are changed and no external tools (Jira, git, Serena, gh) are called.
> Each step below says what would happen in a real run.

---

## Step 0 – Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) has everything the skill needs:
- Repository Registry: `trustify-backend | Rust backend service | serena_backend | ./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: the naming convention `mcp__<serena-instance>__<tool>` is present, and `serena_backend` is configured

Result: PASS. Execution continues.

## Step 1 – Parse task

All required sections are present: Repository, Target Branch, Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies. There is no API Changes section, which fits because no endpoint is added. The description is complete, so no clarification is needed.

- Target PR: none. Bookend Type: none.
- GitHub Issue field (`customfield_10747`): would be read from the issue. If it is populated, add `Closes <owner>/<repo>#<n>` to the PR body.
- `webUrl` would be captured for the PR "Implements" link.

## Step 1.5 – Description integrity

Would fetch comments and look for `[sdlc-workflow] Description digest:`. If one is found, compute the digest with `scripts/sha256-digest.py` and compare. If none is found, log a warning and continue.

## Step 2 – Dependencies

The task says "Depends on: None", so there is nothing to check.

## Step 3 – Jira

Would run `jira.user_info()`, then `edit_issue(assignee)`, then transition the issue to In Progress. (Skipped in eval.)

## Step 4 – Understand the code (Serena `serena_backend`)

Planned calls:
1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` to see the `AdvisoryService` method layout and signatures.
2. `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs` to confirm the field types (`cves`, `affected_packages`, `severity_counts`) and check whether the struct derives `Default` and `Clone`. Also confirm the `AffectedPackage` type path.
3. `mcp__serena_backend__find_symbol("IngestorService/ingest_advisory")` to confirm it returns `AdvisoryIngestResult`.
4. Sibling conventions: `get_symbols_overview` on `advisory/model/summary.rs`, `advisory/model/details.rs` and `sbom/model/summary.rs`. This shows the derive set (likely `Serialize, Deserialize, Debug, Clone, PartialEq, ToSchema`), doc comment style and module registration. Run `get_symbols_overview` on `tests/api/advisory.rs` and `tests/api/sbom.rs` for test conventions.
5. Read `CONVENTIONS.md` at the repo root to pull out the CI check commands (fmt, clippy, check, and so on) and any codegen commands, such as OpenAPI generation.
6. Read `modules/fundamental/Cargo.toml` to check whether `fundamental` already depends on the `ingestor` crate. This is needed because the new method takes `&AdvisoryIngestResult`.
7. Symbol deduplication: `search_for_pattern("VulnerabilitySummary|extract_vulnerability_summary|severity_breakdown")` across the workspace, to avoid redeclaring an existing type or helper.
8. Documentation candidates: `README.md`, `docs/api.md` and `docs/architecture.md`. No public endpoint changes, so no doc update is expected.

Expected conventions (to be confirmed by inspection):
- Service methods are `pub async fn ...(&self, ...) -> Result<T, AppError>`, with `.context()` for error wrapping.
- Models are one struct per file under `model/` and registered in `model/mod.rs`.
- Tests are integration tests in `tests/api/` that use `assert_eq!`.

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6 – Changes

### 6.1 Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if sibling models derive ToSchema

/// Digest of an ingested advisory's vulnerability data, for email notifications.
///
/// Every field is non-optional. Missing upstream data becomes zero or empty.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers. Always equals `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty when none).
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory (0 when unknown).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty when severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

Match the derive list exactly to the sibling `AdvisorySummary` once it has been inspected.

### 6.2 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add the method to `impl AdvisoryService`, following the existing `Result<T, AppError>` pattern:

```rust
use trustify_module_ingestor::service::AdvisoryIngestResult; // real crate path confirmed in Step 4
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

/// Builds a [`VulnerabilitySummary`] from an ingestor result for digest emails.
///
/// Each `Option` field in `AdvisoryIngestResult` (`cves`, `affected_packages`,
/// `severity_counts`) gets its own default when it is `None`. The method never
/// panics on missing data. It returns `Err(AppError)` only if a count does not
/// fit in `u32`.
pub fn extract_vulnerability_summary(
    &self,
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // cves: None -> empty list
    let cve_list: Vec<String> = result.cves.as_deref().map(<[String]>::to_vec).unwrap_or_default();

    // affected_packages: None -> 0
    let affected_len = result.affected_packages.as_ref().map_or(0, Vec::len);

    // severity_counts: None -> empty map
    let severity_breakdown = result.severity_counts.clone().unwrap_or_default();

    // cve_count is derived from cve_list, so the two cannot disagree.
    let cve_count = u32::try_from(cve_list.len()).context("CVE count exceeds u32")?;
    let affected_package_count =
        u32::try_from(affected_len).context("affected package count exceeds u32")?;

    Ok(VulnerabilitySummary { cve_count, cve_list, affected_package_count, severity_breakdown })
}
```

Notes:
- The method is synchronous because it does no DB or I/O work. If every sibling method is `async` and callers expect that, make it `async` to keep sibling parity. This is decided after Step 4 inspection.
- The `&self` receiver is kept so the method sits on `AdvisoryService`, as the task requires.
- Whether to use `.context()` or map into an existing `AppError` variant follows `common/src/error.rs`. As an alternative, use `u32::try_from(..).unwrap_or(u32::MAX)` (saturating) if the team prefers an infallible path. In both cases the method does not panic.
- No `.unwrap()`, `.expect()` or indexing is used on upstream data. See `null-guards.md`.

### 6.3 Create `tests/api/advisory_summary.rs`

Each test function gets a `///` doc comment and `// Given / // When / // Then` sections. Assertions check values, not only lengths. Tests build `AdvisoryIngestResult` values directly through a small local helper (`fn ingest_result(cves, pkgs, severity) -> AdvisoryIngestResult`) and call `AdvisoryService::extract_vulnerability_summary`. They follow the setup used in `tests/api/advisory.rs` to construct the service.

| Test | Given | Then (value-based) |
|---|---|---|
| `test_summary_fully_populated` | cves=`Some(["CVE-2024-0001","CVE-2024-0002"])`, 3 affected packages, severity=`{"critical":1,"high":2}` | `assert_eq!(summary, VulnerabilitySummary { cve_count: 2, cve_list: vec![...], affected_package_count: 3, severity_breakdown: {...} })` |
| `test_summary_all_none_returns_zeroed` | all three fields `None` | `assert_eq!(summary, VulnerabilitySummary::default())`, plus explicit checks `cve_count == 0`, `cve_list == Vec::<String>::new()`, `affected_package_count == 0`, `severity_breakdown == HashMap::new()` |
| Mixed Some/None (each None defaults independently) | (a) cves=None and the others Some; (b) affected_packages=None and the others Some; (c) severity_counts=None and the others Some | Only the `None` field takes its default. The others keep their exact values. |
| `test_cve_count_matches_cve_list_len` | cves with 0, 1 and several entries (include `Some(vec![])`) | `assert_eq!(summary.cve_count as usize, summary.cve_list.len())`, and `cve_list` equals the input exactly |

Parameterization (Meszaros heuristic): the three mixed cases share setup, action and assertion structure. If `rstest` is already a dev-dependency of `tests/`, use `#[rstest]` with `#[case]` for the mixed cases and for the cve_count consistency cases. If the sibling tests do not use parameterization, write separate test functions to match the project.

Test registration: if `tests/` uses an explicit harness (for example `tests/api/main.rs` or `mod` lines), the new file has to be registered. That file is not in Files to Modify, so it gets flagged in Step 9 (see below).

### Documentation impact

There is no new endpoint, CLI or config, so no doc updates are expected. The new public symbols get doc comments as shown.

## Step 7 – Tests

Would run `cargo test -p <tests-crate>` and fix any failures (stop after 3 identical failures).

## Step 8 – Acceptance criteria mapping

| AC | Satisfied by |
|---|---|
| Valid summary from fully-populated result | 6.2 plus `test_summary_fully_populated` |
| Handles None values without panicking | `unwrap_or_default` / `map_or` guards, no `unwrap` or `expect`; the all-None and mixed tests |
| Fields always populated with defaults | `VulnerabilitySummary` has no `Option` fields; defaults come from the guards |
| `cve_count` matches `cve_list` length | `cve_count` is computed from `cve_list.len()` after defaulting; `test_cve_count_matches_cve_list_len` |

## Step 9 – Self-verification

- **Scope containment and flags:** the expected diff is the 3 listed files. These changes would probably be needed but are outside Files to Modify / Files to Create, so they would be **flagged for user approval** and not added silently:
  1. `modules/fundamental/src/advisory/model/mod.rs`: needs `pub mod vulnerability_summary;` (and perhaps a `pub use`) so the new struct compiles into the crate.
  2. `modules/fundamental/Cargo.toml`: needs a `trustify-module-ingestor` dependency only if `fundamental` does not already depend on `ingestor`. If adding it would create a dependency cycle (ingestor depending on fundamental), raise this with the user. One option is to move `AdvisoryIngestResult` to `common`, but that is out of scope too.
  3. The test harness registration for `tests/api/advisory_summary.rs`, if the tests crate needs explicit `mod` entries or `[[test]]` entries in Cargo.toml.
- **Untracked file check:** the two new files would be staged explicitly. Look for any other untracked files in the touched directories.
- **Dead parameters:** none. No code is removed.
- **Validated-value override:** not applicable, since no later merge writes into the summary.
- **Sensitive patterns:** none expected. Would grep the staged diff anyway.
- **Duplication check:** grep for existing CVE- or severity-aggregation helpers, such as anything in `AdvisorySummary` or the search module. Reuse one if found.
- **CI checks:** run every command pulled from `CONVENTIONS.md` (for example `cargo fmt --check`, `cargo clippy -- -D warnings`) and any codegen. Any non-zero exit is a hard stop.
- **Rust module tests:** resolve crate names with `cargo metadata --no-deps --format-version 1`, then run `cargo test -p trustify-module-fundamental` and `cargo test -p <tests crate>`.
- **Data-flow trace:** `IngestorService::ingest_advisory()` produces an `AdvisoryIngestResult`, then `AdvisoryService::extract_vulnerability_summary()` applies the guards and defaults, then returns a `VulnerabilitySummary` (serializable for the email digest). Input, processing and output connect. The email sending itself is outside this task's scope and is noted as intentionally absent.
- **Query scope:** not applicable, since there are no DB queries.
- **Contract and sibling parity:** there is no trait contract. Check the derive set, doc comments and `AppError` usage against sibling models and services. Check that the caller site matches how other fundamental code consumes ingestor types.

## Step 10 – Commit / PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds AdvisoryService::extract_vulnerability_summary(), which turns
AdvisoryIngestResult into a non-optional VulnerabilitySummary, defaulting
None cves/affected_packages/severity_counts to empty/zero.

Implements TC-9211"
```

Fork detection: `git remote get-url upstream`. Then `gh pr create --base main`, with the body containing `Implements [TC-9211](<webUrl>)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Jira

Set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment with the PR link, a summary and any deviations (for example, approved out-of-scope `mod.rs` registration), ending with the implement-task footnote. Transition to In Review.
