# Implementation Plan for TC-9211

## Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records
from the ingestor module and produces a `VulnerabilitySummary` suitable for email
digest notifications. The extractor must handle all three nullable fields
(`cves`, `affected_packages`, `severity_counts`) defensively, since the data crosses
the module boundary from `modules/ingestor` into `modules/fundamental`.

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose:** Define the `VulnerabilitySummary` output struct with non-optional fields.

**Changes:**

```rust
use std::collections::HashMap;

/// Summary of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional and use sensible defaults when the upstream
/// `AdvisoryIngestResult` contains `None` values. This ensures consumers
/// never need to handle missing data.
#[derive(Debug, Clone, PartialEq, Eq)]
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

**Design decisions:**
- All fields are non-optional (`u32`, `Vec<String>`, `HashMap<String, u32>`) so
  consumers never need to handle `None`.
- Implements `Default` to provide a zeroed-out summary.
- Derives `PartialEq` and `Eq` for test assertions.
- `cve_count` is stored explicitly (rather than computed from `cve_list.len()`) to
  match the task specification, but the extractor ensures they are always consistent.

### 2. `modules/fundamental/src/advisory/model/mod.rs` (modify)

**Purpose:** Register the new `vulnerability_summary` submodule.

**Changes:**
- Add `pub mod vulnerability_summary;` to the existing module declarations.
- Add `pub use vulnerability_summary::VulnerabilitySummary;` for convenient re-export.

### 3. `tests/api/advisory_summary.rs`

**Purpose:** Integration tests for the vulnerability summary extractor.

**Changes:** See test plan below in the Tests section.

### 4. `tests/api/mod.rs` or test harness entry point (modify if needed)

**Purpose:** Register the new test module. If the test directory uses a `mod.rs` or
the tests are standalone files picked up by cargo automatically, no modification is
needed. If tests are registered via a `mod` declaration, add `mod advisory_summary;`.

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose:** Add the `extract_vulnerability_summary()` method to `AdvisoryService`.

**Changes:**

Add a new public method to the existing `AdvisoryService` impl block:

```rust
use crate::advisory::model::VulnerabilitySummary;
use modules_ingestor::service::AdvisoryIngestResult; // adjust import path as needed
use std::collections::HashMap;

