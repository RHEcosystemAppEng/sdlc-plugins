# Implementation Plan — TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, Path: `./`)
**Target Branch**: `main`
**Task branch**: `TC-9211`
**Dependencies**: None (Step 2 skipped)
**Target PR / Bookend Type**: none, so this uses the default flow

> Eval mode: no repository files were changed and no external tools (Jira, git, Serena,
> gh) were called. Each step below says what would happen in a live run.

---

## Step 0: Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) contains:
- `## Repository Registry`: 1 entry (trustify-backend → `serena_backend`, `./`)
- `## Jira Configuration`: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- `## Code Intelligence`: tool naming convention `mcp__<serena-instance>__<tool>`, plus a rust-analyzer indexing limitation

Result: **PASS**. Execution continues.

## Step 1: Task parsing

Every required section is present: Repository, Target Branch, Description, Files to Modify,
Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies.
API Changes is absent. That is acceptable because this task adds no endpoint.
- GitHub Issue field (`customfield_10747`): would be read from the issue. If it holds a URL,
  `Closes <owner>/<repo>#<n>` would go in the PR body. The mock has no value, so this is skipped.
- `webUrl` would be captured for the PR "Implements" link.

## Step 1.5: Description digest

Would call `jira.get_issue_comments(TC-9211)` and look for `[sdlc-workflow] Description digest:`.
Then compute the digest with `python3 scripts/sha256-digest.py` and compare the two.
The task is synthetic, so no digest is available. This would be logged as a warning and the run would continue.

## Step 3: Jira transition (simulated)

`jira.user_info()` → `jira.edit_issue(TC-9211, assignee=<me>)` → `jira.transition_issue → In Progress`.

## Step 4: Understand the code (planned Serena calls)

| Purpose | Call |
|---|---|
| Structure of the file to modify | `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` |
| Existing method pattern | `mcp__serena_backend__find_symbol("AdvisoryService", include_body=true, depth=1)` |
| Upstream type definition | `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs` |
| Upstream element type | `mcp__serena_backend__find_symbol("AffectedPackage", include_body=true)` |
| Producer behaviour | `mcp__serena_backend__find_symbol("IngestorService/ingest_advisory", include_body=true)` |
| Sibling model conventions | `get_symbols_overview` on `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs` |
| Model module registration | `get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")` |
| Sibling test conventions | `get_symbols_overview("tests/api/advisory.rs")`, `tests/api/sbom.rs` |
| Crate dependency check | Read `modules/fundamental/Cargo.toml` to confirm a `trustify-module-ingestor` (or equivalent) dependency |
| Symbol dedup | `search_for_pattern("VulnerabilitySummary\|vulnerability_summary\|severity_breakdown")` across the workspace |
| Repo conventions | Read `CONVENTIONS.md` at repo root and extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) |
| Docs | `README.md`, `docs/api.md`, `docs/architecture.md`. No public API changes, so no doc updates are expected |

### Conventions found (from repo-backend.md; a live run would confirm them in code)
- **Module layout**: `model/ + service/ + endpoints/` per domain. The new struct belongs in `advisory/model/`.
- **Error handling**: service methods return `Result<T, AppError>` (`common/src/error.rs`) and use `.context()` wrapping.
- **Model structs**: derive `Serialize, Deserialize, Debug, Clone, PartialEq` (and `utoipa::ToSchema` if siblings derive it). Siblings are the reference.
- **Tests**: integration tests live in `tests/api/` and assert with `assert_eq!`.
- **Naming**: `snake_case` `verb_noun` methods (`fetch`, `list`, `search`). `extract_vulnerability_summary` fits this pattern.

### Cross-crate dependency (Reuse over duplication)
`AdvisoryIngestResult` lives in the `ingestor` crate and is consumed in `fundamental`.
- If `fundamental/Cargo.toml` already depends on `ingestor`, import with `use trustify_module_ingestor::service::{AdvisoryIngestResult, AffectedPackage};`. If the type is not `pub`, make it `pub`.
- If no dependency exists, adding one means editing `modules/fundamental/Cargo.toml`, which is **outside the declared scope**. I would **flag this to the user** (Step 9 scope containment) rather than change it silently. I would also check for a reverse dependency (ingestor → fundamental), which would create a cycle. If that exists, the alternative is to accept the three `Option` fields, or a small trait, rather than the concrete type. I would recommend one approach and wait for the user's answer.

---

## Step 5: Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6: Changes per file

