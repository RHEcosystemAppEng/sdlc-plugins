# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records and produces a `VulnerabilitySummary` digest suitable for email notifications. The extractor must handle all nullable/optional fields gracefully.

## Repository

trustify-backend (Rust backend service)

## Target Branch

main

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry with trustify-backend entry
- Jira Configuration with project key TC, Cloud ID, and Feature issue type ID
- Code Intelligence with Serena instance serena_backend and tool naming convention

Validation passes.

## Step 1 -- Parse Task Description

### Parsed sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add vulnerability summary extractor for advisory digest emails
- **Files to Modify**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Files to Create**: `modules/fundamental/src/advisory/model/vulnerability_summary.rs`, `tests/api/advisory_summary.rs`
- **Implementation Notes**: AdvisoryIngestResult in `modules/ingestor/src/service/mod.rs`, service method pattern returns `Result<T, AppError>`, output struct has non-optional fields with defaults
- **Acceptance Criteria**: 4 items (fully-populated summary, None handling, non-optional output fields, cve_count consistency)
- **Test Requirements**: 4 tests (all Some, all None, mixed Some/None, cve_count consistency)
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 4 -- Understand the Code

### Files to inspect

1. **`modules/ingestor/src/service/mod.rs`** -- Read `AdvisoryIngestResult` struct definition to confirm the `Option<T>` field types:
   - `cves: Option<Vec<String>>`
   - `affected_packages: Option<Vec<AffectedPackage>>`
   - `severity_counts: Option<HashMap<String, u32>>`

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Inspect `AdvisoryService` to understand:
   - Existing method signatures and patterns (all return `Result<T, AppError>`)
   - Import conventions
   - How the service accesses the ingestor module's types

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Check existing model module structure to understand how models are registered (e.g., `pub mod summary;` declarations).

4. **`modules/fundamental/src/advisory/model/summary.rs`** -- Read sibling model file (`AdvisorySummary`) to understand struct conventions: derive macros, field documentation, serialization attributes.

5. **`modules/fundamental/src/advisory/model/details.rs`** -- Second sibling for convention cross-reference.

6. **`tests/api/advisory.rs`** -- Read sibling test file to understand test conventions: assertion patterns, setup, imports.

7. **`common/src/error.rs`** -- Confirm `AppError` enum and how it's used in Result types.

### Convention conformance analysis

Based on the repository structure and conventions documented in repo-backend.md:

- **Naming**: Rust snake_case for functions, PascalCase for types. Method names follow `verb_noun` pattern.
- **Error handling**: All service methods return `Result<T, AppError>` with `.context()` wrapping.
- **Module structure**: `model/ + service/ + endpoints/` per domain module.
- **Derives**: Model structs likely use `#[derive(Debug, Clone, Serialize, Deserialize)]`.
- **Test patterns**: Integration tests in `tests/api/`, use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

### Documentation files

- `CONVENTIONS.md` at repository root (check for CI commands)
- No API docs directly related to this internal extractor method

## Step 5 -- Create Branch

Would create branch `TC-9211` from `main`:

```bash
git checkout main
git pull
git checkout -b TC-9211
```

## Step 6 -- Implementation Changes

### File 1: CREATE `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

Create the `VulnerabilitySummary` output struct with non-optional fields:

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Summary of vulnerability data extracted from an advisory ingest result.
///
/// All fields are non-optional with sensible defaults applied when the
/// source `AdvisoryIngestResult` contains `None` values. This struct is
/// intended for consumption by email digest notifications.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,

    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,

    /// Number of packages affected by the advisory.
    pub affected_package_count: u32,

    /// Counts of vulnerabilities grouped by severity level
    /// (e.g., "critical" -> 3, "high" -> 7).
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

### File 2: MODIFY `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration for the new model file:

```rust
pub mod vulnerability_summary;
```

This registers `VulnerabilitySummary` in the module tree so it can be imported by the service layer.

### File 3: MODIFY `modules/fundamental/src/advisory/service/advisory.rs`

Add the `extract_vulnerability_summary()` method to `AdvisoryService`. The method takes an `AdvisoryIngestResult` and returns `Result<VulnerabilitySummary, AppError>`.

**Imports to add:**

```rust
use crate::advisory::model::vulnerability_summary::VulnerabilitySummary;
// AdvisoryIngestResult import -- depends on how the ingestor module is
// referenced. Likely via a crate dependency:
use trustify_module_ingestor::service::AdvisoryIngestResult;
```

