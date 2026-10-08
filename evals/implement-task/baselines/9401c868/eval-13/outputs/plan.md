# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records from the ingestor module and produces a `VulnerabilitySummary` digest suitable for email notifications. The extractor must handle all nullable fields (`cves`, `affected_packages`, `severity_counts`) gracefully without panicking.

## Repository

trustify-backend

## Target Branch

main

## Project Configuration Validation (Step 0)

The mock CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Tool naming convention and configured instance

Configuration is valid. Proceeding.

## Parsed Task Sections (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new branch and PR flow)

---

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

**What exists**: AdvisoryService with methods like `fetch`, `list`, `search` that follow the pattern of returning `Result<T, AppError>`.

**Changes**:
- Add a new public method `extract_vulnerability_summary(&self, ingest_result: &AdvisoryIngestResult) -> Result<VulnerabilitySummary, AppError>` to AdvisoryService.
- The method consumes an `AdvisoryIngestResult` reference and produces a `VulnerabilitySummary` with all nullable fields safely defaulted.
- Add `use` import for `VulnerabilitySummary` from the new model module.
- Add `use` import for `AdvisoryIngestResult` from `modules/ingestor/src/service/mod.rs` (the ingestor crate).

**Implementation of `extract_vulnerability_summary`**:

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Handles nullable fields from the ingest result by defaulting to
/// empty collections and zero counts when data is absent.
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Defensive access: cves may be None when advisory has no CVE references
    let cve_list = ingest_result
        .cves
        .as_ref()
        .cloned()
        .unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Defensive access: affected_packages may be None for advisories without package-level detail
    let affected_package_count = ingest_result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Defensive access: severity_counts may be None when severity metadata is absent
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

**Convention conformance**: Follows the existing service method pattern -- methods on AdvisoryService return `Result<T, AppError>`. Uses `.context()` wrapping if any fallible operations are added. Named with `verb_noun` pattern consistent with sibling methods (`fetch`, `list`, `search`).

---

## Files to Create

### 2. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose**: Define the `VulnerabilitySummary` output struct with non-optional fields and sensible defaults.

**Content**:

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Summary of vulnerabilities extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults, ensuring consumers
/// never need to handle None values. Produced by
/// `AdvisoryService::extract_vulnerability_summary()`.
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
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

**Integration**: Register this module in `modules/fundamental/src/advisory/model/mod.rs` by adding:
```rust
pub mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

**Design rationale**:
- Derives `Default` so callers can construct a zeroed summary easily (useful in tests and fallback paths).
- Derives `PartialEq, Eq` to support `assert_eq!` in tests.
- Derives `Serialize, Deserialize` to match sibling model structs (`AdvisorySummary`, `AdvisoryDetails`) that are serializable for API responses.
- All fields are non-optional per task specification, shifting the null-handling burden from consumers to the producer (`extract_vulnerability_summary`).

### 3. `modules/fundamental/src/advisory/model/mod.rs` (modify)

**Change**: Add the new module declaration and re-export. This file already declares `pub mod summary;` and `pub mod details;` -- add `pub mod vulnerability_summary;` alongside them.

Note: This file is not explicitly listed in "Files to Modify" but is required to register the new module. This would be flagged in Step 9's scope containment check and user approval would be requested before committing.

### 4. `tests/api/advisory_summary.rs`

**Purpose**: Integration tests for the vulnerability summary extractor.

**Content**:

```rust
use std::collections::HashMap;
use trustify_fundamental::advisory::model::VulnerabilitySummary;
// Import AdvisoryIngestResult from ingestor module
// Import AdvisoryService and test utilities

/// Verifies extraction from a fully-populated AdvisoryIngestResult with all fields Some.
#[test]
fn test_extract_summary_all_fields_populated() {
    // Given a fully-populated AdvisoryIngestResult
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
        // ... other required fields with test defaults
    };

    // When extracting the vulnerability summary
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed");

    // Then all fields should reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(
        summary.cve_list,
        vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()]
    );
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
}

/// Verifies extraction handles all-None fields without panicking, producing a zeroed summary.
#[test]
fn test_extract_summary_all_none_fields() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other required fields with test defaults
    };

    // When extracting the vulnerability summary
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed even with all-None fields");

    // Then all fields should have zero/empty defaults
    assert_eq!(summary.cve_count, 0);
    assert_eq!(summary.cve_list, Vec::<String>::new());
    assert_eq!(summary.affected_package_count, 0);
    assert_eq!(summary.severity_breakdown, HashMap::new());
}

