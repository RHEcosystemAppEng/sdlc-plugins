# Implementation Plan -- TC-9211

## Task Summary

Add a vulnerability summary extractor (`extract_vulnerability_summary()`) to `AdvisoryService` that processes `AdvisoryIngestResult` records from the ingestor module and produces a `VulnerabilitySummary` struct suitable for email digest notifications. The extractor must handle all three nullable fields (`cves`, `affected_packages`, `severity_counts`) gracefully without panicking.

---

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**What changes**: Add a new public method `extract_vulnerability_summary()` to `AdvisoryService`.

**Method signature**:

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Processes the nullable fields in `AdvisoryIngestResult` and produces a
/// `VulnerabilitySummary` with non-optional fields and sensible defaults
/// for any missing data.
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
```

**Implementation logic**:

```rust
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Handle cves: Option<Vec<String>> -> Vec<String>
    let cve_list = ingest_result
        .cves
        .as_ref()
        .cloned()
        .unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Handle affected_packages: Option<Vec<AffectedPackage>> -> u32 count
    let affected_package_count = ingest_result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Handle severity_counts: Option<HashMap<String, u32>> -> HashMap<String, u32>
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

**Integration**: This follows the existing service method pattern in `advisory.rs` where methods return `Result<T, AppError>`. The method uses `&self` to conform to the `AdvisoryService` method conventions and `.context()` wrapping if any fallible operations were needed (in this case the method is infallible aside from the Result wrapper for API consistency).

**Module registration**: Add `mod vulnerability_summary;` to `modules/fundamental/src/advisory/model/mod.rs` and a `pub use vulnerability_summary::VulnerabilitySummary;` re-export.

Also add `use crate::advisory::model::VulnerabilitySummary;` import to `advisory.rs`.

### 2. `modules/fundamental/src/advisory/model/mod.rs`

**What changes**: Add module declaration and re-export for the new `vulnerability_summary` module.

```rust
mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

---

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**What it contains**: The `VulnerabilitySummary` output struct with non-optional fields.

```rust
use std::collections::HashMap;

/// A summarized view of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional and use sensible defaults (empty collections, zero counts)
/// when the source `AdvisoryIngestResult` has `None` values for its optional fields.
#[derive(Debug, Clone, PartialEq)]
pub struct VulnerabilitySummary {
    /// Total number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,
    /// Breakdown of vulnerability counts by severity level (e.g., "critical" -> 3).
    pub severity_breakdown: HashMap<String, u32>,
}

impl Default for VulnerabilitySummary {
    fn default() -> Self {
        Self {
            cve_count: 0,
            cve_list: Vec::new(),
            affected_package_count: 0,
            severity_breakdown: HashMap::new(),
        }
    }
}
```

**Conventions followed**: Uses `#[derive(Debug, Clone, PartialEq)]` consistent with sibling model structs (`AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`). Implements `Default` to support test construction and the "zeroed summary" contract for all-None inputs.

### 2. `tests/api/advisory_summary.rs`

**What it contains**: Integration tests for the vulnerability summary extractor.

```rust
use std::collections::HashMap;
use modules_fundamental::advisory::model::VulnerabilitySummary;
// Import AdvisoryIngestResult and AffectedPackage from ingestor module
use modules_ingestor::service::AdvisoryIngestResult;

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
            create_test_affected_package("pkg-a"),
            create_test_affected_package("pkg-b"),
            create_test_affected_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
        // ... other fields as needed
    };

    // When extracting the vulnerability summary
    let service = create_test_advisory_service();
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed");

    // Then all fields should reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
    assert_eq!(summary.severity_breakdown.len(), 2);
}

/// Verifies that an AdvisoryIngestResult with all None fields produces a zeroed summary.
#[test]
fn test_extract_summary_all_none_fields() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other fields as needed
    };

    // When extracting the vulnerability summary
    let service = create_test_advisory_service();
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed even with all-None fields");

    // Then all fields should have sensible zero/empty defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none_cves_only() {
    // Given an AdvisoryIngestResult with only cves populated
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other fields as needed
    };

    // When extracting the vulnerability summary
    let service = create_test_advisory_service();
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed");

    // Then cve fields should reflect input, others should default
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none_packages_only() {
    // Given an AdvisoryIngestResult with only affected_packages populated
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: Some(vec![
            create_test_affected_package("pkg-x"),
        ]),
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let service = create_test_advisory_service();
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed");

    // Then affected_package_count reflects input, others default
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 1);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none_severity_only() {
    // Given an AdvisoryIngestResult with only severity_counts populated
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: Some(HashMap::from([
            ("low".to_string(), 5),
        ])),
    };

    // When extracting the vulnerability summary
    let service = create_test_advisory_service();
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed");

    // Then severity_breakdown reflects input, others default
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert_eq!(summary.severity_breakdown.get("low"), Some(&5));
    assert_eq!(summary.severity_breakdown.len(), 1);
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various CVE list sizes
    let test_cases: Vec<Option<Vec<String>>> = vec![
        None,
        Some(vec![]),
        Some(vec!["CVE-2024-0001".to_string()]),
        Some(vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
            "CVE-2024-0003".to_string(),
        ]),
    ];

    let service = create_test_advisory_service();

    for cves in test_cases {
        let ingest_result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
        };

        // When extracting the summary
        let summary = service
            .extract_vulnerability_summary(&ingest_result)
            .expect("extraction should succeed");

        // Then cve_count must always equal cve_list.len()
        assert_eq!(
            summary.cve_count,
            summary.cve_list.len() as u32,
            "cve_count ({}) does not match cve_list.len() ({})",
            summary.cve_count,
            summary.cve_list.len()
        );
    }
}
```