**Method to add to `impl AdvisoryService`:**

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Processes the optional fields of `AdvisoryIngestResult` and produces
/// a `VulnerabilitySummary` with non-optional fields. Missing upstream
/// data is replaced with sensible defaults (empty collections, zero counts).
pub fn extract_vulnerability_summary(
    &self,
    ingest_result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Defensively extract CVE list, defaulting to empty vec when None
    let cve_list = ingest_result
        .cves
        .as_ref()
        .cloned()
        .unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Defensively extract affected package count, defaulting to 0 when None
    let affected_package_count = ingest_result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Defensively extract severity breakdown, defaulting to empty map when None
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

**Key design decisions:**

- Method takes `&AdvisoryIngestResult` (borrowed reference) -- does not consume the input, allowing the caller to continue using it.
- Uses `.as_ref().cloned().unwrap_or_default()` pattern for `Option<Vec<T>>` and `Option<HashMap<K,V>>` -- idiomatic Rust for defensive extraction.
- Uses `.as_ref().map(|v| ...).unwrap_or(0)` for deriving counts from optional collections.
- `cve_count` is always derived from `cve_list.len()` to guarantee consistency (acceptance criterion 4).
- Returns `Result<T, AppError>` to follow existing service method conventions, even though the current implementation is infallible. This maintains API consistency and allows future error paths.

### File 4: CREATE `tests/api/advisory_summary.rs`

Integration tests for the vulnerability summary extractor. See Test Requirements below.

### File 5: MODIFY `tests/Cargo.toml`

If the test file needs to be registered, ensure `advisory_summary` is included in the test targets.

## Step 7 -- Tests

### Test file: `tests/api/advisory_summary.rs`

Four test functions, following the project's existing test conventions:

```rust
use std::collections::HashMap;
use trustify_module_ingestor::service::AdvisoryIngestResult;
use trustify_module_fundamental::advisory::service::AdvisoryService;

/// Verifies that a fully-populated AdvisoryIngestResult produces a
/// correct summary with all fields populated from the source data.
#[test]
fn test_extract_summary_fully_populated() {
    // Given a fully-populated AdvisoryIngestResult
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec![
            "CVE-2024-1234".to_string(),
            "CVE-2024-5678".to_string(),
        ]),
        affected_packages: Some(vec![
            /* AffectedPackage instances */
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 3),
        ])),
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields are correctly populated
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, /* expected count */);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&3));
}

/// Verifies that an AdvisoryIngestResult with all None fields produces
/// a zeroed summary with empty collections and zero counts.
#[test]
fn test_extract_summary_all_none() {
    // Given an AdvisoryIngestResult with all optional fields as None
    let ingest_result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then all fields default to zero/empty
    assert_eq!(summary.cve_count, 0);
    assert!(summary.cve_list.is_empty());
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that each None field defaults independently when other
/// fields contain Some values.
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given an AdvisoryIngestResult with mixed Some/None fields
    let ingest_result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        // ... other fields
    };

    // When extracting the vulnerability summary
    let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

    // Then populated fields are extracted and None fields default independently
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert!(summary.severity_breakdown.is_empty());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various input sizes
    for cve_count_input in [0, 1, 5, 100] {
        let cves: Vec<String> = (0..cve_count_input)
            .map(|i| format!("CVE-2024-{:04}", i))
            .collect();

        let ingest_result = AdvisoryIngestResult {
            cves: Some(cves.clone()),
            affected_packages: None,
            severity_counts: None,
            // ... other fields
        };

        // When extracting the summary
        let summary = service.extract_vulnerability_summary(&ingest_result).unwrap();

        // Then cve_count always equals cve_list.len()
        assert_eq!(
            summary.cve_count as usize,
            summary.cve_list.len(),
            "cve_count must match cve_list.len() for input of size {}",
            cve_count_input
        );
        assert_eq!(summary.cve_list, cves);
    }
}
```

## Step 8 -- Acceptance Criteria Verification

| Criterion | How satisfied |
|---|---|
| `extract_vulnerability_summary()` produces valid summary from fully-populated input | Test `test_extract_summary_fully_populated` verifies all fields are correctly extracted |
| Handles None values without panicking | Test `test_extract_summary_all_none` passes None for all fields; `unwrap_or_default()` guards prevent panics |
| VulnerabilitySummary fields are always non-optional with sensible defaults | Struct definition uses `u32`, `Vec<String>`, `HashMap<String, u32>` -- no `Option` wrappers |
| cve_count matches cve_list length | `cve_count` is derived from `cve_list.len()` at computation time; test `test_cve_count_matches_cve_list_length` verifies |

## Step 9 -- Self-Verification Checklist

### Scope containment

Files in scope:
- MODIFY: `modules/fundamental/src/advisory/service/advisory.rs` (listed in Files to Modify)
- MODIFY: `modules/fundamental/src/advisory/model/mod.rs` (required for module registration of new file)
- CREATE: `modules/fundamental/src/advisory/model/vulnerability_summary.rs` (listed in Files to Create)
- CREATE: `tests/api/advisory_summary.rs` (listed in Files to Create)

Note: `modules/fundamental/src/advisory/model/mod.rs` is not explicitly listed in Files to Modify but is required to register the new model module. This would be flagged for user approval as an out-of-scope modification.

### Data-flow trace

- **Input**: `AdvisoryIngestResult` produced by `IngestorService::ingest_advisory()`
- **Processing**: `extract_vulnerability_summary()` applies null guards and extracts/counts fields
- **Output**: `VulnerabilitySummary` struct ready for email digest consumption

Flow is complete within the defined scope. The upstream producer (`IngestorService`) and downstream consumer (email digest) are out of scope for this task.

### Duplication check

Would search for existing summary extraction logic:
- `grep -r "VulnerabilitySummary" modules/`
- `grep -r "extract.*summary" modules/fundamental/src/advisory/`
- `grep -r "cve_count" modules/`

### CI checks

Would check `CONVENTIONS.md` for CI commands. At minimum:
- `cargo check` -- compilation verification
- `cargo fmt --check` -- formatting
- `cargo clippy` -- lint
- `cargo test -p trustify-module-fundamental` -- module tests

## Step 10 -- Commit

```
feat(advisory): add vulnerability summary extractor for digest emails

Add VulnerabilitySummary struct and extract_vulnerability_summary() method
to AdvisoryService. The extractor processes AdvisoryIngestResult records
with defensive handling of all Option<T> fields (cves, affected_packages,
severity_counts) using unwrap_or_default() guards.

Implements TC-9211
```

## Summary of Files

| Action | File | Purpose |
|---|---|---|
| CREATE | `modules/fundamental/src/advisory/model/vulnerability_summary.rs` | VulnerabilitySummary struct definition |
| MODIFY | `modules/fundamental/src/advisory/model/mod.rs` | Register new model module |
| MODIFY | `modules/fundamental/src/advisory/service/advisory.rs` | Add `extract_vulnerability_summary()` method |
| CREATE | `tests/api/advisory_summary.rs` | Integration tests (4 test functions) |
