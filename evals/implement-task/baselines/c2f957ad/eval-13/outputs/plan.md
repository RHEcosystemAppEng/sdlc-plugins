# Implementation Plan — TC-9211

**Summary**: Add vulnerability summary extractor for advisory digest emails
**Repository**: trustify-backend (Serena instance: `serena_backend`, rust-analyzer)
**Target Branch**: `main`
**Branch to create**: `TC-9211` (Step 5 default flow — no Target PR, no Bookend Type)

---

## Step 0 — Project Configuration validation

The mock CLAUDE.md contains all required sections under `# Project Configuration`:

| Section | Status |
|---|---|
| Repository Registry | Present — `trustify-backend`, Serena `serena_backend`, path `./` |
| Jira Configuration | Present — Project key `TC`, Cloud ID, Feature issue type ID `10142` |
| Code Intelligence | Present — `mcp__<serena-instance>__<tool>` naming convention |

Validation passes; execution continues.

## Step 1 — Task parsing

All required sections are present (Repository, Target Branch, Description, Files to Modify,
Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies).
No Target PR, no Review Context, no Bookend Type. GitHub Issue custom field
(`customfield_10747`) would be read from the issue; if empty, skipped silently.

## Step 1.5 / 2 / 3 — Integrity, dependencies, Jira transition (simulated)

- Digest comment would be fetched and compared (`[sdlc-workflow] Description digest:`).
  Not executed (no external calls in this eval).
- Dependencies: "None" — nothing to verify.
- Would assign TC-9211 to the current user and transition to **In Progress** (not executed).

## Step 4 — Code understanding (what I would inspect with `serena_backend`)

1. `get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see
   `AdvisoryService` and its existing method signatures (`fetch`, `list`, `search`).
2. `find_symbol("AdvisoryIngestResult", include_body=true)` in
   `modules/ingestor/src/service/mod.rs` to confirm the exact field types
   (`cves: Option<Vec<String>>`, `affected_packages: Option<Vec<AffectedPackage>>`,
   `severity_counts: Option<HashMap<String, u32>>`) and visibility (`pub` struct / `pub` fields).
3. `find_symbol("AffectedPackage")` — only its count is needed; no nested fields are read.
4. **Dependency check (reuse over duplication)**: read `modules/fundamental/Cargo.toml` to
   confirm whether `fundamental` already depends on the `ingestor` crate.
   - If yes: import `AdvisoryIngestResult` directly — do NOT redefine it.
   - If no, and `ingestor` depends on `fundamental` (would create a cycle): stop and raise
     this with the user — the extractor's input type cannot be imported without a
     dependency change outside the task scope.
5. **Symbol deduplication**: `search_for_pattern` for `VulnerabilitySummary`,
   `vulnerability_summary`, `severity_breakdown`, `cve_count` across the workspace to make
   sure no equivalent struct/helper already exists (e.g. in `advisory/model/summary.rs`,
   which already carries a severity field).
6. **Sibling conventions** — `get_symbols_overview` on:
   - `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`
     (derive set — likely `Serialize, Deserialize, Debug, Clone, PartialEq, utoipa::ToSchema`; doc comments; field naming)
   - `sbom/service/sbom.rs` (method shape, `Result<T, AppError>`, `.context()` usage)
   - `tests/api/advisory.rs`, `tests/api/sbom.rs` (test setup/context, assertion style)
7. **CONVENTIONS.md** at the repo root exists per repo-backend.md — read it, follow naming /
   layout rules and extract CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) for Step 9.
8. **Docs**: `README.md`, `docs/api.md`, `docs/architecture.md` — this task adds no endpoint
   and no config, so no doc update is expected; recorded for Step 9 currency check.

### Discovered conventions (expected, to be confirmed in Step 4)

- **Error handling**: service methods return `Result<T, AppError>` (`common/src/error.rs`), wrap failures with `.context()`.
- **Module layout**: `model/` + `service/` + `endpoints/`; each model type in its own file, re-exported via `model/mod.rs`.
- **Naming**: `snake_case` methods in `verb_noun` form (`extract_vulnerability_summary`), `PascalCase` structs.
- **Tests**: integration tests in `tests/api/`, `assert_eq!`-based assertions.
- **Skill overrides**: every test gets a `///` doc comment and Given/When/Then comments; value-based assertions instead of length-only checks.

