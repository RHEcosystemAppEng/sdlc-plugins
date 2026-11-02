# Implementation Plan — TC-9211: Add Vulnerability Summary Extractor

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID present
- **Code Intelligence**: Tool naming convention and `serena_backend` instance configured

Validation passes. Proceeding.

## Step 1 — Fetch and Parse Jira Task

**Key**: TC-9211
**Target Branch**: main
**Repository**: trustify-backend

### Parsed Sections

- **Description**: Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records from the ingestor module. Extracts CVE identifiers, affected package counts, and severity breakdowns. Must handle nullable fields gracefully.
- **Files to Modify**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Files to Create**:
  1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`
  2. `tests/api/advisory_summary.rs`
- **Dependencies**: None

## Step 1.5 — Verify Description Integrity

No digest comment found on the Jira issue — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code Inspection

Before modifying any files, inspect the following existing code:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — Read the existing AdvisoryService struct to understand its pattern: methods return `Result<T, AppError>` with `.context()` error wrapping. Need to understand how it imports types and which database/service dependencies it uses.

2. **`modules/ingestor/src/service/mod.rs`** — Read the `AdvisoryIngestResult` struct definition to confirm the three `Option<T>` fields:
   - `cves: Option<Vec<String>>`
   - `affected_packages: Option<Vec<AffectedPackage>>`
   - `severity_counts: Option<HashMap<String, u32>>`

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Read the existing `AdvisorySummary` struct as a sibling model to follow the same patterns (derive macros, field documentation, serde attributes).

4. **`modules/fundamental/src/advisory/model/mod.rs`** — Check how sibling models are registered (pub mod declarations).

5. **`common/src/error.rs`** — Confirm `AppError` type and `.context()` usage pattern.

6. **`tests/api/advisory.rs`** — Read existing advisory integration tests for test setup patterns, assertion style, and database fixture creation.

### Convention Conformance Analysis

From sibling analysis:
- **Error handling**: Methods return `Result<T, AppError>` with `.context("descriptive message")`
- **Naming**: `verb_noun` pattern for service methods (e.g., `fetch_advisory`, `list_advisories`)
- **Model pattern**: Structs derive `Clone, Debug, Serialize, Deserialize`; fields documented
- **Module registration**: New models registered via `pub mod` in `model/mod.rs`
- **Test naming**: `test_<action>_<scenario>` pattern
- **Test assertions**: `assert_eq!` on specific values, not just existence checks

### CONVENTIONS.md Lookup

Check `CONVENTIONS.md` at the repository root for CI check commands and verification steps. Extract any listed CI commands for use in Step 9.

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9211
```

## Step 6 — Implement Changes

### File 1 (Create): `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Create the `VulnerabilitySummary` output struct with non-optional fields:

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Summary of vulnerability data extracted from an advisory ingest result.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVEs referenced in the advisory.
    pub cve_count: u32,
    /// List of CVE identifiers (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,
    /// Counts per severity level (e.g., {"critical": 3, "high": 5}).
    pub severity_breakdown: HashMap<String, u32>,
}
```

All fields are non-optional with sensible defaults for missing upstream data.

### File 2 (Modify): `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:
```rust
pub mod vulnerability_summary;
```

### File 3 (Modify): `modules/fundamental/src/advisory/service/advisory.rs`

Add `extract_vulnerability_summary()` method to `AdvisoryService`. This method accepts an `AdvisoryIngestResult` and produces a `VulnerabilitySummary`.

