# Implementation Plan for TC-9211

## Task Summary

Add a vulnerability summary extractor (`extract_vulnerability_summary()`) to
`AdvisoryService` that processes `AdvisoryIngestResult` records from the ingestor
module and produces a `VulnerabilitySummary` suitable for email digest notifications.

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Create the `VulnerabilitySummary` output struct with non-optional fields:

```rust
use std::collections::HashMap;

/// Summary of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults -- when the source
/// `AdvisoryIngestResult` contains `None` for any aggregate field, the
/// corresponding field here is populated with a zero/empty default.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,
    /// Breakdown of vulnerability counts by severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}
```

Register this module in `modules/fundamental/src/advisory/model/mod.rs`:

```rust
pub mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

### 2. `tests/api/advisory_summary.rs`

Create integration tests (detailed in Test Plan section below).

Register in `tests/api/mod.rs` (or the test harness entry point):

```rust
mod advisory_summary;
```

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

Add the `extract_vulnerability_summary()` method to `AdvisoryService`. This method
takes an `AdvisoryIngestResult` and returns `Result<VulnerabilitySummary, AppError>`.

#### Implementation with defensive guards

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;
use modules_ingestor::service::AdvisoryIngestResult;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result.
    ///
    /// Processes the nullable aggregate fields in `AdvisoryIngestResult` and
    /// produces a `VulnerabilitySummary` with non-optional fields. Fields that
    /// are `None` in the input are replaced with sensible defaults (empty
    /// collections, zero counts).
    pub fn extract_vulnerability_summary(
        ingest_result: AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Guard: cves is Option<Vec<String>>. Use unwrap_or_default() to get
        // an empty Vec when None. Data crosses module boundary from ingestor.
        let cve_list = ingest_result.cves.unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Guard: affected_packages is Option<Vec<AffectedPackage>>. Use
        // as_ref().map().unwrap_or(0) to extract only the count without
        // consuming the Option. Data crosses module boundary from ingestor.
        let affected_package_count = ingest_result
            .affected_packages
            .as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Guard: severity_counts is Option<HashMap<String, u32>>. Use
        // unwrap_or_default() to get an empty HashMap when None. Data crosses
        // module boundary from ingestor.
        let severity_breakdown = ingest_result.severity_counts.unwrap_or_default();

        Ok(VulnerabilitySummary {
            cve_count,
            cve_list,
            affected_package_count,
            severity_breakdown,
        })
    }
}
```

## Test Plan

### Test file: `tests/api/advisory_summary.rs`

#### Test 1: Fully-populated `AdvisoryIngestResult` (all fields `Some`)

```rust
/// Verifies that a fully-populated AdvisoryIngestResult produces a complete summary.
#[test]
fn test_extract_summary_all_fields_populated() {
    // Given an AdvisoryIngestResult with all fields populated
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec![
            "CVE-2024-1234".to_string(),
            "CVE-2024-5678".to_string(),
        ]),
        affected_packages: Some(vec![
            make_test_affected_package("pkg-a"),
            make_test_affected_package("pkg-b"),
            make_test_affected_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(ingest_result)
        .expect("extraction should succeed");

    // Then all fields should reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
    assert_eq!(summary.severity_breakdown.len(), 2);
}
```

#### Test 2: All-`None` fields (defensive guard validation)

```rust
/// Verifies that an AdvisoryIngestResult with all None fields produces a zeroed summary.
///
/// This is the critical test for defensive property access: all three nullable fields
/// (cves, affected_packages, severity_counts) are None, and the extractor must not panic.
#[test]
fn test_extract_summary_all_none_fields() {
    // Given an AdvisoryIngestResult with all optional fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(ingest_result)
        .expect("extraction should succeed even with all-None input");

    // Then all fields should have safe defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}
```

#### Test 3: Mixed `Some`/`None` fields (independent defaulting)

```rust
/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with only cves populated
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(ingest_result)
        .expect("extraction should succeed with partial input");

    // Then cve fields should reflect input, others should have defaults
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}
```

#### Test 4: `cve_count` consistency with `cve_list.len()`

```rust
/// Verifies that cve_count is always consistent with the length of cve_list.
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various cve list sizes
    let cases = vec![
        (None, 0),
        (Some(vec![]), 0),
        (Some(vec!["CVE-2024-0001".to_string()]), 1),
        (Some(vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
            "CVE-2024-0003".to_string(),
        ]), 3),
    ];

    for (cves, expected_count) in cases {
        let ingest_result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
        };

        // When extracting the summary
        let summary = AdvisoryService::extract_vulnerability_summary(ingest_result)
            .expect("extraction should succeed");

        // Then cve_count must equal cve_list.len()
        assert_eq!(summary.cve_count, expected_count);
        assert_eq!(summary.cve_count as usize, summary.cve_list.len());
    }
}
```

## Data-Flow Trace

1. **Input**: `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()`
   in `modules/ingestor/src/service/mod.rs`. Three nullable aggregate fields cross the
   module boundary.
2. **Processing**: `AdvisoryService::extract_vulnerability_summary()` in
   `modules/fundamental/src/advisory/service/advisory.rs`. Each `Option` field is
   guarded with `unwrap_or_default()` or `as_ref().map().unwrap_or()` before use.
3. **Output**: `VulnerabilitySummary` struct with non-optional fields, suitable for
   downstream email digest rendering.

All stages connected. No disconnected paths.

## Key Design Decisions

- The method is a pure function (no database access needed) -- it transforms
  `AdvisoryIngestResult` into `VulnerabilitySummary`. The `Result` return type follows
  the existing service method convention even though the current implementation is
  infallible, leaving room for future validation logic.
- `unwrap_or_default()` is chosen over `match`/`if let` for `cves` and
  `severity_counts` because we need the full contained value and `Default` is
  implemented for both `Vec` and `HashMap`.
- `as_ref().map().unwrap_or()` is chosen for `affected_packages` because we only
  need the count, not ownership of the package list.
- No `.unwrap()` is used anywhere -- all `Option` access is guarded.
