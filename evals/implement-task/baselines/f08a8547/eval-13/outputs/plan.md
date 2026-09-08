# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records from the ingestor module and produces a `VulnerabilitySummary` struct suitable for email digest notifications. The extractor must handle all nullable/optional fields defensively.

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- **Repository Registry**: present, lists `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, lists `serena_backend` instance with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

All required sections are present:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add vulnerability summary extractor processing `AdvisoryIngestResult`
- **Files to Modify**: 1 file
- **Files to Create**: 2 files
- **Implementation Notes**: present with patterns and defaults
- **Acceptance Criteria**: 4 items
- **Test Requirements**: 4 test cases
- **Dependencies**: None

No Target PR, no Bookend Type -- this is a standard implementation flow.

## Step 4 -- Code Understanding Plan

### Files to inspect before implementation

1. **`modules/ingestor/src/service/mod.rs`** -- Read `AdvisoryIngestResult` struct definition to confirm field types (`Option<Vec<String>>`, `Option<Vec<AffectedPackage>>`, `Option<HashMap<String, u32>>`).

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read `AdvisoryService` to understand:
   - Existing method signatures and patterns (return `Result<T, AppError>` with `.context()`)
   - Import conventions
   - How the service accesses the ingestor module's types

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Check existing model re-exports to understand how to register the new `vulnerability_summary` module.

4. **`modules/fundamental/src/advisory/model/summary.rs`** (sibling) -- Study the `AdvisorySummary` struct for conventions: derive macros, doc comments, field naming, serde attributes.

5. **`modules/fundamental/src/advisory/model/details.rs`** (sibling) -- Second sibling for model convention confirmation.

6. **`tests/api/advisory.rs`** (sibling test) -- Study test patterns: assertion style, setup, database bootstrapping, response validation.

7. **`common/src/error.rs`** -- Confirm `AppError` type and `.context()` usage for error handling.

8. **`CONVENTIONS.md`** at repository root -- Check for CI commands and coding conventions.

### Convention conformance expectations (based on repo structure)

- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Naming**: snake_case for functions, PascalCase for types
- **Module structure**: `model/ + service/ + endpoints/`
- **Derives**: likely `#[derive(Debug, Clone, Serialize, Deserialize)]` on model structs
- **Test assertions**: `assert_eq!` with specific values, not length-only checks

## Step 5 -- Branch Creation

```
git checkout main
git pull
git checkout -b TC-9211
```

## Step 6 -- Implementation Changes

### File 1: CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose**: Define the `VulnerabilitySummary` output struct.

**Changes**:
- Add module-level doc comment explaining the struct's purpose (email digest output)
- Define `VulnerabilitySummary` struct with non-optional fields:
  ```rust
  use std::collections::HashMap;
  use serde::{Deserialize, Serialize};

  /// Summary of vulnerability data extracted from an advisory ingest result,
  /// suitable for inclusion in email digest notifications.
  #[derive(Debug, Clone, Serialize, Deserialize, Default)]
  pub struct VulnerabilitySummary {
      /// Number of CVE identifiers found in the advisory.
      pub cve_count: u32,
      /// List of CVE identifier strings (e.g., "CVE-2024-1234").
      pub cve_list: Vec<String>,
      /// Number of packages affected by the advisory.
      pub affected_package_count: u32,
      /// Counts of vulnerabilities broken down by severity level
      /// (e.g., "critical" -> 3, "high" -> 7).
      pub severity_breakdown: HashMap<String, u32>,
  }
  ```
- Derive `Default` so that an empty summary is trivially constructible
- All fields are non-optional with sensible zero-value defaults via `Default`

### File 2: MODIFY `modules/fundamental/src/advisory/model/mod.rs`

**Purpose**: Register the new `vulnerability_summary` module.

**Changes**:
- Add `pub mod vulnerability_summary;` declaration
- Add `pub use vulnerability_summary::VulnerabilitySummary;` re-export (follow sibling pattern from `summary.rs` and `details.rs`)

### File 3: MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose**: Add the `extract_vulnerability_summary()` method to `AdvisoryService`.

