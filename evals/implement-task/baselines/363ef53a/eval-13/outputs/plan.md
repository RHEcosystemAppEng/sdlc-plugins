# Implementation Plan: TC-9211 -- Vulnerability Summary Extractor

## Overview

Add a vulnerability summary extractor that consumes `AdvisoryIngestResult` records from the ingestor module and produces a `VulnerabilitySummary` suitable for advisory digest emails. The core challenge is that `AdvisoryIngestResult` uses `Option<T>` for three aggregate fields, so every access must be guarded against `None`.

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose:** Define the `VulnerabilitySummary` output struct with non-optional fields and sensible defaults.

**Changes:**
- Define a new public struct `VulnerabilitySummary` with the following fields:
  - `cve_count: u32` -- total number of CVE identifiers
  - `cve_list: Vec<String>` -- the CVE identifier strings
  - `affected_package_count: u32` -- number of affected packages
  - `severity_breakdown: HashMap<String, u32>` -- counts keyed by severity level
- Derive `Debug`, `Clone`, `Serialize`, `Deserialize` to match sibling model structs (`AdvisorySummary`, `AdvisoryDetails`).
- Implement `Default` for `VulnerabilitySummary` so all fields zero/empty by default.
- Add a doc comment on the struct explaining its purpose: output model for the vulnerability summary extractor, with all fields guaranteed non-optional.

**Convention conformance:** Follows the `model/` pattern established by `summary.rs` and `details.rs` in the same directory.

### 2. `tests/api/advisory_summary.rs`

**Purpose:** Integration tests for the `extract_vulnerability_summary()` method.

**Changes:**
- Add test: `test_extract_vulnerability_summary_all_populated` -- verifies extraction from a fully-populated `AdvisoryIngestResult` (all fields `Some`). Asserts on specific CVE values, package count, and severity breakdown entries.
- Add test: `test_extract_vulnerability_summary_all_none` -- verifies extraction when `cves = None`, `affected_packages = None`, `severity_counts = None`. Asserts `cve_count == 0`, `cve_list` is empty, `affected_package_count == 0`, `severity_breakdown` is empty. This is the critical null-guard validation test.
- Add test: `test_extract_vulnerability_summary_mixed_some_none` -- verifies that each `None` field defaults independently while `Some` fields are extracted correctly. Tests multiple combinations:
  - `cves = Some`, `affected_packages = None`, `severity_counts = None`
  - `cves = None`, `affected_packages = Some`, `severity_counts = None`
  - `cves = None`, `affected_packages = None`, `severity_counts = Some`
- Add test: `test_cve_count_matches_cve_list_length` -- verifies `cve_count` is always consistent with `cve_list.len()`.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- Follow the existing test pattern: `assert_eq!` assertions with specific values, not just `.is_empty()` or `.len()`.

## Files to Modify

### 3. `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose:** Add the `extract_vulnerability_summary()` method to `AdvisoryService`.

**Changes:**
- Add a new public method `extract_vulnerability_summary(&self, ingest_result: &AdvisoryIngestResult) -> Result<VulnerabilitySummary, AppError>` to `AdvisoryService`.
- Import `VulnerabilitySummary` from the new model module.
- Import `AdvisoryIngestResult` from `modules/ingestor/src/service/mod.rs` (verify the ingestor crate is already a dependency of the fundamental crate in `Cargo.toml`).

**Implementation of `extract_vulnerability_summary()`:**

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Handles nullable fields from AdvisoryIngestResult defensively --
/// the ingestor module's schema uses Option<T> for aggregate data,
/// so any field may be None.
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Guard cves: Option<Vec<String>> -> default to empty Vec
    let cve_list = ingest_result
        .cves
        .as_ref()
        .cloned()
        .unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Guard affected_packages: Option<Vec<AffectedPackage>> -> default to empty Vec
    let affected_package_count = ingest_result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Guard severity_counts: Option<HashMap<String, u32>> -> default to empty HashMap
    let severity_breakdown = ingest_result
        .severity_counts
        .as_ref()
        .cloned()
        .unwrap_or_default();

    Ok(VulnerabilitySummary {
        cve_count,
        cve_list,
        affected_package_count,
        severity_breakdown,
    })
}
```

### 4. `modules/fundamental/src/advisory/model/mod.rs`

**Purpose:** Register the new `vulnerability_summary` submodule.

**Changes:**
- Add `pub mod vulnerability_summary;` to the module declarations.
- Add `pub use vulnerability_summary::VulnerabilitySummary;` for convenient re-export.

This is an out-of-scope file (not listed in Files to Modify) -- would flag for user approval in Step 9's scope containment check, but it is required for the new model file to be reachable.

## Guard Pattern Summary

| Field | Type | Guard Pattern | Result |
|---|---|---|---|
| `cves` | `Option<Vec<String>>` | `.as_ref().cloned().unwrap_or_default()` | `Vec<String>` (empty if None) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|pkgs\| pkgs.len() as u32).unwrap_or(0)` | `u32` (0 if None) |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.as_ref().cloned().unwrap_or_default()` | `HashMap<String, u32>` (empty if None) |

No field is accessed with `.unwrap()`, `.len()` on Option, `.join()` on Option, or iteration on Option without unwrapping safely first.

## Data-Flow Trace

1. **Input:** `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()` in `modules/ingestor/src/service/mod.rs`.
2. **Processing:** `AdvisoryService::extract_vulnerability_summary()` reads the three nullable fields, applies null guards, and constructs a `VulnerabilitySummary` with non-optional fields.
3. **Output:** `VulnerabilitySummary` returned to the caller for use in email digest rendering.

The data crosses a module boundary (ingestor -> fundamental), which is why defensive access is critical.

## Acceptance Criteria Verification

- [x] `extract_vulnerability_summary()` produces a valid summary from a fully-populated AdvisoryIngestResult -- covered by `test_extract_vulnerability_summary_all_populated`
- [x] Handles None values for all three fields without panicking -- covered by `test_extract_vulnerability_summary_all_none`
- [x] VulnerabilitySummary fields are always populated with sensible defaults -- enforced by guard patterns and `Default` impl
- [x] cve_count matches the length of cve_list -- covered by `test_cve_count_matches_cve_list_length`
