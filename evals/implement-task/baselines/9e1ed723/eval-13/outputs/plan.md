# Implementation Plan — TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, rust-analyzer)
**Target Branch**: `main`
**Task branch**: `TC-9211`

> Simulated run: no repository files changed, and no Jira, git or Serena calls were made.
> Each step lists the action the skill would take.

---

## Step 0 — Project Configuration validation

`claude-md-mock.md` has every required section:

- Repository Registry: 1 entry (`trustify-backend`, `serena_backend`, `./`). PASS
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`. PASS
- Code Intelligence: present, with the `mcp__<serena-instance>__<tool>` naming convention. PASS

Execution continues.

## Step 1 — Parse the task

| Section | Present | Notes |
|---|---|---|
| Repository | yes | trustify-backend |
| Target Branch | yes | `main` (direct-to-main flow) |
| Description | yes | Extractor that reads `AdvisoryIngestResult` and produces a digest |
| Files to Modify | yes | `modules/fundamental/src/advisory/service/advisory.rs` |
| Files to Create | yes | `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | no | No endpoints. The task only adds a service method. |
| Implementation Notes | yes | |
| Acceptance Criteria | yes | 4 items |
| Test Requirements | yes | 4 items |
| Target PR | no | Default flow: new branch and new PR |
| Bookend Type | no | Normal implementation |
| Dependencies | yes | "None" |

The description follows the template, so the skill does not stop.
- The GitHub Issue custom field (`customfield_10747`) would be read from the issue. If it is empty, the skill skips it silently.
- The link "is incorporated by TC-9001" points to the parent feature. It is not a blocking dependency.

## Step 1.5 — Description integrity

The skill would fetch the comments, look for the latest `[sdlc-workflow] Description digest:` comment, and compare digests using `scripts/sha256-digest.py`. If no digest comment exists, it would log a warning and continue.

## Step 2 — Dependencies

Dependencies are "None", so there is nothing to verify.

## Step 3 — Jira transition

The skill would call `jira.user_info()`, assign the issue to the current user, and transition it to In Progress. All three calls were simulated.

## Step 4 — Understand the code (planned Serena calls)

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")`: list the `AdvisoryService` methods (fetch, list, search) and their `Result<T, AppError>` signatures.
2. `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs`: confirm the exact field types (`Option<Vec<String>>`, `Option<Vec<AffectedPackage>>`, `Option<HashMap<String, u32>>`) and check for any other optional fields.
3. `mcp__serena_backend__find_symbol("AffectedPackage")`: find where the type is defined and whether it is `pub`.
4. `mcp__serena_backend__find_symbol("IngestorService/ingest_advisory")`: confirm it returns `AdvisoryIngestResult`.
5. Sibling conventions:
   - `get_symbols_overview` on `advisory/model/summary.rs`, `advisory/model/details.rs` and `sbom/model/summary.rs`: derives (`Serialize`, `Deserialize`, `ToSchema`, `Debug`, `Clone`), doc comments, field naming.
   - `get_symbols_overview` on `tests/api/advisory.rs` and `tests/api/sbom.rs`: test harness and assertion style.
6. Reuse and duplication search: `search_for_pattern("severity_counts|severity_breakdown|cve_count|VulnerabilitySummary")` across the workspace. The goal is to avoid redeclaring a severity map or summary type that already exists. `AdvisorySummary` already has a `severity` field, and the plan would reuse any severity-level constants found there.
7. Dependency check: read `modules/fundamental/Cargo.toml` to see whether the `ingestor` crate is already a dependency of `fundamental`. **This must be confirmed.** If it is not a dependency, the method cannot accept `AdvisoryIngestResult` without changing `Cargo.toml`, and `Cargo.toml` is out of scope. Also check that adding the dependency would not create a cycle, for example if ingestor already depends on fundamental. If it would, the skill escalates to the user (see Risks).
8. Read `CONVENTIONS.md` at the repo root. Extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`) and any code-generation commands for use in Step 9.
9. Documentation: `README.md`, `CONVENTIONS.md`, `docs/architecture.md`, `docs/api.md`. No API is added, so no documentation update is expected.

### Conventions found (from repo-backend.md, to be confirmed with Serena)

- **Error handling**: service methods return `Result<T, AppError>` (`common/src/error.rs`) and wrap errors with `.context()`.
- **Module pattern**: `model/ + service/ + endpoints/`. Each model struct lives in its own file under `model/` and is re-exported from `model/mod.rs`.
- **Naming**: `verb_noun` method names (`extract_vulnerability_summary`), and `PascalCase` structs with a `Summary`/`Details` suffix.
- **Tests**: integration tests in `tests/api/<domain>.rs`, with `assert_eq!` as the assertion style. The task's test cases are pure data transformations, so they do not need HTTP calls or database fixtures.
- **Parameterized tests**: the plan uses `rstest` only if sibling tests already use it. Otherwise each scenario gets its own documented `#[test]` function.