**Changes**:
- Add import for `VulnerabilitySummary` from the model module
- Add import for `AdvisoryIngestResult` from the ingestor module (or reference it by full path)
- Add import for `std::collections::HashMap`
- Add new method `extract_vulnerability_summary`:

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Handles nullable fields from `AdvisoryIngestResult` by defaulting
/// `None` values to empty collections, ensuring the returned
/// `VulnerabilitySummary` always has valid, non-optional fields.
pub fn extract_vulnerability_summary(
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Guard each nullable field with unwrap_or_default / as_deref
    let cve_list = result.cves.clone().unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    let affected_package_count = result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

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
```

**Key design decisions**:
- Method is an associated function (no `&self`) since it does not need database access -- it is a pure transformation. If the sibling convention requires `&self` for all service methods, adapt accordingly and take `&self` even if unused.
- Returns `Result<VulnerabilitySummary, AppError>` to follow the existing service method pattern, even though this pure function cannot currently fail. This maintains API consistency and allows future error paths (e.g., validation) without breaking callers.
- Uses `.clone().unwrap_or_default()` for `cves` and `severity_counts` because we need owned values for the output struct.
- Uses `.as_ref().map(...).unwrap_or(0)` for `affected_packages` to avoid cloning the full package list when we only need the count.

### File 4: CREATE `tests/api/advisory_summary.rs`

**Purpose**: Integration tests for the vulnerability summary extractor.

**Changes**:
- Add test module with four test functions:

```rust
/// Verifies that a fully-populated AdvisoryIngestResult produces
/// a correct summary with all fields populated.
#[test]
fn test_extract_summary_fully_populated() {
    // Given an AdvisoryIngestResult with all fields populated
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-0001".to_string(), "CVE-2024-0002".to_string()]),
        affected_packages: Some(vec![
            make_test_package("pkg-a"),
            make_test_package("pkg-b"),
            make_test_package("pkg-c"),
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 2),
        ])),
        // ... other required fields with defaults
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then all fields reflect the input data
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-0001", "CVE-2024-0002"]);
    assert_eq!(summary.affected_package_count, 3);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&2));
}

/// Verifies that an AdvisoryIngestResult with all None fields produces
/// a zeroed summary without panicking.
#[test]
fn test_extract_summary_all_none() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other required fields with defaults
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then all fields default to zero/empty values
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that mixed Some/None fields default independently --
/// a None in one field does not affect extraction of other fields.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with cves=Some but other fields=None
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other required fields with defaults
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

    // Then cves are extracted, but other fields default to zero/empty
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_consistent_with_list_length() {
    // Given multiple AdvisoryIngestResult variants
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
        let result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
            // ... other required fields with defaults
        };

        // When extracting the vulnerability summary
        let summary = AdvisoryService::extract_vulnerability_summary(&result).unwrap();

        // Then cve_count matches cve_list.len()
        assert_eq!(summary.cve_count, expected_count);
        assert_eq!(summary.cve_count as usize, summary.cve_list.len());
    }
}
```

### File 5: MODIFY `tests/api/mod.rs` (or equivalent test registration)

**Purpose**: Register the new test module if the test harness requires explicit module declarations.

**Changes**:
- Add `mod advisory_summary;` to the test module root.

Note: This file is not listed in Files to Modify. It would be flagged as an out-of-scope modification during Step 9 scope containment and requires user approval.

## Step 8 -- Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| `extract_vulnerability_summary()` produces valid summary from fully-populated result | `test_extract_summary_fully_populated` asserts all fields match input values |
| Handles None values without panicking | `test_extract_summary_all_none` passes with all-None input |
| VulnerabilitySummary fields are always non-optional with sensible defaults | Struct definition uses `u32`, `Vec<String>`, `HashMap` -- no `Option` wrappers |
| cve_count matches cve_list length | `test_cve_count_consistent_with_list_length` checks multiple variants including edge cases |

## Step 9 -- Self-Verification Checklist

### Scope containment
- Files to Modify: `advisory.rs` (service) -- in scope
- Files to Create: `vulnerability_summary.rs`, `advisory_summary.rs` (tests) -- in scope
- Potential out-of-scope: `advisory/model/mod.rs` (module registration), `tests/api/mod.rs` (test registration) -- flag for user approval

### Data-flow trace
- **Input**: `AdvisoryIngestResult` from `IngestorService::ingest_advisory()`
- **Processing**: `extract_vulnerability_summary()` reads optional fields, applies null guards, computes counts
- **Output**: `VulnerabilitySummary` struct with non-optional fields
- Flow is complete: input -> transformation -> output. No persistence or API layer needed for this task.

### Contract and sibling parity
- **Contract**: Method returns `Result<T, AppError>` matching sibling service methods
- **Sibling parity**: follows `advisory.rs` patterns for error handling, `summary.rs`/`details.rs` patterns for model definition
- **Cross-module entity**: reads from `AdvisoryIngestResult` (ingestor module) -- read-only, no write concerns

### Duplication check
- Search for existing `VulnerabilitySummary` or `vulnerability_summary` in the codebase
- Search for existing CVE extraction logic that could be reused
- Search for `unwrap_or_default` patterns on `AdvisoryIngestResult` fields

## Step 10 -- Commit Plan

```
git add modules/fundamental/src/advisory/model/vulnerability_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add vulnerability summary extractor for digest emails

Add extract_vulnerability_summary() to AdvisoryService that processes
AdvisoryIngestResult records and produces a VulnerabilitySummary with
non-optional fields. All nullable upstream fields (cves, affected_packages,
severity_counts) are guarded with unwrap_or_default / map+unwrap_or.

Implements TC-9211"
```

## Step 11 -- Jira Update Plan

1. Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
2. Add comment with PR link, summary of changes, and note that no deviations from plan occurred
3. Transition TC-9211 to In Review
