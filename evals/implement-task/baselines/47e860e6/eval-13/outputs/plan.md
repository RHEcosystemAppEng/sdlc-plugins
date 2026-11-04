# Implementation Plan: TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, path `./`)
**Target Branch**: `main`
**Task branch**: `TC-9211`

---

## Step 0: Validate Project Configuration

From `claude-md-mock.md`, the `# Project Configuration` section has:

- `## Repository Registry`: one entry, `trustify-backend` → `serena_backend` → `./`. Pass.
- `## Jira Configuration`: Project key `TC`, Cloud ID, Feature issue type ID `10142`. Pass. Optional fields also present: Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`.
- `## Code Intelligence`: the tool naming convention `mcp__<serena-instance>__<tool>` is present. Pass. Limitation: rust-analyzer can take 30-60s to index on first use.

Configuration is valid, so execution continues.

## Step 1: Parse Task (simulated `jira.get_issue(TC-9211)`)

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR | not present, so default flow (new branch and new PR) |
| Bookend Type | not present, so a normal implementation task |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | none (service-layer method only, no new endpoint) |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue; if it is set, add `Closes <owner>/<repo>#<n>` to the PR body |

All required sections are present, so there is no reason to stop for clarification.

## Step 1.5: Description integrity (simulated)

I would fetch the comments and look for `[sdlc-workflow] Description digest:`. If no digest comment exists, I would log a warning and continue. If one exists, I would compute the digest with `scripts/sha256-digest.py` and compare. No Jira calls were made in this eval.

## Step 2: Dependencies

"Depends on: None", so there is nothing to verify.

## Step 3: Jira transition (simulated, not executed)

`jira.user_info()` → `jira.edit_issue(TC-9211, assignee=<me>)` → `jira.transition_issue(TC-9211, "In Progress")`.

## Step 4: Understand the Code (planned Serena calls)

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")`: get the `AdvisoryService` structure and its existing method signatures (fetch, list, search) to confirm the `Result<T, AppError>` pattern.
2. `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` in `modules/ingestor/src/service/mod.rs`: confirm the exact field types (`cves: Option<Vec<String>>`, `affected_packages: Option<Vec<AffectedPackage>>`, `severity_counts: Option<HashMap<String, u32>>`). Also confirm whether `AffectedPackage` and the struct are `pub` and re-exported from the ingestor crate root.
3. `mcp__serena_backend__find_symbol("IngestorService/ingest_advisory", include_body=true)`: understand when each field is `None` and whether `Some(vec![])` is also possible. The guards cover both cases.
4. **Dependency check (important):** read `modules/fundamental/Cargo.toml` to see whether the `fundamental` crate already depends on the `ingestor` crate. If `ingestor` already depends on `fundamental`, importing `AdvisoryIngestResult` into `fundamental` would create a crate cycle. If that happens, stop and raise it with the user. Do not silently duplicate the struct.
5. Siblings for convention analysis:
   - `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) and `details.rs`: derive set (`Serialize`, `Deserialize`, `ToSchema`?, `Debug`, `Clone`, `PartialEq`?), doc comment style, field naming.
   - `modules/fundamental/src/sbom/model/summary.rs`: a second model sibling.
   - `modules/fundamental/src/sbom/service/sbom.rs`: a second service sibling, for method shape and `.context()` usage.
   - `tests/api/advisory.rs` and `tests/api/sbom.rs`: test setup, DB fixture helpers, assertion style.
6. `mcp__serena_backend__search_for_pattern("VulnerabilitySummary|vulnerability_summary|severity_breakdown")` across the workspace: symbol deduplication, so I don't redeclare something that already exists.
7. Read `CONVENTIONS.md` at the repo root. Extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`) and any code generation commands (e.g. OpenAPI generation) for Step 9.
8. Documentation files: `README.md`, `docs/architecture.md`, `docs/api.md`. No endpoint is added, so I don't expect API doc changes.

### Expected conventions (to be confirmed by the Serena analysis)

- **Naming**: `snake_case` methods using a `verb_noun` pattern (`extract_vulnerability_summary`); model structs named `<Domain><Kind>`; one model per file, re-exported via `model/mod.rs`.
- **Error handling**: service methods return `Result<T, AppError>`; fallible operations use `.context(...)`.
- **Models**: `#[derive(Debug, Clone, Serialize, Deserialize, ...)]` with `///` doc comments.
- **Tests**: integration tests in `tests/api/` using `assert_eq!`. The skill's guidance on value-based assertions and doc comments overrides sibling patterns.

