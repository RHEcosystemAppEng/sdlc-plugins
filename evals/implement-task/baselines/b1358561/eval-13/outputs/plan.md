# Implementation Plan — TC-9211

**Summary:** Add vulnerability summary extractor for advisory digest emails
**Repository:** trustify-backend (Serena instance `serena_backend`, path `./`)
**Target Branch:** `main`
**Mode:** **default** (no Target PR and no Bookend Type). Steps 1–11 run: create branch `TC-9211` from `main`, open a PR against `main`, set the PR field, comment, and move to In Review.

> Eval constraint: no repository files were changed and no external tools were called (Jira, git, Serena, gh). Each external step below says what *would* happen.

---

## Step 0 – Project Configuration validation

From `claude-md-mock.md`:

| Section | Status |
|---|---|
| Repository Registry | PASS: `trustify-backend` → `serena_backend`, path `./` |
| Jira Configuration | PASS: Project key TC, Cloud ID, Feature issue type ID 10142 (also PR field `customfield_10875`, GitHub Issue field `customfield_10747`) |
| Code Intelligence | PASS: naming convention `mcp__<instance>__<tool>`, instance `serena_backend` (rust-analyzer; may need 30–60s to index on first use) |

Configuration is valid, so execution continues.

## Step 1 – Parse task

Every required section is present: Repository, Target Branch, Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies. There is no API Changes section, which is fine because the task adds no endpoint. There is no Target PR, Bookend Type, or Review Context.
- GitHub Issue field `customfield_10747`: would be read from the issue. If it is empty, the step is skipped and the PR body gets no `Closes` line.
- The `webUrl` would be captured for the PR link.

## Step 1.5 – Description digest
Would call `jira.get_issue_comments(TC-9211)`, find the newest `[sdlc-workflow] Description digest:` comment, and compare it with the output of `scripts/sha256-digest.py`. If no digest comment exists, log a warning and continue.

## Step 2 – Dependencies
"Depends on: None", so there is nothing to check.

## Step 3 – Jira
Would call `jira.user_info()`, then assign the issue to the current user with `jira.edit_issue`, then transition it to **In Progress**.

## Step 4 – Understand the code (planned Serena calls)

| Purpose | Call |
|---|---|
| Structure of the file to modify | `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` |
| Existing method pattern (`Result<T, AppError>`, `.context()`) | `find_symbol("AdvisoryService", include_body=false, depth=1)`, then read the body of one method such as `fetch` |
| **Upstream contract** | `find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs`, plus `find_symbol("AffectedPackage", include_body=true)` |
| How the producer fills the fields | `find_symbol("IngestorService/ingest_advisory", include_body=true)`, to learn when each `Option` is `None` and whether `Some(vec![])` can happen |
| Model registration pattern | `get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` and the sibling `summary.rs` (`AdvisorySummary`) for derives (`Serialize`, `Deserialize`, `ToSchema`?, `Debug`, `Clone`, `PartialEq`, `Default`) |
| Crate dependency | Read `modules/fundamental/Cargo.toml` to check whether `trustify-module-ingestor` (or the equivalent) is already a dependency. See the risk below |
| Duplication / reuse | `search_for_pattern("severity_counts\|severity_breakdown\|cve_count")` to look for an existing severity aggregation helper (for example in `AdvisorySummary`, which has a severity field) |
| Test conventions | `get_symbols_overview("tests/api/advisory.rs")` and `tests/api/sbom.rs`, plus `tests/Cargo.toml` for how test files are registered and whether `rstest` is used |
| Conventions | Read `CONVENTIONS.md` at the repo root. Pull out the CI check commands (for example `cargo fmt --check`, `cargo clippy -- -D warnings`) and any codegen commands (for example OpenAPI) |
| Documentation | Look for README/docs about advisory services. `docs/api.md` does not apply because there is no endpoint |

**Expected conventions (from repo-backend.md, to confirm against sibling files):**
- Error handling: service methods return `Result<T, AppError>` and wrap errors with `.context()`.
- Module layout: `model/ + service/ + endpoints/`. A new model file needs `pub mod` in `model/mod.rs`.
- Naming: `verb_noun` methods (`extract_vulnerability_summary`), `PascalCase` structs.
- Tests: integration tests in `tests/api/` that use the real PostgreSQL test DB. HTTP tests use `assert_eq!(resp.status(), StatusCode::OK)`. This extractor is a pure transformation, so its tests assert values directly on the returned struct.

### Risks and conflicts to raise with the user in Step 4