impl AdvisoryService {
    /// Extracts a vulnerability summary from an advisory ingest result.
    ///
    /// Converts the optional fields in `AdvisoryIngestResult` into a
    /// `VulnerabilitySummary` with non-optional fields and sensible defaults.
    /// This method never panics on `None` inputs — all nullable fields are
    /// safely unwrapped using `unwrap_or_default()`.
    pub fn extract_vulnerability_summary(
        result: &AdvisoryIngestResult,
    ) -> Result<VulnerabilitySummary, AppError> {
        // Defensively unwrap cves: Option<Vec<String>> -> Vec<String>
        let cve_list = result.cves.clone().unwrap_or_default();
        let cve_count = cve_list.len() as u32;

        // Defensively unwrap affected_packages: Option<Vec<AffectedPackage>> -> count
        let affected_package_count = result
            .affected_packages
            .as_ref()
            .map(|pkgs| pkgs.len() as u32)
            .unwrap_or(0);

        // Defensively unwrap severity_counts: Option<HashMap<String, u32>> -> HashMap
        let severity_breakdown = result
            .severity_counts
            .clone()
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

**Pattern justification:**
- Follows the existing service method pattern: methods on `AdvisoryService` return
  `Result<T, AppError>`.
- Uses `unwrap_or_default()` on `Option<Vec<_>>` and `Option<HashMap<_, _>>` which
  both implement `Default` (producing empty collections).
- Uses `as_ref().map().unwrap_or(0)` for `affected_packages` to avoid cloning the
  entire vector when we only need the count.
- Uses `clone()` on `cves` and `severity_counts` because we need owned data for the
  output struct. If performance is a concern, the signature could take ownership
  (`result: AdvisoryIngestResult`) instead of a reference.

## Handling Nullable Fields from AdvisoryIngestResult

The `AdvisoryIngestResult` struct (defined in `modules/ingestor/src/service/mod.rs`)
uses `Option<T>` for all three aggregate data fields. Since this data crosses the
module boundary from the ingestor into the fundamental advisory service, defensive
access is mandatory. The ingestor may:

1. Return `None` for advisories that lack CVE references, package-level detail, or
   severity metadata.
2. Evolve its schema independently, potentially making previously-populated fields
   optional in new advisory formats.
3. Return partial results due to parsing failures in upstream advisory data.

Each nullable field is handled as follows:

| Field | Type | Guard Pattern | Default Value |
|-------|------|--------------|---------------|
| `cves` | `Option<Vec<String>>` | `.clone().unwrap_or_default()` | `Vec::new()` (empty list) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|v\| v.len() as u32).unwrap_or(0)` | `0` (count only) |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.clone().unwrap_or_default()` | `HashMap::new()` (empty map) |

No `.unwrap()` is used on any `Option` field. No `.len()`, `.join()`, or iteration
is performed directly on an `Option<T>` value without first safely extracting the
inner value.

## Tests

### `tests/api/advisory_summary.rs`

Four test cases covering all acceptance criteria and test requirements:

#### Test 1: Fully populated input (all fields `Some`)

```rust
/// Verifies that a fully-populated AdvisoryIngestResult produces a complete summary
/// with correct counts and data.
#[test]
fn test_extract_summary_all_fields_present() {
    // Given an AdvisoryIngestResult with all fields populated
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()]),
        affected_packages: Some(vec![
            make_test_package("pkg-a"),
            make_test_package("pkg-b"),
            make_test_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1u32),
            ("high".to_string(), 2u32),
        ])),
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then the summary reflects all input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
    assert_eq!(summary.severity_breakdown.len(), 2);
}
```

#### Test 2: All-None input (zeroed summary)

```rust
/// Verifies that an AdvisoryIngestResult with all None fields produces a zeroed
/// summary without panicking.
#[test]
fn test_extract_summary_all_none() {
    // Given an AdvisoryIngestResult with all fields set to None
    let result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then the summary has zeroed/empty defaults
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}
```

#### Test 3: Mixed Some/None fields (independent defaults)

```rust
/// Verifies that each None field defaults independently when other fields are Some.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves populated but other fields None
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then cve fields reflect the input, other fields use defaults
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}
```

#### Test 4: cve_count consistency with cve_list.len()

```rust
/// Verifies that cve_count always matches cve_list.len() for both populated and
/// empty inputs.
#[test]
fn test_cve_count_matches_cve_list_len() {
    // Case 1: populated cves
    let result_some = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-0001".to_string(), "CVE-2024-0002".to_string(),
                        "CVE-2024-0003".to_string()]),
        affected_packages: None,
        severity_counts: None,
    };
    let summary_some = AdvisoryService::extract_vulnerability_summary(&result_some).unwrap();
    assert_eq!(summary_some.cve_count as usize, summary_some.cve_list.len());
    assert_eq!(summary_some.cve_count, 3);

    // Case 2: None cves
    let result_none = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
    };
    let summary_none = AdvisoryService::extract_vulnerability_summary(&result_none).unwrap();
    assert_eq!(summary_none.cve_count as usize, summary_none.cve_list.len());
    assert_eq!(summary_none.cve_count, 0);
}
```

## Convention Conformance

- **Error handling:** Method returns `Result<T, AppError>` consistent with other
  `AdvisoryService` methods.
- **Module structure:** New model file placed in `advisory/model/` following the
  existing `model/ + service/ + endpoints/` pattern.
- **Test location:** Integration test in `tests/api/` following sibling test file
  placement (`advisory.rs`, `sbom.rs`, `search.rs`).
- **Documentation:** All public structs and methods have `///` doc comments.

## Data-Flow Trace

```
Input:  AdvisoryIngestResult (from IngestorService::ingest_advisory())
  |
  v
Processing:  AdvisoryService::extract_vulnerability_summary()
  - Defensively unwraps Option fields
  - Computes cve_count from cve_list length
  - Extracts affected_package_count from vector length
  - Clones severity_counts map
  |
  v
Output:  VulnerabilitySummary (non-optional fields, ready for email digest)
```

All stages are connected. The extractor is a pure transformation with no persistence
or side effects — it converts nullable ingestor output into a clean, non-optional
struct for downstream email notification formatting.
