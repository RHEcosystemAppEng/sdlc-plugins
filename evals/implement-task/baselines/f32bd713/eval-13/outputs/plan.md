# Implementation Plan: TC-9211 -- Vulnerability Summary Extractor

## Overview

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records
(produced by the ingestor module) and outputs a `VulnerabilitySummary` struct with
non-optional, safely-defaulted fields suitable for email digest notifications.

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Create the `VulnerabilitySummary` output struct with fully non-optional fields:

```rust
use std::collections::HashMap;

/// Summary of vulnerability data extracted from an advisory ingest result,
/// intended for use in email digest notifications.
///
/// All fields are non-optional with sensible defaults — callers do not need
/// to handle missing data.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of affected packages referenced by the advisory.
    pub affected_package_count: u32,
    /// Breakdown of vulnerability counts by severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}
```

Rationale: deriving `Default` ensures `VulnerabilitySummary::default()` produces a
zeroed/empty summary. Deriving `PartialEq` and `Eq` enables assertion-based testing.

### 2. `modules/fundamental/src/advisory/model/mod.rs` (modify)

Register the new submodule by adding:

```rust
pub mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

This follows the existing pattern in sibling model modules (`summary.rs`, `details.rs`),
which are declared and re-exported from `mod.rs`.

### 3. `tests/api/advisory_summary.rs`

Create integration tests (detailed in the Tests section below).

Register the test module in `tests/api/mod.rs` (or in the test crate's `Cargo.toml` if
tests are flat binaries without a module tree -- adapt to whichever pattern the existing
`tests/api/advisory.rs` uses).

## Files to Modify

### 4. `modules/fundamental/src/advisory/service/advisory.rs`

Add a new method `extract_vulnerability_summary()` to `AdvisoryService`. Following the
existing service method pattern, the method returns `Result<VulnerabilitySummary, AppError>`.

```rust
use crate::advisory::model::VulnerabilitySummary;
// AdvisoryIngestResult is imported from the ingestor crate
use trustify_ingestor::service::AdvisoryIngestResult;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result.
    ///
    /// Handles nullable fields in `AdvisoryIngestResult` defensively:
    /// `cves`, `affected_packages`, and `severity_counts` may all be `None`
    /// when the upstream advisory lacks the corresponding metadata. Each
    /// `None` field produces a safe default (empty collection or zero count).
    pub fn extract_vulnerability_summary(
        &self,
        ingest_result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard: cves is Option<Vec<String>> -- default to empty Vec
        let cve_list = ingest_result
            .cves
            .as_ref()
            .cloned()
            .unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Guard: affected_packages is Option<Vec<AffectedPackage>> -- default to 0
        let affected_package_count = ingest_result
            .affected_packages
            .as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Guard: severity_counts is Option<HashMap<String, u32>> -- default to empty HashMap
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
}
```

Key design decisions:

- **`as_ref().cloned().unwrap_or_default()` for `cves` and `severity_counts`**: uses
  `as_ref()` to avoid moving out of the borrowed `ingest_result`, then `cloned()` to
  produce an owned copy, then `unwrap_or_default()` to fall back to empty collection.
- **`as_ref().map(...).unwrap_or(0)` for `affected_packages`**: we only need the count
  (not the full list), so we map to `.len()` inside the `Option` and default to 0.
  This avoids cloning the entire `Vec<AffectedPackage>`.
- No `.unwrap()` calls anywhere -- all Option access goes through safe combinators.
- The method takes `&AdvisoryIngestResult` (borrowed) since it only reads data.
- Returns `Result<_, AppError>` to match the existing service method convention, even
  though the current implementation is infallible. This future-proofs the signature for
  validation logic that may be added later.

## Tests

### `tests/api/advisory_summary.rs`

Four test functions covering all acceptance criteria and test requirements:

```rust
use std::collections::HashMap;
use trustify_fundamental::advisory::model::VulnerabilitySummary;
// Assume test helper for constructing AdvisoryIngestResult
use trustify_ingestor::service::AdvisoryIngestResult;