## Step 5 — Branch

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6 — Changes per file

### 1. CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Digest of an advisory's vulnerability data, suitable for email notifications.
///
/// All fields are non-optional. Missing upstream data becomes an empty or zero value.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers. Always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty when none).
    pub cve_list: Vec<String>,
    /// Number of affected packages (0 when no package-level detail is available).
    pub affected_package_count: u32,
    /// Counts per severity level (empty when severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

- `Default` gives a zeroed summary, which is the all-`None` case.
- Add `ToSchema` / `utoipa` derives only if the sibling `summary.rs` uses them.

### 2. MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add this method to `impl AdvisoryService`, following the existing method pattern:

```rust
/// Builds a [`VulnerabilitySummary`] from an ingestor `AdvisoryIngestResult`.
///
/// `cves`, `affected_packages` and `severity_counts` are all `Option`s that cross
/// the ingestor module boundary. Each `None` defaults on its own to an empty or
/// zero value, so this method never panics on missing data.
pub fn extract_vulnerability_summary(
    &self,
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();
    let cve_count = u32::try_from(cve_list.len())
        .context("CVE count exceeds u32::MAX")?;

    let affected_package_count = result
        .affected_packages
        .as_ref()
        .map_or(Ok(0), |pkgs| u32::try_from(pkgs.len()))
        .context("affected package count exceeds u32::MAX")?;

    let severity_breakdown: HashMap<String, u32> =
        result.severity_counts.clone().unwrap_or_default();

    Ok(VulnerabilitySummary {
        cve_count,
        cve_list,
        affected_package_count,
        severity_breakdown,
    })
}
```

- `cve_count` is computed from `cve_list.len()` after the default is applied. This guarantees the acceptance criterion "cve_count matches the length of cve_list".
- `u32::try_from(...)` with `.context()` replaces `as u32`, which could silently truncate. This matches the `Result<T, AppError>` + `.context()` convention. If `AppError` has no `anyhow` context conversion, use the equivalent pattern found in siblings.
- The input is taken by reference (`&AdvisoryIngestResult`) so callers keep ownership, and only the needed parts are cloned. If the callers found in Step 4 pass ownership, the signature takes `AdvisoryIngestResult` by value and uses `result.cves.unwrap_or_default()` without the clone.
- No `.unwrap()`, `.expect()` or indexing is used on any of the optional fields.
- Imports to add: `std::collections::HashMap`, `crate::advisory::model::vulnerability_summary::VulnerabilitySummary` (or the re-export path), and `trustify_module_ingestor::service::AdvisoryIngestResult` (the real crate name comes from `Cargo.toml`).
- The method does not touch the database or the `&self` state. It is still placed on `AdvisoryService`, as the task specifies, so it fits the service API and can later use injected config.

### 3. CREATE `tests/api/advisory_summary.rs`

Each test has a `///` doc comment, and the non-trivial ones have `// Given / // When / // Then` comments. Assertions check values, not just lengths.

A helper `fn ingest_result(cves, pkgs, sev) -> AdvisoryIngestResult` builds the fixtures. The service comes from the same test harness that `tests/api/advisory.rs` uses.