**Test module registration**: Add `mod advisory_summary;` to `tests/api/mod.rs` (or the test harness entrypoint as appropriate).

---

## Handling Nullable Fields from AdvisoryIngestResult

The core challenge is that `AdvisoryIngestResult` (defined in `modules/ingestor/src/service/mod.rs`) uses `Option<T>` for all three aggregate fields. Since the data crosses a module boundary (ingestor -> fundamental), the extractor must apply defensive property access on every field.

### Strategy per field

| Field | Type | Guard Pattern | Output |
|-------|------|---------------|--------|
| `cves` | `Option<Vec<String>>` | `.as_ref().cloned().unwrap_or_default()` | `Vec<String>` (empty if None) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|p\| p.len() as u32).unwrap_or(0)` | `u32` (0 if None) |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.as_ref().cloned().unwrap_or_default()` | `HashMap<String, u32>` (empty if None) |

No `.unwrap()` calls are used anywhere. All Option handling uses Rust idiomatic combinators (`unwrap_or_default`, `as_ref`, `map`, `cloned`).

---

## Data-Flow Trace

**Input**: `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()` in the ingestor module.

**Processing**: `AdvisoryService::extract_vulnerability_summary()` in the fundamental module reads the three nullable fields, applies defensive guards, and constructs a `VulnerabilitySummary`.

**Output**: `VulnerabilitySummary` struct with non-optional fields, ready for consumption by the email digest notification system.

Flow: `IngestorService::ingest_advisory()` -> `AdvisoryIngestResult` -> `AdvisoryService::extract_vulnerability_summary()` -> `VulnerabilitySummary` -> email digest consumer (out of scope for this task).

The input and processing stages are fully connected. The output stage (email digest consumer) is intentionally out of scope per the task description.

---

## Acceptance Criteria Verification Plan

| Criterion | How verified |
|-----------|-------------|
| `extract_vulnerability_summary()` produces valid summary from fully-populated input | `test_extract_summary_all_fields_populated` asserts specific field values |
| Handles None values without panicking | `test_extract_summary_all_none_fields` passes with all-None input |
| VulnerabilitySummary fields are always non-optional with sensible defaults | Struct definition uses non-optional types; Default impl provides zeroed values |
| cve_count matches cve_list.len() | `test_cve_count_matches_cve_list_length` checks invariant across multiple inputs |

---

## Convention Conformance

| Convention | Source | Applied How |
|-----------|--------|-------------|
| Service methods return `Result<T, AppError>` | Sibling methods in `advisory.rs` | Method signature uses `Result<VulnerabilitySummary, AppError>` |
| Model structs derive Debug, Clone | Sibling models (`AdvisorySummary`, `SbomSummary`) | `#[derive(Debug, Clone, PartialEq)]` |
| Module pattern: model/ + service/ | Repository convention | New model in `model/vulnerability_summary.rs`, method in `service/advisory.rs` |
| Test assertions use `assert_eq!` with specific values | Sibling tests in `tests/api/` | All tests assert on concrete values, not just lengths |
| Doc comments on all public symbols | SKILL.md requirement | `///` doc comments on struct, fields, and method |
| Given-When-Then test structure | SKILL.md requirement | Section comments in all non-trivial tests |