/// Verifies extraction handles mixed Some/None fields independently.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves populated but other fields None
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other required fields with test defaults
    };

    // When extracting the vulnerability summary
    let summary = service
        .extract_vulnerability_summary(&ingest_result)
        .expect("extraction should succeed with mixed fields");

    // Then populated fields reflect data, None fields have defaults
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999".to_string()]);
    assert_eq!(summary.affected_package_count, 0);
    assert_eq!(summary.severity_breakdown, HashMap::new());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given varying numbers of CVEs
    let test_cases = vec![
        vec![],
        vec!["CVE-2024-0001".to_string()],
        vec![
            "CVE-2024-0001".to_string(),
            "CVE-2024-0002".to_string(),
            "CVE-2024-0003".to_string(),
        ],
    ];

    for cves in test_cases {
        let expected_count = cves.len() as u32;
        let ingest_result = AdvisoryIngestResult {
            cves: Some(cves),
            affected_packages: None,
            severity_counts: None,
            // ... other required fields with test defaults
        };

        // When extracting
        let summary = service
            .extract_vulnerability_summary(&ingest_result)
            .expect("extraction should succeed");

        // Then cve_count must equal cve_list.len()
        assert_eq!(
            summary.cve_count,
            summary.cve_list.len() as u32,
            "cve_count must match cve_list.len()"
        );
        assert_eq!(summary.cve_count, expected_count);
    }
}
```

**Test registration**: Add `mod advisory_summary;` to `tests/api/mod.rs` (or the test harness entry point). This would also be flagged as an out-of-scope file in Step 9.

---

## Integration Points

### Module registration chain

1. `vulnerability_summary.rs` is declared in `advisory/model/mod.rs`
2. `advisory/model/mod.rs` re-exports `VulnerabilitySummary`
3. `advisory/service/advisory.rs` imports `VulnerabilitySummary` and `AdvisoryIngestResult`
4. `tests/api/advisory_summary.rs` imports both types for test construction and assertion

### Cross-crate dependency

The `extract_vulnerability_summary` method references `AdvisoryIngestResult` from the `ingestor` crate (`modules/ingestor/src/service/mod.rs`). Before implementing, verify that `modules/fundamental/Cargo.toml` already lists the `ingestor` crate as a dependency.

- **If it does**: import directly -- no changes needed to dependency manifests.
- **If it does not**: this is a new cross-crate dependency. Evaluate whether to add the dependency or duplicate/inline the `AdvisoryIngestResult` type. Since the method's entire purpose is to consume ingestor output, adding the dependency is justified. Add to `modules/fundamental/Cargo.toml`:
  ```toml
  [dependencies]
  trustify-ingestor = { path = "../ingestor" }
  ```

### Data-flow trace

1. **Input**: `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()` (ingestor module)
2. **Processing**: `AdvisoryService::extract_vulnerability_summary()` applies null guards and transforms to `VulnerabilitySummary`
3. **Output**: `VulnerabilitySummary` struct returned to caller for use in email digest rendering

The flow is complete: ingest result (input) -> extraction with defensive access (processing) -> non-optional summary struct (output). No persistence or API endpoint is required by this task.

---

## Acceptance Criteria Verification Plan

| Criterion | Verification |
|-----------|-------------|
| `extract_vulnerability_summary()` produces valid summary from fully-populated input | `test_extract_summary_all_fields_populated` asserts all fields |
| Handles None values for all three nullable fields without panicking | `test_extract_summary_all_none_fields` passes with zeroed defaults |
| VulnerabilitySummary fields are always populated (non-optional) with sensible defaults | Struct definition has no `Option<T>` fields; None inputs produce defaults |
| cve_count matches cve_list length | `test_cve_count_matches_cve_list_length` validates consistency |

---

## Nullable Field Handling Summary

All three nullable fields from `AdvisoryIngestResult` are handled using Rust idiomatic patterns:

| Field | Type | Guard Pattern | Default Value |
|-------|------|--------------|---------------|
| `cves` | `Option<Vec<String>>` | `.as_ref().cloned().unwrap_or_default()` | `Vec::new()` (empty vec) |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|pkgs\| pkgs.len() as u32).unwrap_or(0)` | `0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.as_ref().cloned().unwrap_or_default()` | `HashMap::new()` (empty map) |

See `null-guards.md` for the full defensive property access analysis.

---

## Self-Verification Checklist (Step 9)

- **Scope containment**: `advisory/model/mod.rs` (module registration) and `tests/api/mod.rs` (test registration) are out-of-scope modifications required for integration. Would flag for user approval.
- **Dead parameter detection**: No parameters removed from existing functions.
- **Sensitive-pattern check**: No secrets, credentials, or environment files involved.
- **Documentation currency**: No public API endpoints changed; no doc updates needed.
- **Duplication check**: Search for existing vulnerability summary or CVE extraction utilities in the codebase before implementing.
- **CI checks**: Run `cargo fmt`, `cargo clippy`, and `cargo test -p trustify-fundamental` per CONVENTIONS.md (if present) or standard Rust CI practices.
