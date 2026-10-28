# Implementation Plan: TC-9211

## Task Summary

Add a vulnerability summary extractor (`extract_vulnerability_summary()`) that processes
`AdvisoryIngestResult` records from the ingestor module and produces a
`VulnerabilitySummary` struct suitable for email digest notifications. The extractor must
handle all nullable fields gracefully without panicking.

## Repository

trustify-backend

## Target Branch

main

---

## Files to Create

### 1. `modules/fundamental/src/advisory/model/vulnerability_summary.rs`

**Purpose**: Define the `VulnerabilitySummary` output struct with non-optional fields.

**Changes**:

- Define a new public struct `VulnerabilitySummary` with the following fields:
  - `cve_count: u32` -- total number of CVE identifiers
  - `cve_list: Vec<String>` -- the CVE identifiers themselves
  - `affected_package_count: u32` -- number of affected packages
  - `severity_breakdown: HashMap<String, u32>` -- counts per severity level (e.g., "critical": 3, "high": 7)
- Derive `Debug`, `Clone`, `Default`, `Serialize`, `Deserialize` (following existing model patterns like `AdvisorySummary` and `SbomSummary`).
- Implement `Default` via derive -- this gives `cve_count: 0`, `cve_list: vec![]`, `affected_package_count: 0`, `severity_breakdown: HashMap::new()`, which matches the "sensible defaults" requirement.
- Add a doc comment (`///`) explaining the struct's purpose: output of the vulnerability summary extractor, used for advisory digest emails.
- Add doc comments on each field explaining what it represents and its default behavior when source data is absent.

**Module registration**:

- Add `pub mod vulnerability_summary;` to `modules/fundamental/src/advisory/model/mod.rs` and re-export the struct.

### 2. `tests/api/advisory_summary.rs`

**Purpose**: Integration tests for the `extract_vulnerability_summary()` method.

**Changes**:

- Add `mod advisory_summary;` to the test module's root (likely `tests/api/mod.rs` or via `Cargo.toml` test target configuration).
- Implement the following test cases (each with `///` doc comment and given-when-then structure):

#### Test: `test_extract_summary_fully_populated`
- **Given**: An `AdvisoryIngestResult` with all fields populated:
  - `cves: Some(vec!["CVE-2024-1234".to_string(), "CVE-2024-5678".to_string()])`
  - `affected_packages: Some(vec![AffectedPackage { name: "openssl".into(), .. }, AffectedPackage { name: "libcurl".into(), .. }])`
  - `severity_counts: Some(HashMap::from([("critical".to_string(), 1), ("high".to_string(), 2)]))`
- **When**: Call `extract_vulnerability_summary(&result)`
- **Then**: Assert `cve_count == 2`, `cve_list == ["CVE-2024-1234", "CVE-2024-5678"]`, `affected_package_count == 2`, `severity_breakdown == {"critical": 1, "high": 2}`
- **Also assert**: `cve_count == cve_list.len() as u32` (acceptance criterion: count matches list length)

#### Test: `test_extract_summary_all_none`
- **Given**: An `AdvisoryIngestResult` with `cves: None`, `affected_packages: None`, `severity_counts: None`
- **When**: Call `extract_vulnerability_summary(&result)`
- **Then**: Assert `cve_count == 0`, `cve_list.is_empty()`, `affected_package_count == 0`, `severity_breakdown.is_empty()`
- Validates the "should return zeroed summary" requirement.

#### Test: `test_extract_summary_mixed_some_none`
- **Given**: An `AdvisoryIngestResult` with:
  - `cves: Some(vec!["CVE-2024-9999".to_string()])`
  - `affected_packages: None`
  - `severity_counts: None`
- **When**: Call `extract_vulnerability_summary(&result)`
- **Then**: Assert `cve_count == 1`, `cve_list == ["CVE-2024-9999"]`, `affected_package_count == 0`, `severity_breakdown.is_empty()`
- Validates each `None` field defaults independently without affecting populated fields.

#### Test: `test_cve_count_consistent_with_list`
- **Given**: An `AdvisoryIngestResult` with `cves: Some(vec!["CVE-2024-0001".to_string(), "CVE-2024-0002".to_string(), "CVE-2024-0003".to_string()])`, other fields `None`
- **When**: Call `extract_vulnerability_summary(&result)`
- **Then**: Assert `summary.cve_count == summary.cve_list.len() as u32`
- Explicit acceptance criterion test: count always matches list length.

---

## Files to Modify