### 1. CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Digest of an ingested advisory's vulnerability data, used to build email notifications.
///
/// All fields are non-optional. Missing upstream data is represented by
/// empty collections and zero counts, so consumers never need to handle `None`.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers; always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty if none).
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory (0 if unknown).
    pub affected_package_count: u32,
    /// Count of findings per severity level, e.g. `"critical" -> 2` (empty if unknown).
    pub severity_breakdown: HashMap<String, u32>,
}
```

- `#[derive(Default)]` gives the zeroed summary for free. The all-`None` case equals `VulnerabilitySummary::default()`, which keeps both the implementation and the tests simple.
- Derives are matched to sibling `summary.rs`. If siblings also derive `utoipa::ToSchema`, add it.

### 2. MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to the `impl AdvisoryService` block using Serena `insert_after_symbol`, placed after the last existing method:

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;
use trustify_module_ingestor::service::AdvisoryIngestResult;

impl AdvisoryService {
    // ... existing methods ...

    /// Builds a [`VulnerabilitySummary`] from an ingestor result for digest emails.
    ///
    /// Every aggregate field on `AdvisoryIngestResult` is optional. A `None` value
    /// becomes an empty collection or a zero count, so the method never panics on
    /// missing data. `cve_count` is always derived from the final `cve_list`.
    pub fn extract_vulnerability_summary(
        &self,
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard: cves may be None -> empty list
        let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();

        // Guard: affected_packages may be None -> 0; only the length is read
        let affected_package_count = result
            .affected_packages
            .as_ref()
            .map_or(0, Vec::len);

        // Guard: severity_counts may be None -> empty map
        let severity_breakdown = result.severity_counts.clone().unwrap_or_default();

        Ok(VulnerabilitySummary {
            cve_count: saturating_u32(cve_list.len()),
            cve_list,
            affected_package_count: saturating_u32(affected_package_count),
            severity_breakdown,
        })
    }
}

/// Converts a collection length to `u32`, clamping at `u32::MAX` instead of truncating.
fn saturating_u32(len: usize) -> u32 {
    u32::try_from(len).unwrap_or(u32::MAX)
}
```

Notes:
- Signature follows the `Result<T, AppError>` service convention, as the Implementation Notes require. The current body cannot fail. Keeping the `Result` matches the sibling API and leaves room for future validation.
- The method borrows `&AdvisoryIngestResult`, so callers keep ownership. `.clone()` is applied only to the inner `Option` value. If callers can give up ownership, an owned `AdvisoryIngestResult` parameter would remove the clones. I would check `find_referencing_symbols` on `ingest_advisory` to choose. Borrowing is the default.
- The method does not use `&self`. It stays on `AdvisoryService` because the task names that location. If clippy (`unused_self`, pedantic) is enabled in CONVENTIONS.md CI checks, I would make it an associated function (`fn extract_vulnerability_summary(result: &...)`) and keep it on the impl.
- `saturating_u32`: before declaring it, search the workspace for an existing length/u32 conversion helper and reuse one if found (symbol deduplication).
- See `null-guards.md` for the full guard analysis.

### 3. Module registration (out of scope, flagged)

The new struct is unreachable unless `modules/fundamental/src/advisory/model/mod.rs` declares it:
```rust
pub mod vulnerability_summary;
```
This file is **not** in Files to Modify or Files to Create. It is a one-line change required for the code to compile, but under the scope rules I would **not change it silently**. In Step 9 scope containment I would list it, explain that the new module needs it to compile, and ask the user to approve.

The same applies to:
- **Test target registration**: depending on how `tests/Cargo.toml` and the test harness are set up, `tests/api/advisory_summary.rs` may need a `mod advisory_summary;` line or a `[[test]]` entry. I would check how `tests/api/advisory.rs` is wired. If an existing file must change, I would flag it for approval.
- **`modules/fundamental/Cargo.toml`**: only if the ingestor dependency is missing (see above).

### 4. CREATE `tests/api/advisory_summary.rs`

The tests follow sibling conventions in `tests/api/advisory.rs` (setup helpers, `assert_eq!`). The method is a pure function, so the tests need no HTTP or DB round-trip, but they live in `tests/api/` as specified. Each test has a `///` doc comment and given/when/then sections, and asserts on **values**, not only lengths.