## Step 5: Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9211
```

## Step 6: Implement Changes

### 6.1 CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Digest of an ingested advisory's vulnerability data, used for email notifications.
///
/// All fields are non-optional: missing upstream data is represented by
/// zero counts and empty collections rather than `None`.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers; always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty if none were reported).
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory (0 if package detail is absent).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty if severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

- `Default` gives the "zeroed summary" for free and documents what "sensible defaults" means.
- The derive list is matched to the `AdvisorySummary` sibling. If siblings derive `utoipa::ToSchema`, add it too.

### 6.2 MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add the import and a new method on `AdvisoryService`:

```rust
use std::collections::HashMap;
use trustify_module_ingestor::service::AdvisoryIngestResult; // exact path confirmed in Step 4
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    /// Builds a [`VulnerabilitySummary`] from an ingestor result for digest emails.
    ///
    /// Every `Option` field on `AdvisoryIngestResult` is treated as possibly
    /// absent: `None` cves → empty list / count 0, `None` affected_packages →
    /// count 0, `None` severity_counts → empty map. Never panics on missing data.
    /// Returns `AppError` only if a collection length exceeds `u32::MAX`.
    pub fn extract_vulnerability_summary(
        &self,
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();
        let cve_count = u32::try_from(cve_list.len())
            .context("CVE count exceeds u32::MAX")?;

        let affected_package_count = u32::try_from(
            result.affected_packages.as_ref().map_or(0, Vec::len),
        )
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
}
```

Design decisions:

- **Signature**: takes `&AdvisoryIngestResult` so callers keep ownership of the ingest result (it may also be logged or persisted). The cost is cloning the CVE list and the severity map, which are small.
- **Return type**: `Result<VulnerabilitySummary, AppError>`, following the service method pattern from the Implementation Notes. The only error path is the checked `usize` → `u32` conversion. I chose a checked conversion over `as u32` because `as` truncates silently, and the conversion never panics either way. If `AppError` lacks a `.context()` path for `TryFromIntError`, map it with `.map_err(|e| AppError::Internal(...))` to match the sibling error constructor.
- **cve_count consistency**: `cve_count` is computed from `cve_list.len()` after defaulting, so the acceptance criterion "cve_count matches the length of the cve_list" holds by construction. There is no second code path that could diverge.
- **No `unwrap()` / `expect()` / indexing** on any upstream field.
- **No `&self` state is used.** Keeping it as a method is what the task asks for ("add method to AdvisoryService") and matches sibling methods. Clippy's `unused_self` is pedantic-only, so it is not triggered by default lints.
- **No async / DB access**: this is a pure transformation, so the method is synchronous.

Full nullable-field analysis: see `null-guards.md`.

### 6.3 CREATE `tests/api/advisory_summary.rs`

All tests get a `///` doc comment and Given/When/Then comments. Assertions are value-based: they compare whole `VulnerabilitySummary` values with `assert_eq!`, not just lengths. A small test helper `fn ingest_result(cves, pkgs, sev) -> AdvisoryIngestResult` builds fixtures.

| Test | Covers |
|---|---|
| `extract_summary_fully_populated` | All fields `Some`: 2 CVEs, 3 packages, `{"critical":1,"high":2}`. Asserts the full expected struct with `assert_eq!`. AC1, TR1 |
| `extract_summary_all_none_returns_zeroed` | `cves=None, affected_packages=None, severity_counts=None`. Asserts `== VulnerabilitySummary::default()`, and that there is no panic. AC2, AC3, TR2 |
| `extract_summary_mixed_fields_default_independently` | Parameterized over the mixed combinations (e.g. `Some/None/Some`, `None/Some/None`, `Some/Some/None`). Each case asserts the full expected struct, so every `None` field defaults independently while the `Some` fields are preserved. TR3 |
| `extract_summary_cve_count_matches_list_len` | Parameterized over `None`, `Some(vec![])`, `Some(1 item)`, `Some(5 items)`. Asserts `summary.cve_count as usize == summary.cve_list.len()` **and** that `cve_list` equals the expected values. AC4, TR4 |
| `extract_summary_empty_some_collections` | `Some(vec![])`, `Some(vec![])`, `Some(HashMap::new())`. Produces the same zeroed result as `None`, which distinguishes "present but empty" from "absent" without any special casing. Edge case. |