### 3. `modules/fundamental/src/advisory/service/advisory.rs`

**Purpose**: Add the `extract_vulnerability_summary()` method to `AdvisoryService`.

**Changes**:

- Add import for `VulnerabilitySummary` from `crate::advisory::model::vulnerability_summary`.
- Add import for `AdvisoryIngestResult` from the ingestor crate (the `AdvisoryIngestResult` struct is defined in `modules/ingestor/src/service/mod.rs`; the import path depends on the ingestor crate's public exports, likely `trustify_ingestor::service::AdvisoryIngestResult` or similar).
- Add import for `std::collections::HashMap`.
- Add a new public method to `AdvisoryService`:

```rust
/// Extracts a vulnerability summary from an advisory ingest result.
///
/// Processes the optional fields of `AdvisoryIngestResult` (CVEs, affected
/// packages, severity counts) into a flat, non-optional `VulnerabilitySummary`
/// suitable for digest email rendering.
///
/// All `None` fields are treated as empty/zero -- the method never panics on
/// missing data.
pub fn extract_vulnerability_summary(
    result: &AdvisoryIngestResult,
) -> Result<VulnerabilitySummary, AppError> {
    // Handle cves: Option<Vec<String>>
    let cve_list = result.cves.clone().unwrap_or_default();
    let cve_count = cve_list.len() as u32;

    // Handle affected_packages: Option<Vec<AffectedPackage>>
    let affected_package_count = result
        .affected_packages
        .as_ref()
        .map(|pkgs| pkgs.len() as u32)
        .unwrap_or(0);

    // Handle severity_counts: Option<HashMap<String, u32>>
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

**Pattern conformance**: The method follows the existing AdvisoryService pattern:
- Returns `Result<T, AppError>` (matching `advisory.rs` convention)
- Takes a reference to input data rather than consuming it
- Uses `.context()` wrapping if any fallible operations are added in the future
- The method is a pure transformation (no DB access needed), but wraps in `Result` for consistency with the service layer pattern

**Why `Result<T, AppError>` even though the method is infallible**: The existing service methods uniformly return `Result<T, AppError>`. Maintaining this signature keeps the API consistent and allows future changes (e.g., adding validation that could fail) without a breaking signature change.

---

## Additional Module Registration

### `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod vulnerability_summary;` and a re-export:
```rust
pub mod vulnerability_summary;
pub use vulnerability_summary::VulnerabilitySummary;
```

This follows the pattern established by `summary.rs` and `details.rs` in the same directory.

---

## Dependency Considerations

- The `AdvisoryIngestResult` struct lives in the `ingestor` crate (`modules/ingestor/src/service/mod.rs`). The `fundamental` crate must already depend on `ingestor` (or the shared types must be in `common`) for this cross-module reference to work. Check `modules/fundamental/Cargo.toml` for an existing dependency on the ingestor crate.
- If the dependency does not exist, the struct's fields would need to be passed as individual parameters rather than taking `&AdvisoryIngestResult` directly, to avoid introducing a new cross-crate dependency. In that case, the method signature would change to accept the three optional fields individually. However, the task description implies direct consumption of `AdvisoryIngestResult`, so the dependency likely already exists.

---

## Handling Nullable Fields from AdvisoryIngestResult

The `AdvisoryIngestResult` struct uses `Option<T>` for all three aggregate fields because:

1. **Data crosses a module boundary**: The ingest result is produced by the ingestor module and consumed by the fundamental module. The producer may return partial results depending on the advisory format parsed.
2. **Schema allows null**: Not all advisory formats contain CVE references, package-level detail, or severity metadata. The `Option` type accurately models this real-world variability.
3. **Independent nullability**: Each field may be `None` independently -- an advisory could have CVEs but no package detail, or severity counts but no CVE list.

The extractor handles each nullable field using Rust idiomatic patterns:

| Field | Type | Guard Pattern | Rationale |
|-------|------|---------------|-----------|
| `cves` | `Option<Vec<String>>` | `.clone().unwrap_or_default()` | Produces an owned `Vec<String>` (needed for the output struct); default is `vec![]` |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | `.as_ref().map(\|pkgs\| pkgs.len() as u32).unwrap_or(0)` | Only the count is needed, so borrow with `as_ref()` to avoid cloning the full vec; default is `0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | `.clone().unwrap_or_default()` | The entire map is transferred to the output struct; default is `HashMap::new()` |

No `.unwrap()` is ever used on `Option` fields. The method is guaranteed not to panic on any combination of `None` inputs.
