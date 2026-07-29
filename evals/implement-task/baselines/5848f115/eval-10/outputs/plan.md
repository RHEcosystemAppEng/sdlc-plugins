# Implementation Plan for TC-9208: Add package license summary endpoint with tests

## Overview

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns license counts
categorized by type (permissive, copyleft, unknown) with deduplicated license identifier
lists for each category.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

Register the new `license_summary` route under the existing package endpoints router.
Import the new `license_summary` module and add its route to the Axum router, following
the same pattern used in `modules/fundamental/src/sbom/endpoints/mod.rs` for registering
sub-routes (e.g., how `list.rs` and `get.rs` are registered).

### 2. `modules/fundamental/src/package/model/mod.rs`

Add `pub mod license_summary;` declaration to expose the new model module, following the
same pattern as the existing `pub mod summary;` declaration.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

Define the `LicenseSummary` response struct:

```rust
/// Response struct for the license summary endpoint, categorizing licenses by type.
#[derive(Debug, Serialize, Deserialize)]
pub struct LicenseSummary {
    pub permissive: LicenseCategory,
    pub copyleft: LicenseCategory,
    pub unknown: LicenseCategory,
}

/// A single category of licenses with a count and deduplicated list of identifiers.
#[derive(Debug, Serialize, Deserialize)]
pub struct LicenseCategory {
    pub count: usize,
    pub licenses: Vec<String>,
}
```

Include classification logic (or a helper function) that maps known SPDX license
identifiers to their category (permissive, copyleft, or unknown). Use the
`package_license` entity from `entity/src/package_license.rs` as the data source.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

Implement the GET handler:

- Follow the pattern from `modules/fundamental/src/package/endpoints/list.rs` for handler
  structure and error handling
- Accept the SBOM ID as a path parameter
- Query the `package_license` entity joined through `sbom_package` to get all licenses
  for packages in the given SBOM
- Return 404 via `AppError` with `.context()` wrapping when the SBOM ID does not exist
- Deduplicate licenses within each category using a `HashSet`
- Return the `LicenseSummary` response struct as JSON

### 5. `tests/api/package_license.rs`

Create integration tests following sibling conventions from `tests/api/advisory.rs` and
`tests/api/sbom.rs` for structure and naming, but using value-based assertions per the
skill's quality guidance (see test-plan.md for details).

## Implementation Sequence

1. Create the `LicenseSummary` and `LicenseCategory` model structs
2. Create the endpoint handler with license classification logic
3. Register the route in the package endpoints module
4. Add the `pub mod license_summary;` declaration in the model module
5. Write integration tests (see test-plan.md)
6. Run `cargo test` to verify all tests pass
7. Run CI checks from CONVENTIONS.md if present
8. Verify all acceptance criteria are satisfied