1. **Cross-crate dependency.** `AdvisoryIngestResult` lives in the `ingestor` crate. If `fundamental` does not already depend on `ingestor`, adding that dependency could create a cycle, because the ingestor may already depend on fundamental. If a cycle would result, stop and ask whether to (a) move `AdvisoryIngestResult` to `common`, or (b) take the needed fields through a small input type. Under the Reuse rules, I would not duplicate the struct silently.
2. **Out-of-scope registration files.** The new files only compile if they are registered:
   - `modules/fundamental/src/advisory/model/mod.rs`: add `pub mod vulnerability_summary;` and possibly `pub use`.
   - Test registration: either `tests/Cargo.toml` (a `[[test]]` entry) or a `tests/api/main.rs`/`mod.rs` listing `mod advisory_summary;`, depending on how the existing tests are wired.

   These files are not in Files to Modify or Files to Create. Per Step 6, they are **Step 9 scope flags** that need explicit user approval, not silent plan expansion.
3. **Method placement.** The extractor only transforms data and needs no DB access. It still goes on `AdvisoryService` as an `&self` method returning `Result<VulnerabilitySummary, AppError>`, as the task specifies. I would not change that.

## Step 5 – Branch
```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6 – Implementation

### File to create: `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Digest-ready summary of an advisory's vulnerabilities, used for email notifications.
///
/// Every field is non-optional. Missing upstream data becomes an empty or zero value,
/// so consumers never need to handle `None`.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers; always equals `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty when the advisory has none).
    pub cve_list: Vec<String>,
    /// Number of affected packages (0 when package-level detail is absent).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty when severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```
- Derives follow the sibling `summary.rs`. If the siblings derive `utoipa::ToSchema`, add it too. `Default` gives the all-zero summary.

### File to modify: `modules/fundamental/src/advisory/service/advisory.rs`

Add this method to `impl AdvisoryService`, using Serena `insert_after_symbol` after the last existing method:

```rust
use trustify_module_ingestor::service::AdvisoryIngestResult; // exact path confirmed in Step 4
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

/// Builds a [`VulnerabilitySummary`] from an ingestor result for advisory digest emails.
///
/// `AdvisoryIngestResult` comes from the ingestor module, and all of its aggregate
/// fields are optional. Each `None` field becomes an empty or zero value on its own,
/// so this method never panics on partial data. `cve_count` is always derived from
/// the final `cve_list`, which keeps the two consistent.
pub fn extract_vulnerability_summary(
    &self,
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Guard: cves may be None (advisory has no CVE references).
    let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();

    // Guard: affected_packages may be None (no package-level detail).
    let affected_package_count = result
        .affected_packages
        .as_deref()
        .map_or(0, <[_]>::len);

    // Guard: severity_counts may be None (severity metadata absent).
    let severity_breakdown: HashMap<String, u32> =
        result.severity_counts.clone().unwrap_or_default();

    Ok(VulnerabilitySummary {
        cve_count: u32::try_from(cve_list.len()).context("CVE count exceeds u32")?,
        cve_list,
        affected_package_count: u32::try_from(affected_package_count)
            .context("affected package count exceeds u32")?,
        severity_breakdown,
    })
}
```
- The `Result<T, AppError>` return and `.context()` wrapping match the existing service methods. The only error path is the `usize`→`u32` conversion, which surfaces overflow instead of truncating it with `as u32`.
- If the caller owns the result, a by-value variant (`result: AdvisoryIngestResult`) avoids the clones by moving fields with `result.cves.unwrap_or_default()`. I would pick the signature that matches how sibling service methods take their inputs.
- I would not filter, dedupe, or validate CVE strings, because the task does not ask for it.
- Null-guard details are in `null-guards.md`.

### File to create: `tests/api/advisory_summary.rs`

Fixture helper: `fn ingest_result(cves, affected_packages, severity_counts) -> AdvisoryIngestResult`. The extractor needs no DB, but tests construct `AdvisoryService` the same way the sibling tests in `tests/api/advisory.rs` do (shared test context / DB fixture). If `rstest` is in `tests/Cargo.toml`, use it for the mixed-field cases.