```rust
/// Builds an AdvisoryIngestResult with the given optional aggregates (other fields default).
fn ingest_result(
    cves: Option<Vec<String>>,
    affected_packages: Option<Vec<AffectedPackage>>,
    severity_counts: Option<HashMap<String, u32>>,
) -> AdvisoryIngestResult { /* ..Default::default() or sibling fixture */ }

/// Verifies a fully-populated result maps every field into the summary.
#[test]
fn extract_summary_fully_populated() {
    // Given an ingest result with 2 CVEs, 3 packages and severity counts
    // When extracting the summary
    // Then each field matches exactly
    assert_eq!(summary, VulnerabilitySummary {
        cve_count: 2,
        cve_list: vec!["CVE-2024-0001".into(), "CVE-2024-0002".into()],
        affected_package_count: 3,
        severity_breakdown: HashMap::from([("critical".into(), 1), ("high".into(), 2)]),
    });
}

/// Verifies all-None aggregates yield a zeroed summary without panicking.
#[test]
fn extract_summary_all_none_returns_zeroed() {
    // Given cves=None, affected_packages=None, severity_counts=None
    // When extracting
    // Then the summary equals VulnerabilitySummary::default()
    assert_eq!(summary, VulnerabilitySummary::default());
}

/// Verifies each None field defaults independently when mixed with Some fields.
// rstest cases (only if the project already uses rstest, otherwise three separate tests):
//   cves only       -> cve_list populated, affected_package_count 0, severity_breakdown empty
//   packages only   -> cve_list empty, cve_count 0, affected_package_count N, breakdown empty
//   severity only   -> cve_list empty, counts 0, breakdown populated
// Each case asserts on the full expected VulnerabilitySummary.

/// Verifies cve_count always equals cve_list.len(), including empty Some(vec![]) and None.
#[test]
fn extract_summary_cve_count_matches_list() { /* cases: None, Some(vec![]), Some(1), Some(5) */ }
```

The mixed Some/None cases share one setup→act→assert algorithm with different data, so per the Meszaros heuristic they are candidates for `rstest`. I would use `rstest` only if `tests/Cargo.toml` or sibling tests already use it. Otherwise I would write separate test functions, because adding a dependency would be out of scope.

Extra edge cases inside the tests above: `Some(vec![])` versus `None` (both give 0 and empty), and an empty `Some(HashMap::new())`.

## Step 7: Running tests (simulated)

`cargo test -p trustify-tests` (or the package that owns `tests/api`) and `cargo test -p trustify-module-fundamental`. The real crate names would come from `cargo metadata --no-deps --format-version 1`.

## Step 8: Acceptance criteria mapping

| Criterion | Where it is satisfied |
|---|---|
| Valid summary from a fully-populated result | `extract_vulnerability_summary` + `extract_summary_fully_populated` |
| Handles None for cves / affected_packages / severity_counts without panic | `unwrap_or_default` / `map_or` guards with no `unwrap()`/`expect()`; all-None and mixed tests |
| Summary fields always populated with sensible defaults | Non-`Option` fields on `VulnerabilitySummary`, `#[derive(Default)]` |
| cve_count matches cve_list length | `cve_count` computed from the final `cve_list.len()`; dedicated test |

## Step 9: Self-verification plan

- **Scope containment**: expected diff is `advisory/service/advisory.rs` (M), `advisory/model/vulnerability_summary.rs` (A), `tests/api/advisory_summary.rs` (A). Out-of-scope files that need user approval: `advisory/model/mod.rs` (module declaration), and possibly the test harness registration and `fundamental/Cargo.toml`.
- **Sensitive patterns**: none expected.
- **Duplication**: grep for existing severity aggregation (e.g. in `AdvisorySummary`'s severity field) and for any helper that already flattens `AdvisoryIngestResult`.
- **CI checks**: run every command from CONVENTIONS.md (fmt, clippy, check, test). Stop immediately on any non-zero exit.
- **Rust module tests**: `cargo test -p <fundamental crate>` and the tests crate.
- **Data-flow trace**: `IngestorService::ingest_advisory()` → `AdvisoryIngestResult` (Option fields) → `AdvisoryService::extract_vulnerability_summary()` (guards and defaults) → `VulnerabilitySummary` (non-optional) → email digest consumer. The consumer and sender are **not** part of this task, so the output stage stops at the returned struct. This is intentional and in scope; I would record it for the user.
- **Contract & sibling parity**: no trait is implemented. The method signature matches sibling `Result<T, AppError>` methods. No shared DB entity is written. There are no existing callers, since this is a new method.

## Step 10: Commit (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds VulnerabilitySummary and AdvisoryService::extract_vulnerability_summary(),
which turns an ingestor AdvisoryIngestResult into a non-optional digest.
None values for cves, affected_packages and severity_counts become empty
collections or zero counts.

Implements TC-9211"
```
`gh pr create --base main`, body includes `Implements [TC-9211](<webUrl>)`. Run fork detection first.

## Step 11: Jira (simulated)

Set `customfield_10875` to the PR URL (ADF inlineCard). Add a comment with the PR link, a change summary, and any deviations (e.g. the approved `model/mod.rs` registration), ending with the implement-task footnote. Then `transition_issue → In Review`.