---

## Step 6 — Changes

### 1. CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Digest-ready summary of an ingested advisory, used for email notifications.
///
/// All fields are non-optional: missing upstream data is represented by
/// zero counts and empty collections rather than `None`.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize /*, utoipa::ToSchema if siblings use it */)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers; always equal to `cve_list.len()`.
    pub cve_count: u32,
    /// CVE identifiers referenced by the advisory (empty when none).
    pub cve_list: Vec<String>,
    /// Number of affected packages (0 when package-level detail is absent).
    pub affected_package_count: u32,
    /// Count of findings per severity level (empty when severity metadata is absent).
    pub severity_breakdown: HashMap<String, u32>,
}
```

Derive list will be aligned with sibling `summary.rs`. `Default` is derived so that the
all-`None` case maps naturally to `VulnerabilitySummary::default()`.

### 2. MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add a method to `AdvisoryService`, following the existing `Result<T, AppError>` pattern:

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;
use trustify_module_ingestor::service::AdvisoryIngestResult; // exact path confirmed in Step 4

impl AdvisoryService {
    /// Builds a [`VulnerabilitySummary`] from an ingestor result.
    ///
    /// Every aggregate field of `AdvisoryIngestResult` is optional; `None` values are
    /// mapped to empty collections / zero counts so this never panics on partial data.
    pub fn extract_vulnerability_summary(
        &self,
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // cves: Option<Vec<String>> -> empty Vec when None
        let cve_list: Vec<String> = result.cves.as_deref().map(<[String]>::to_vec).unwrap_or_default();

        // affected_packages: Option<Vec<AffectedPackage>> -> 0 when None
        let affected_package_count =
            to_u32(result.affected_packages.as_ref().map_or(0, Vec::len));

        // severity_counts: Option<HashMap<String, u32>> -> empty map when None
        let severity_breakdown = result.severity_counts.clone().unwrap_or_default();

        Ok(VulnerabilitySummary {
            // derived from cve_list so the invariant cve_count == cve_list.len() always holds
            cve_count: to_u32(cve_list.len()),
            cve_list,
            affected_package_count,
            severity_breakdown,
        })
    }
}

/// Saturating usize -> u32 conversion (avoids `as` truncation and panics).
fn to_u32(n: usize) -> u32 {
    u32::try_from(n).unwrap_or(u32::MAX)
}
```

Notes:
- Takes `&AdvisoryIngestResult` (borrow) so callers can still use the result after
  extraction; the cost is a clone of the CVE list and severity map. If Step 4 shows callers
  always hand over ownership, an owned variant (`result.cves.unwrap_or_default()`) avoids the clone.
- No DB access is needed, so `&self` is unused beyond namespacing; kept on `AdvisoryService`
  because the task explicitly says "add method to AdvisoryService".
- Returns `Result` for consistency with sibling methods even though the current body cannot
  fail; no `.unwrap()`/`.expect()`/indexing is used anywhere.
- Before writing `to_u32`, grep `common/` for an existing saturating-conversion helper and
  reuse it if present (symbol deduplication). If the saturating behaviour is considered
  overkill, `cve_count` stays consistent with `cve_list.len()` for any realistic list.

### 3. CREATE `tests/api/advisory_summary.rs`

Integration tests following `tests/api/advisory.rs` setup (test context / service construction).
Every test gets a `///` doc comment and Given/When/Then sections; assertions compare full values.