| Test | Given | Then (value-based assertions) |
|---|---|---|
| `extract_summary_fully_populated` | `cves=Some(["CVE-2024-0001","CVE-2024-0002"])`, `affected_packages=Some([pkgA,pkgB,pkgC])`, `severity_counts=Some({"critical":1,"high":2})` | `assert_eq!(summary, VulnerabilitySummary { cve_count: 2, cve_list: vec!["CVE-2024-0001".into(), "CVE-2024-0002".into()], affected_package_count: 3, severity_breakdown: HashMap::from([("critical".into(),1),("high".into(),2)]) })` |
| `extract_summary_all_none` | all three `None` | `assert_eq!(summary, VulnerabilitySummary::default())`, and spell out `cve_count == 0`, `cve_list.is_empty()`, `affected_package_count == 0`, `severity_breakdown.is_empty()` |
| `extract_summary_mixed_fields` (parameterized with `rstest` if the project uses it, otherwise 3 separate tests) | (a) only `cves` Some; (b) only `affected_packages` Some; (c) only `severity_counts` Some | Each `None` field gets its default and each `Some` field keeps its exact values. Compare the whole struct with `assert_eq!` |
| `extract_summary_cve_count_matches_list` | `cves=Some(vec![])`, `Some(one)`, `Some(three)`, and `None` | `assert_eq!(summary.cve_count as usize, summary.cve_list.len())` plus a check on the actual list contents |

- Each test gets a `///` doc comment and `// Given / // When / // Then` sections.
- The tests assert on values, comparing whole structs, not only lengths.
- The fixture CVE IDs are distinct, but no test assumes uniqueness, because the contract does not require it.

### Documentation impact
There is no Documentation Updates section and no endpoint or config change. No doc edits are needed. New symbols get doc comments as shown above.

## Step 7 – Run tests
`cargo test -p <fundamental crate>` plus the integration test crate, with crate names resolved via `cargo metadata --no-deps --format-version 1`.

## Step 8 – Acceptance criteria

| Criterion | How it is satisfied |
|---|---|
| Valid summary from a fully populated result | `extract_summary_fully_populated` |
| Handles `None` for cves, affected_packages, and severity_counts without panicking | `unwrap_or_default` / `map_or(0, …)` guards, with no `unwrap()`, `expect()`, or indexing. Covered by `extract_summary_all_none` and `extract_summary_mixed_fields` |
| Fields always populated with sensible defaults | The struct has non-`Option` fields and derives `Default` |
| `cve_count` matches `cve_list.len()` | `cve_count` is computed from the final `cve_list`. Covered by `extract_summary_cve_count_matches_list` |

## Step 9 – Self-verification (expected results)

| # | Check | Expected |
|---|---|---|
| 1 | Scope containment | **FLAGGED**: `advisory/model/mod.rs` (module registration) and the test registration file (`tests/Cargo.toml` or the test `main.rs`), plus `modules/fundamental/Cargo.toml` if the ingestor dependency is missing. Each needs user approval before commit |
| 2 | Untracked files | The new files sit next to modified files. Each is referenced from its `mod.rs`/test registration, so they are staged only after approval |
| 3 | Sensitive patterns | PASS (no secrets) |
| 4 | Dead parameters | N/A (no code removed) |
| 5 | Duplication | Search for existing severity/CVE aggregation helpers. If one exists, reuse it |
| 6 | Documentation currency | Does not fire (no public API, config, or setup change, apart from a new service method) |
| 10 | Cross-section references | PASS: `AdvisoryIngestResult` path (`modules/ingestor/src/service/mod.rs`) is consistent between Description and Implementation Notes. `AdvisoryService` is at `advisory/service/advisory.rs` |
| 11 | Data-flow trace | `IngestorService::ingest_advisory()` → `AdvisoryIngestResult` → `extract_vulnerability_summary()` → `VulnerabilitySummary`. The email-sending consumer is out of scope (parent TC-9001), so report it as intentionally out of scope |
| 12 | Query scope | N/A (no DB batch) |
| 13 | Contract & sibling parity | Contract: honors `AdvisoryIngestResult`'s `Option` types. Sibling: same `Result<_, AppError>` and `.context()` pattern. Cross-module entity: N/A. Caller-site: check the other consumers of `AdvisoryIngestResult` for how they treat `None` |
| 14 | CI checks | Run the commands from CONVENTIONS.md (fmt, clippy, etc.). A failure is a hard stop |
| 15 | Module tests (Rust) | `cargo test -p` for each modified crate, resolved via `cargo metadata` |
| 16 | Validated-value override | N/A |

## Step 10 – Commit and PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds VulnerabilitySummary and AdvisoryService::extract_vulnerability_summary(),
which turns AdvisoryIngestResult into a non-optional digest. None fields for
cves, affected_packages and severity_counts each default to empty/zero.

Implements TC-9211"
```
Check for a fork with `git remote get-url upstream`, then `gh pr create --base main …`. The PR body starts with `Implements [TC-9211](<webUrl>)`, adds `Closes owner/repo#N` only if the GitHub Issue field is set, and records any choice to export or inline (for example, how the ingestor type was imported).

## Step 11 – Jira
- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Add a comment with the PR link, a summary, and any deviations (for example, approved registration files). The comment ends with the `implement-task` footnote.
- Transition to **In Review**.