/// Verifies that a fully-populated AdvisoryIngestResult produces correct summary values.
#[test]
fn test_extract_summary_all_fields_populated() {
    // Given an AdvisoryIngestResult with all fields set to Some
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()]),
        affected_packages: Some(vec![
            make_affected_package("pkg-a"),
            make_affected_package("pkg-b"),
            make_affected_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
        ..Default::default()
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
    assert_eq!(summary.severity_breakdown.len(), 2);
}

/// Verifies that an all-None AdvisoryIngestResult produces a zeroed summary without panicking.
#[test]
fn test_extract_summary_all_none_fields() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        ..Default::default()
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields have safe defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other fields are populated.
#[test]
fn test_extract_summary_mixed_some_and_none() {
    // Given an AdvisoryIngestResult where cves is Some but packages and severity are None
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        ..Default::default()
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then cve fields reflect the input, while other fields have defaults
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given results with various cve list sizes including None
    let cases: Vec<Option<Vec<String>>> = vec![
        None,
        Some(vec![]),
        Some(vec!["CVE-2024-0001".to_string()]),
        Some(vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
            "CVE-2024-0003".to_string(),
        ]),
    ];

    for cves in cases {
        let ingest_result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
            ..Default::default()
        };

        // When extracting the summary
        let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

        // Then cve_count always equals cve_list.len()
        assert_eq!(
            summary.cve_count,
            summary.cve_list.len() as u32,
            "cve_count ({}) did not match cve_list.len() ({})",
            summary.cve_count,
            summary.cve_list.len()
        );
    }
}
```

Notes on test design:
- Value-based assertions (not just length checks) -- per the skill's quality standard.
- Each test has a doc comment explaining what it verifies.
- Given/When/Then section comments for non-trivial tests.
- The all-None test is the critical case for verifying null guards work.
- The consistency test uses a data-driven approach with multiple cases, following the
  project's Rust test conventions.

## Module Registration and Imports

- `modules/fundamental/src/advisory/model/mod.rs`: add `pub mod vulnerability_summary;`
  and `pub use vulnerability_summary::VulnerabilitySummary;` following the existing
  `pub mod summary;` / `pub mod details;` pattern.
- `modules/fundamental/src/advisory/service/advisory.rs`: add `use` for
  `VulnerabilitySummary` and `AdvisoryIngestResult`.
- `tests/api/advisory_summary.rs`: register in the test harness (e.g., `mod advisory_summary;`
  in `tests/api/mod.rs` or as a separate `[[test]]` target in `tests/Cargo.toml`).

## Scope Containment

Only files listed in the task's Files to Modify and Files to Create are touched:

| File | Action | In scope? |
|------|--------|-----------|
| `modules/fundamental/src/advisory/service/advisory.rs` | Modify | Yes (Files to Modify) |
| `modules/fundamental/src/advisory/model/vulnerability_summary.rs` | Create | Yes (Files to Create) |
| `tests/api/advisory_summary.rs` | Create | Yes (Files to Create) |
| `modules/fundamental/src/advisory/model/mod.rs` | Modify | Flagged for user approval -- needed to register the new submodule |

The `model/mod.rs` modification is a minimal one-line addition required for the new file
to be usable. This would be flagged during Step 9's scope containment check for user
approval.

## Data-Flow Trace

1. **Input**: `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()` in
   `modules/ingestor/src/service/mod.rs`. Data crosses the ingestor-to-fundamental module
   boundary.
2. **Processing**: `AdvisoryService::extract_vulnerability_summary()` reads the three
   nullable fields, applies null guards, computes counts, and assembles the output struct.
3. **Output**: `VulnerabilitySummary` with non-optional fields ready for email digest
   consumption.

The flow is complete within the scope of this task. The email notification consumer is
outside this task's scope (TC-9001 parent feature).