| Test | Input | Expected (value-based) |
|---|---|---|
| `extract_summary_fully_populated` | `cves=Some(["CVE-2024-0001","CVE-2024-0002"])`, `affected_packages=Some([pkgA,pkgB,pkgC])`, `severity_counts=Some({"critical":1,"high":2})` | `assert_eq!(summary, VulnerabilitySummary { cve_count: 2, cve_list: vec![...], affected_package_count: 3, severity_breakdown: {...} })` |
| `extract_summary_all_none_returns_zeroed` | all three `None` | `assert_eq!(summary, VulnerabilitySummary::default())` plus explicit field checks (`cve_count == 0`, `cve_list.is_empty()`, etc.) |
| `extract_summary_mixed_fields_default_independently` | three cases: only `cves` Some; only `affected_packages` Some; only `severity_counts` Some | each populated field carries its value, each `None` field is its default |
| `extract_summary_cve_count_matches_cve_list` | `Some(vec![])`, `Some([1 item])`, `Some([5 items])`, `None` | `assert_eq!(summary.cve_count as usize, summary.cve_list.len())` and `assert_eq!(summary.cve_list, expected_list)` |

Parameterization: the mixed case and the cve_count consistency case share the same
setup/action/assertion structure with different data, so they are candidates for `rstest`.
I would only use `rstest` if Step 4 shows it is already a dev-dependency / used in sibling
tests; otherwise use a table-driven loop over a `Vec<(input, expected)>` inside one test, or
separate tests, matching the existing project style.

A small helper `fn ingest_result(cves, pkgs, severity) -> AdvisoryIngestResult` will build
fixtures (using `..Default::default()` if the struct implements `Default`, otherwise filling
the remaining fields explicitly).

---

## Out-of-scope files flagged (Step 9 scope containment)

These are NOT in Files to Modify / Files to Create, but the change will not compile or the
tests will not run without them. Under the skill rules I would not edit them silently; I
would list them and ask the user for approval:

1. `modules/fundamental/src/advisory/model/mod.rs` — needs `pub mod vulnerability_summary;`
   (and possibly `pub use`) so the new struct is reachable.
2. `tests/Cargo.toml` (or a test harness `main.rs`/`mod.rs` in `tests/api/`) — the new test
   file may need a `[[test]]` entry or `mod advisory_summary;` depending on how existing
   test files are registered.
3. `modules/fundamental/Cargo.toml` — only if `fundamental` does not already depend on the
   `ingestor` crate (needed to import `AdvisoryIngestResult`). If adding it would create a
   dependency cycle, stop and consult the user.

## Steps 7–9 — Verification

- Run CI commands extracted from `CONVENTIONS.md` (hard stop on any non-zero exit).
- Rust module-level test requirement: resolve crate names via
  `cargo metadata --no-deps --format-version 1` and run `cargo test -p <fundamental-crate>`
  and `cargo test -p <tests-crate>` (or `cargo nextest run -p ...`).
- Acceptance criteria mapping:
  - Fully populated → valid summary: test 1.
  - `None` for each field without panic: tests 2 and 3; no `unwrap`/`expect`/indexing in code.
  - Non-optional fields with defaults: struct has no `Option` fields; `Default` derived.
  - `cve_count == cve_list.len()`: `cve_count` is derived from `cve_list.len()`; test 4.
- Data-flow trace: `IngestorService::ingest_advisory()` → `AdvisoryIngestResult` (input) →
  `extract_vulnerability_summary()` normalizes `Option`s (processing) → `VulnerabilitySummary`
  (output, `Serialize` for the email digest). The email-sending consumer is out of scope
  (handled elsewhere under TC-9001) — I would note this as intentionally incomplete.
- Contract & sibling parity: no trait implemented; derives and doc style match sibling
  `summary.rs`; error type matches sibling service methods; no shared DB entity is written;
  no existing callers (new method).
- Sensitive-pattern check, duplication check, untracked-file check as described in the skill.

## Steps 10–11 — Commit, PR, Jira (simulated, not executed)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(advisory): add vulnerability summary extractor for digest emails

Adds AdvisoryService::extract_vulnerability_summary() which turns an
AdvisoryIngestResult into a VulnerabilitySummary, mapping None fields
to zero counts and empty collections.

Implements TC-9211"
```

- `gh pr create --base main` (or fork form if an `upstream` remote exists); body contains
  `Implements [TC-9211](<webUrl>)` and a `Closes owner/repo#N` line if the GitHub Issue field is set.
- Set `customfield_10875` to the PR URL (ADF inlineCard), add a Jira comment (PR link, summary,
  deviations including any approved out-of-scope files) ending with the skill footnote, and transition to **In Review**.