Parameterization: use `rstest` only if Step 4 shows the test crate already uses it. Otherwise use a table-driven `for` loop over a `[(input, expected)]` array, with case labels in the assertion messages. That avoids adding a new dev-dependency, which would mean touching an out-of-scope `Cargo.toml`.

Tests that need an `AdvisoryService` instance follow the construction pattern used in `tests/api/advisory.rs` (test DB context).

### 6.4 Documentation impact

There is no endpoint, CLI, or config change, so no doc updates are expected. The `docs/api.md` REST reference is unaffected.

## Step 7: Run tests (simulated)

`cargo test -p <fundamental crate name>` and `cargo test -p <tests crate name>`, with crate names resolved via `cargo metadata --no-deps --format-version 1`.

## Step 8: Acceptance Criteria mapping

| AC | Satisfied by |
|---|---|
| Valid summary from a fully-populated result | 6.2 logic plus `extract_summary_fully_populated` |
| Handles `None` for cves / affected_packages / severity_counts without panicking | `unwrap_or_default()` / `map_or(0, ..)` plus checked conversion; no `unwrap`; all-None and mixed tests |
| Fields are always populated with sensible defaults | `VulnerabilitySummary` has no `Option` fields and derives `Default` |
| `cve_count` matches the length of `cve_list` | Count derived from the defaulted list; dedicated test |

## Step 9: Self-verification

### Scope containment: files that need flagging

The plan touches exactly the three listed files. Wiring them in, however, probably needs edits to files **not** listed in the task. Per the skill rules these are **not** in the implementation plan. They would be flagged for user approval:

1. `modules/fundamental/src/advisory/model/mod.rs`: needs `pub mod vulnerability_summary;` (and possibly `pub use`). Without it the new file is not compiled.
2. `tests/Cargo.toml` or the test harness entry file (e.g. a `[[test]]` entry or `mod advisory_summary;` in the test crate root): may be needed for `tests/api/advisory_summary.rs` to be compiled. This depends on how `tests/api/*.rs` are registered (checked in Step 4).
3. `modules/fundamental/Cargo.toml`: only if `fundamental` doesn't already depend on the ingestor crate. If adding that dependency would create a cycle, stop and ask the user instead.

### Other checks

- **Untracked files**: check `git status --short` before staging.
- **Dead parameters**: none, since nothing is removed.
- **Sensitive patterns**: none expected.
- **Duplication**: grep for existing CVE-count or severity aggregation helpers (e.g. in `AdvisorySummary` construction) and reuse them if found.
- **CI**: run every command from the `CONVENTIONS.md` CI section (fmt, clippy, etc.). Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p` for each crate with modified files.
- **Data-flow trace**: input `IngestorService::ingest_advisory()` → `AdvisoryIngestResult` (Option fields) → processing in `extract_vulnerability_summary()` (guards and defaults) → output `VulnerabilitySummary` (non-optional), consumed by the email digest. The email-sending consumer is out of scope for this task (presumably a later TC-9001 task). It is flagged as an intentionally incomplete downstream stage.
- **Query scope**: not applicable, since there is no DB iteration.
- **Contract and sibling parity**:
  - Contract: no trait is implemented.
  - Sibling parity: the method signature and error type match `AdvisoryService` siblings; the model derives match `AdvisorySummary`.
  - Cross-module entity: no DB writes.
  - Caller-site: consumes the ingestor's public struct read-only, with no mutation.

## Step 10: Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds AdvisoryService::extract_vulnerability_summary(), which converts an
AdvisoryIngestResult (Option fields) into a non-optional VulnerabilitySummary
with zero/empty defaults for missing CVEs, packages, and severity counts.

Implements TC-9211"
```

Then check for a fork (`git remote get-url upstream`) and run `gh pr create --base main ...`. The PR body includes `Implements [TC-9211](https://<site>/browse/TC-9211)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11: Jira update (simulated)

- Set `customfield_10875` to an ADF `inlineCard` containing the PR URL.
- Add a comment with the PR link, a summary of changes, and any deviations (e.g. the out-of-scope `model/mod.rs` registration, if approved). End it with the footnote from `shared/comment-footnote.md` using skill name `implement-task`.
- Transition the issue to **In Review**.
