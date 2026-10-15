# Implementation Plan for TC-9211

## Summary

Add a vulnerability summary extractor that processes `AdvisoryIngestResult` records
from the ingestor module and produces a `VulnerabilitySummary` digest suitable for
email notifications. The extractor must handle all nullable fields from the ingestor
output gracefully, producing non-optional output fields with sensible defaults.

## Task Sections Parsed

- **Repository**: trustify-backend
- **Target Branch**: main
- **Files to Modify**: `modules/fundamental/src/advisory/service/advisory.rs`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/vulnerability_summary.rs`
  - `tests/api/advisory_summary.rs`
- **Dependencies**: None

## Step 4 -- Understand the Code

### Sibling / Convention Analysis

Before implementing, the following files would be inspected to understand conventions:

1. **Model siblings** (in `modules/fundamental/src/advisory/model/`):
   - `summary.rs` (AdvisorySummary) -- struct layout, derive macros, field documentation
   - `details.rs` (AdvisoryDetails) -- struct layout, relationship to summary

2. **Service siblings** (in `modules/fundamental/src/advisory/service/`):
   - `advisory.rs` (AdvisoryService) -- method signatures, error handling pattern (`Result<T, AppError>` with `.context()`), how services consume ingestor data

3. **Ingestor source** (in `modules/ingestor/src/service/mod.rs`):
   - `AdvisoryIngestResult` struct definition -- confirm the three `Option<T>` fields and any other fields
   - `AffectedPackage` type definition -- understand its structure for counting

4. **Test siblings** (in `tests/api/`):
   - `advisory.rs` -- test patterns, assertion style, setup/teardown conventions
   - `sbom.rs` -- additional reference for `assert_eq!(resp.status(), StatusCode::OK)` pattern

5. **Error type** (in `common/src/error.rs`):
   - `AppError` enum -- confirm error wrapping conventions

### Discovered Conventions (Expected)

- **Error handling**: `Result<T, AppError>` with `.context()` wrapping on fallible operations
- **Naming**: `verb_noun` pattern for service methods (e.g., `fetch_advisory`, `list_advisories`)
- **Derives**: Model structs use `#[derive(Debug, Clone, Serialize, Deserialize)]`
- **Module registration**: New model files are re-exported via `model/mod.rs`
- **Test assertions**: `assert_eq!` with specific values, not length-only checks

### CONVENTIONS.md

Would check for `trustify-backend/CONVENTIONS.md` and extract any CI check commands
(formatting, linting, clippy, etc.) for use in Step 9.

---

## File 1: Create `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

### Purpose

Define the `VulnerabilitySummary` output struct with non-optional fields. This struct
represents the extracted digest produced by the extractor method.

### Changes

1. Add module-level documentation comment describing the file's purpose.

2. Define `VulnerabilitySummary` struct:

```rust
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// A digest of vulnerability data extracted from an advisory ingest result,
/// suitable for inclusion in email notifications.
///
/// All fields are non-optional and populated with sensible defaults when the
/// source `AdvisoryIngestResult` contains `None` values.
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
pub struct VulnerabilitySummary {
    /// Number of CVE identifiers found in the advisory.
    pub cve_count: u32,
    /// List of CVE identifier strings (e.g., "CVE-2024-1234").
    pub cve_list: Vec<String>,
    /// Number of affected packages referenced by the advisory.
    pub affected_package_count: u32,
    /// Counts of vulnerabilities grouped by severity level (e.g., "critical" -> 5).
    pub severity_breakdown: HashMap<String, u32>,
}
```

3. Derive `Default` to support the all-None test case (zeroed summary).
4. Derive `PartialEq, Eq` to support `assert_eq!` in tests.

### Integration

- Add `pub mod vulnerability_summary;` to `modules/fundamental/src/advisory/model/mod.rs`
- Add `pub use vulnerability_summary::VulnerabilitySummary;` re-export in the same `mod.rs`

---

## File 2: Modify `modules/fundamental/src/advisory/service/advisory.rs`

### Purpose

Add the `extract_vulnerability_summary()` method to `AdvisoryService`.

### Changes

1. Add import for the new model type and `HashMap`:

```rust
use crate::advisory::model::VulnerabilitySummary;
use std::collections::HashMap;
```

2. Add import for the ingestor result type (verify actual path via Serena/Grep):

```rust
use trustify_module_ingestor::service::AdvisoryIngestResult;
```

