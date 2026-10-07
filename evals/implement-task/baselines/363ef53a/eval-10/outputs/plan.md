# Implementation Plan: TC-9208 -- Add Package License Summary Endpoint

## Overview

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated license identifiers per
category. Also add integration tests for the new endpoint.

## Files to Modify

### `modules/fundamental/src/package/endpoints/mod.rs`

Register the new `/license-summary` route in the existing route configuration. Following
the pattern from the sibling `list.rs` endpoint, add a `.route()` call mounting the
`license_summary::get_license_summary` handler at `/api/v2/sbom/{id}/license-summary`.
Import the new `license_summary` submodule.

### `modules/fundamental/src/package/model/mod.rs`

Add `pub mod license_summary;` to expose the new model module, following the existing
`pub mod summary;` pattern already present for `PackageSummary`.

## Files to Create

### `modules/fundamental/src/package/model/license_summary.rs`

Define the response struct:

```rust
/// Categorized summary of package licenses within an SBOM.
#[derive(Debug, Serialize, Deserialize)]
pub struct LicenseSummary {
    /// Licenses classified as permissive (e.g., MIT, Apache-2.0).
    pub permissive: LicenseCategory,
    /// Licenses classified as copyleft (e.g., GPL-3.0, AGPL-3.0).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be classified.
    pub unknown: LicenseCategory,
}

/// A single license category with count and deduplicated identifiers.
#[derive(Debug, Serialize, Deserialize)]
pub struct LicenseCategory {
    /// Number of unique licenses in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers.
    pub licenses: Vec<String>,
}
```

Use `serde` derive macros consistent with sibling model files (`summary.rs`, `details.rs`).

### `modules/fundamental/src/package/endpoints/license_summary.rs`

Implement the handler:

- Follow the endpoint pattern from `modules/fundamental/src/package/endpoints/list.rs`
- Accept the SBOM ID as a path parameter
- Query `package_license` entity via `entity/src/package_license.rs` joined through
  `sbom_package` to scope results to the given SBOM
- Return `Result<Json<LicenseSummary>, AppError>` with `.context()` wrapping on errors
- Return 404 via `AppError` when the SBOM ID does not exist
- Classify licenses into permissive/copyleft/unknown categories
- Deduplicate license identifiers within each category using `HashSet`

### `tests/api/package_license.rs`

Create integration tests following sibling test conventions from `tests/api/advisory.rs`
and `tests/api/sbom.rs` for structure, naming, and setup/teardown, but using value-based
assertions per skill guidance (see test-plan.md for details).

Four test functions covering:
1. Valid SBOM with known licenses returns correct categorized counts and identifiers
2. Non-existent SBOM ID returns 404
3. SBOM with no packages returns zeros and empty lists
4. Duplicate licenses within a category are counted only once

## Data Flow

1. **Input**: HTTP GET request with SBOM ID path parameter
2. **Validation**: Check SBOM exists; return 404 if not
3. **Query**: JOIN `sbom_package` and `package_license` tables filtered by SBOM ID
4. **Processing**: Classify each license identifier, deduplicate per category via HashSet
5. **Output**: Serialize `LicenseSummary` as JSON response

## Dependencies

No prerequisite tasks. The `package_license` entity already exists at
`entity/src/package_license.rs`.