| Test | Covers | Key assertions |
|---|---|---|
| `extract_summary_fully_populated` | All fields `Some` (AC1, TR1) | `cve_list == vec!["CVE-2024-0001","CVE-2024-0002"]`, `cve_count == 2`, `affected_package_count == 3`, `severity_breakdown == HashMap{"critical":1,"high":2}` |
| `extract_summary_all_none` | All `None` (AC2, AC3, TR2) | `summary == VulnerabilitySummary::default()`: `cve_count 0`, empty list, `affected_package_count 0`, empty map, no panic |
| `extract_summary_mixed_fields` | Mixed Some/None (TR3) | Several fixtures, e.g. (cves=Some, pkgs=None, sev=Some) and (cves=None, pkgs=Some, sev=None). Checks that each field defaults independently and that `Some` values are kept exactly. Uses `rstest` `#[case]` only if siblings use rstest. Otherwise there is one test per combination, because the assertion structure is the same. |
| `extract_summary_cve_count_matches_list` | AC4, TR4 | For each of None, Some(empty), Some(3 items): `cve_count as usize == cve_list.len()`, plus the concrete expected list |
| `extract_summary_some_empty_collections` | Edge case: `Some(vec![])` / `Some(HashMap::new())` | Same result as `None`: zeroed counts and empty collections |

Run `cargo test -p <fundamental crate>` and the tests crate (the crate name is resolved with `cargo metadata --no-deps`).

## Step 7–8 — Acceptance criteria mapping

| AC | Satisfied by |
|---|---|
| Valid summary from a fully populated result | Method plus `extract_summary_fully_populated` |
| `None` values handled without panic | `unwrap_or_default` / `map_or` guards plus the all-None and mixed tests |
| Summary fields always populated | `VulnerabilitySummary` has no `Option` fields, and its `Default` derive gives zeroed values |
| `cve_count == cve_list.len()` | Count derived from the defaulted list, plus a dedicated test |

## Step 9 — Self-verification

### Scope containment: files outside Files to Modify / Files to Create that may need to change

The new files cannot compile or run without some wiring. Under the skill rules these files are **flagged for user approval**, not silently edited:

1. `modules/fundamental/src/advisory/model/mod.rs`: needs `pub mod vulnerability_summary;`, and possibly `pub use vulnerability_summary::VulnerabilitySummary;`. Without it the new model file is not compiled.
2. `tests/Cargo.toml` (`[[test]]` entries) or the tests crate root: registers `api/advisory_summary.rs` if the test layout requires explicit registration.
3. `modules/fundamental/Cargo.toml`: only needed if the `ingestor` crate is not already a dependency of `fundamental` (see Step 4.7).

Each file would be listed with the reason it changed, and the skill would wait for explicit approval before committing.

### Other checks

- **Untracked file check**: confirm both new files are staged and nothing else is untracked in the touched directories.
- **Sensitive patterns**: none expected.
- **Duplication check**: grep for other per-severity aggregation or CVE-count helpers. Reuse them if found.
- **CI**: run the CONVENTIONS.md commands (fmt, clippy, check). Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p <fundamental crate>` plus the integration tests crate.
- **Data-flow trace**: `IngestorService::ingest_advisory()` produces `AdvisoryIngestResult` (input), `AdvisoryService::extract_vulnerability_summary()` applies the null guards and counts (processing), and the result is a `VulnerabilitySummary` (output). The email digest consumer is not part of this task (it belongs to the parent feature TC-9001). This would be reported as intentionally out of scope.
- **Contract and sibling parity**:
  - No trait is implemented.
  - The method signature follows the sibling `Result<T, AppError>` pattern.
  - No shared database entity is written.
  - No callers exist yet.
- **Dead parameters**: none, since no code is removed.

## Step 10 — Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for advisory digests

Adds AdvisoryService::extract_vulnerability_summary() which converts an
AdvisoryIngestResult into a VulnerabilitySummary with non-optional fields,
defaulting None cves/affected_packages/severity_counts to empty/zero.

Implements TC-9211"
```

- Fork detection: `git remote get-url upstream`.
- PR: `gh pr create --base main`. The body includes `Implements [TC-9211](<webUrl>)`, and `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 — Jira update

- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a change summary, and any deviations (for example, approved out-of-scope `mod.rs` registration). The comment ends with the standard `implement-task` footnote.
- Transition the issue to In Review.

## Risks and open questions to raise with the user

1. **Crate dependency direction**: does `fundamental` already depend on `ingestor`? If not, adding the dependency is out of scope and could create a cycle. The alternative would be to move `AdvisoryIngestResult` to `common`, which is a larger and out-of-scope change. The skill asks the user before proceeding.
2. **Module registration** in `model/mod.rs` and test registration: these are out of scope but required, as flagged above.
3. **Integration test location**: the test cases are pure unit-level transformations, but the task places them in `tests/api/`. The plan keeps the task-specified path, which honors the task scope.
