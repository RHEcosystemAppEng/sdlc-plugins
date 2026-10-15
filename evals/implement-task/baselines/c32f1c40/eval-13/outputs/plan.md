# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records
from the ingestor module and produces a `VulnerabilitySummary` digest suitable for
email notifications. The extractor reads optional/nullable fields and produces a
struct with non-optional fields using sensible defaults.

## Target Repository

trustify-backend

## Target Branch

main

## Files to Modify

### `modules/fundamental/src/advisory/service/advisory.rs`

**What exists:** AdvisoryService with methods like `fetch`, `list`, `search`, all
returning `Result<T, AppError>`.

**Changes:**

1. Add a new method `extract_vulnerability_summary` to `AdvisoryService`:

```rust
/// Extracts a vulnerability summary from an advisory ingest result,
/// producing a digest suitable for email notifications.
///
/// All nullable fields in `AdvisoryIngestResult` are handled defensively:
/// `None` values are replaced with sensible defaults (empty collections,
/// zero counts) so the returned `VulnerabilitySummary` always has
/// populated, non-optional fields.
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Handle nullable cves field
    let cve_list = ingest_result.cves
        .as_ref()
        .cloned()
        .unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Handle nullable affected_packages field
    let affected_package_count = ingest_result.affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Handle nullable severity_counts field
    let severity_breakdown = ingest_result.severity_counts
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

2. Add the necessary imports at the top of the file:
   - `use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;`
   - Ensure `AdvisoryIngestResult` is imported from the ingestor module
     (the ingestor crate should already be a dependency of the fundamental crate;
     verify in `modules/fundamental/Cargo.toml`)

**Convention conformance:** The method follows the existing pattern of AdvisoryService
methods returning `Result<T, AppError>`. Method name uses the `verb_noun` pattern
consistent with sibling methods (`fetch_advisory`, `list_advisories`).

## Files to Create

### `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose:** Define the `VulnerabilitySummary` output struct.

**Contents:**

```rust
use std::collections::HashMap;

/// Summary of vulnerabilities extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults for missing upstream data.
/// This struct is suitable for rendering advisory digest emails.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers in this advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by this advisory.
    pub affected_package_count: u32,
    /// Counts of vulnerabilities per severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}
```

**Integration:** Register the module in `modules/fundamental/src/advisory/model/mod.rs`
by adding `pub mod vulnerability_summary;`.

### `tests/api/advisory_summary.rs`

**Purpose:** Integration tests for the vulnerability summary extractor.

**Test cases:**

```rust
use std::collections::HashMap;

/// Verifies that a fully-populated AdvisoryIngestResult produces a complete summary.
#[test]
fn test_extract_summary_fully_populated() {
    // Given an AdvisoryIngestResult with all fields populated
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-0001".to_string(), "CVE-2024-0002".to_string()]),
        affected_packages: Some(vec![
            make_test_affected_package("pkg-a"),
            make_test_affected_package("pkg-b"),
            make_test_affected_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
        // ... other required fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then the summary reflects all upstream data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-0001", "CVE-2024-0002"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
}

/// Verifies that an AdvisoryIngestResult with all None fields produces a zeroed summary.
#[test]
fn test_extract_summary_all_none() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other required fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields have zero/empty defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that mixed Some/None fields default independently.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves=Some but other fields=None
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-0099".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other required fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then cve fields are populated but others default to zero/empty
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-0099"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_consistent_with_list_length() {
    // Given various cve list sizes
    for count in [0, 1, 5, 100] {
        let cves: Vec<String> = (0..count)
            .map(|i| format!("CVE-2024-{:04}", i))
            .collect();
        let ingest_result = AdvisoryIngestResult {
            cves: Some(cves.clone()),
            affected_packages: None,
            severity_counts: None,
            // ... other required fields
        };

        // When extracting the summary
        let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

        // Then cve_count equals cve_list.len()
        assert_eq!(summary.cve_count, summary.cve_list.len() as u32);
        assert_eq!(summary.cve_list, cves);
    }
}
```

**Integration:** Register the test module in `tests/api/` by adding `mod advisory_summary;`
to the test harness entry point (e.g., `tests/api/mod.rs` or the `#[cfg(test)]` module).

## Dependency Verification

The `AdvisoryIngestResult` struct is defined in `modules/ingestor/src/service/mod.rs`.
Before implementing, verify that `modules/fundamental/Cargo.toml` already has a
dependency on the `ingestor` crate. If it does, the `AdvisoryIngestResult` type can be
imported directly. If not, assess whether adding the dependency is appropriate (per the
skill's "Reuse over duplication" guidance) or whether the struct definition should be
duplicated.

## Module Registration Steps

1. Add `pub mod vulnerability_summary;` to `modules/fundamental/src/advisory/model/mod.rs`
2. Add import of `VulnerabilitySummary` in `advisory.rs`
3. Register test module in `tests/api/` (via `mod.rs` or test harness)

## Data Flow Trace

```
Input:  AdvisoryIngestResult (from IngestorService::ingest_advisory())
          |
          v
Processing: extract_vulnerability_summary() in AdvisoryService
          - Reads cves (Option<Vec<String>>) -> unwrap_or_default -> Vec<String>
          - Reads affected_packages (Option<Vec<AffectedPackage>>) -> map len or default 0
          - Reads severity_counts (Option<HashMap<String, u32>>) -> unwrap_or_default
          - Computes cve_count from cve_list.len()
          |
          v
Output: VulnerabilitySummary (non-optional fields, ready for email digest rendering)
```

All stages are connected. The output struct has no optional fields, ensuring
downstream email rendering code does not need additional null checks.