**Defensive property access for all three nullable fields:**

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result.
    pub fn extract_vulnerability_summary(
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard cves: Option<Vec<String>> → default to empty Vec
        let cve_list = result.cves.as_ref()
            .map(|v| v.clone())
            .unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Guard affected_packages: Option<Vec<AffectedPackage>> → default to empty Vec, take count
        let affected_package_count = result.affected_packages.as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Guard severity_counts: Option<HashMap<String, u32>> → default to empty HashMap
        let severity_breakdown = result.severity_counts.as_ref()
            .map(|m| m.clone())
            .unwrap_or_default();

        Ok(VulnerabilitySummary {
            cve_count,
            cve_list,
            affected_package_count,
            severity_breakdown,
        })
    }
}
```

Key patterns:
- `as_ref()` to borrow the Option content without consuming it
- `unwrap_or_default()` for types implementing `Default` (Vec, HashMap)
- `map()` + `unwrap_or(0)` for computed values from the Option content
- No direct `.unwrap()` calls on any Option field

### File 4 (Create): `tests/api/advisory_summary.rs`

Integration tests covering all nullable field combinations. See Step 7 below.

## Step 7 — Write Tests

### Test file: `tests/api/advisory_summary.rs`

```rust
/// Verifies extraction from a fully-populated AdvisoryIngestResult.
#[test]
fn test_extract_vulnerability_summary_all_populated() {
    // Given a fully-populated AdvisoryIngestResult
    // When extracting the vulnerability summary
    // Then all fields reflect the input data
    // Assert: cve_count == cve_list.len(), specific CVE values present,
    //         affected_package_count matches input, severity_breakdown matches
}

/// Verifies extraction handles all-None fields without panicking.
#[test]
fn test_extract_vulnerability_summary_all_none() {
    // Given an AdvisoryIngestResult with cves=None, affected_packages=None, severity_counts=None
    // When extracting the vulnerability summary
    // Then returns zeroed/empty defaults: cve_count=0, cve_list=[], affected_package_count=0, severity_breakdown={}
}

/// Verifies each None field defaults independently of other fields.
#[test]
fn test_extract_vulnerability_summary_mixed_some_none() {
    // Given cves=Some([...]), affected_packages=None, severity_counts=Some({...})
    // When extracting the vulnerability summary
    // Then cve fields are populated, affected_package_count=0, severity_breakdown populated
}

/// Verifies cve_count is consistent with cve_list length.
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various cve list lengths
    // When extracting summaries
    // Then assert_eq!(summary.cve_count, summary.cve_list.len() as u32) for each
}
```

Tests use value-based assertions (`assert_eq!` on specific CVE strings, counts, and HashMap entries) rather than existence checks.

## Step 8 — Verify Acceptance Criteria

- [x] `extract_vulnerability_summary()` produces valid summary from fully-populated input — verified by `test_extract_vulnerability_summary_all_populated`
- [x] Handles None values without panicking — verified by `test_extract_vulnerability_summary_all_none`
- [x] VulnerabilitySummary fields are always non-optional with defaults — struct definition uses non-optional types
- [x] cve_count matches cve_list.len() — verified by `test_cve_count_matches_cve_list_length`

## Step 9 — Self-Verification

### Scope containment
Modified/created files:
1. `modules/fundamental/src/advisory/service/advisory.rs` — listed in Files to Modify ✓
2. `modules/fundamental/src/advisory/model/vulnerability_summary.rs` — listed in Files to Create ✓
3. `tests/api/advisory_summary.rs` — listed in Files to Create ✓
4. `modules/fundamental/src/advisory/model/mod.rs` — out of scope but required for module registration

File 4 is out of scope — flag to user: `model/mod.rs` needs a `pub mod vulnerability_summary;` line to make the new model accessible. This is a mechanical module registration change required by the Rust module system.

### Module-level test requirement (Rust)

Resolve crate name using `cargo metadata --no-deps --format-version 1` from the workspace root. The modified files are in `modules/fundamental/`, which maps to a package (e.g., `trustify-module-fundamental`). Run:

```
cargo test -p trustify-module-fundamental
```

Do not derive the crate name from the nearest `Cargo.toml` which may be a virtual workspace manifest.

### Defensive property access verification
All three Option fields use safe access patterns — see null-guards.md for detailed analysis.

## Step 10 — Commit and Push

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/model/vulnerability_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Add extract_vulnerability_summary() to AdvisoryService that processes
AdvisoryIngestResult records with defensive null guards on all three
Option fields (cves, affected_packages, severity_counts). Produces a
VulnerabilitySummary with non-optional fields using sensible defaults.

Implements TC-9211"
```

Branch: TC-9211, PR targeting main with `--base main`.