3. Add the extractor method to the `impl AdvisoryService` block:

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Processes the nullable fields of `AdvisoryIngestResult` (cves,
/// affected_packages, severity_counts) and produces a `VulnerabilitySummary`
/// with non-optional fields populated with sensible defaults for any
/// missing data.
pub fn extract_vulnerability_summary(
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Guard: cves may be None when the advisory has no CVE references.
    let cve_list = result.cves.clone().unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Guard: affected_packages may be None for advisories without
    // package-level detail.
    let affected_package_count = result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Guard: severity_counts may be None when severity metadata is absent.
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

### Design Decisions

- The method is a **pure function** (no `&self`, no database access) since it transforms
  in-memory data. This follows the task description which says it "reads" ingest results --
  it does not query the database for them. If sibling methods are all `&self` methods,
  the method could take `&self` for consistency even if unused, but the cleaner approach
  is a static/associated function.
- Returns `Result<T, AppError>` per the project convention, even though the current
  implementation is infallible -- this maintains API consistency and allows future
  error-producing logic (e.g., validation) without a breaking change.
- Uses `clone()` for `cve_list` and `severity_breakdown` because the method takes
  `&AdvisoryIngestResult` by reference. If performance were critical, an owned variant
  could accept `AdvisoryIngestResult` by value.

---

## File 3: Create `tests/api/advisory_summary.rs`

### Purpose

Integration tests for the vulnerability summary extractor. Cover all acceptance criteria
and test requirements.

### Changes

1. Add test module with the following test functions:

```rust
use std::collections::HashMap;
use trustify_module_fundamental::advisory::model::VulnerabilitySummary;
use trustify_module_fundamental::advisory::service::AdvisoryService;
use trustify_module_ingestor::service::AdvisoryIngestResult;

/// Verifies that a fully-populated AdvisoryIngestResult produces a summary
/// with all fields correctly extracted.
#[test]
fn test_extract_summary_fully_populated() {
    // Given a fully-populated AdvisoryIngestResult
    let result = AdvisoryIngestResult {
        cves: Some(vec![
            "CVE-2024-1234".to_string(),
            "CVE-2024-5678".to_string(),
        ]),
        affected_packages: Some(vec![
            /* construct AffectedPackage instances per the actual struct */
        ]),
        severity_counts: Some(HashMap::from([
            ("critical".to_string(), 1),
            ("high".to_string(), 3),
        ])),
        ..Default::default() // or explicit fields depending on struct definition
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result)
        .expect("extraction should succeed");

    // Then all fields are correctly populated
    assert_eq!(summary.cve_count, 2);
    assert_eq!(summary.cve_list, vec!["CVE-2024-1234", "CVE-2024-5678"]);
    assert_eq!(summary.affected_package_count, /* expected count */);
    assert_eq!(summary.severity_breakdown.get("critical"), Some(&1));
    assert_eq!(summary.severity_breakdown.get("high"), Some(&3));
}

/// Verifies that an AdvisoryIngestResult with all-None fields produces a
/// zeroed summary without panicking.
#[test]
fn test_extract_summary_all_none() {
    // Given an AdvisoryIngestResult with all nullable fields set to None
    let result = AdvisoryIngestResult {
        cves: None,
        affected_packages: None,
        severity_counts: None,
        ..Default::default()
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result)
        .expect("extraction should succeed even with all-None fields");

    // Then all fields have sensible defaults (zeroed)
    assert_eq!(summary.cve_count, 0);
    assert_eq!(summary.cve_list, Vec::<String>::new());
    assert_eq!(summary.affected_package_count, 0);
    assert_eq!(summary.severity_breakdown, HashMap::new());
}

/// Verifies that each None field defaults independently when other fields
/// are populated (mixed Some/None).
#[test]
fn test_extract_summary_mixed_some_none() {
    // Given cves is Some but affected_packages and severity_counts are None
    let result = AdvisoryIngestResult {
        cves: Some(vec!["CVE-2024-9999".to_string()]),
        affected_packages: None,
        severity_counts: None,
        ..Default::default()
    };

    // When extracting the vulnerability summary
    let summary = AdvisoryService::extract_vulnerability_summary(&result)
        .expect("extraction should succeed with mixed fields");

    // Then cve fields are populated and others are defaulted
    assert_eq!(summary.cve_count, 1);
    assert_eq!(summary.cve_list, vec!["CVE-2024-9999"]);
    assert_eq!(summary.affected_package_count, 0);
    assert_eq!(summary.severity_breakdown, HashMap::new());
}

/// Verifies that cve_count is always consistent with cve_list.len().
#[test]
fn test_cve_count_matches_cve_list_length() {
    // Given various CVE list sizes
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
        let result = AdvisoryIngestResult {
            cves,
            affected_packages: None,
            severity_counts: None,
            ..Default::default()
        };

        // When extracting
        let summary = AdvisoryService::extract_vulnerability_summary(&result)
            .expect("extraction should succeed");

        // Then cve_count matches cve_list.len()
        assert_eq!(
            summary.cve_count,
            summary.cve_list.len() as u32,
            "cve_count must equal cve_list.len()"
        );
    }
}
```

### Integration

- Add `mod advisory_summary;` to `tests/api/mod.rs` (or the test harness entry point)

---

## Module Registration Changes

### `modules/fundamental/src/advisory/model/mod.rs`

Add:
```rust
pub mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

### `tests/api/mod.rs` (or equivalent test harness file)

Add:
```rust
mod advisory_summary;
```

---

## Dependency Verification

The `modules/fundamental/Cargo.toml` likely already depends on `trustify-module-ingestor`
(or the ingestor types are re-exported). This would be verified by inspecting the
`Cargo.toml` dependency table. If the dependency does not exist, adding it would be
an out-of-scope change to flag in Step 9's scope containment check for user approval.

---

## Step 9 Verification Checklist

1. **Scope containment**: Verify `git diff --name-only` only shows the three files in
   scope plus `model/mod.rs` (module registration, necessary integration).
2. **Sensitive-pattern check**: Scan diff for secrets/credentials.
3. **Dead parameter detection**: No parameters are being removed; N/A.
4. **Duplication check**: Search for existing vulnerability summary or extraction logic
   in the codebase.
5. **CI checks**: Run `cargo fmt --check`, `cargo clippy`, `cargo check` (or whatever
   CONVENTIONS.md specifies).
6. **Module-level tests**: Run `cargo test -p <fundamental-crate-name>` for the crate
   containing the modified service file.
7. **Data-flow trace**: Input: `AdvisoryIngestResult` (from ingestor module) ->
   Processing: `extract_vulnerability_summary()` (null-guard + transform) ->
   Output: `VulnerabilitySummary` (consumed by email notification system, out of scope).
   The input-to-output path is complete within the extractor's responsibility.
