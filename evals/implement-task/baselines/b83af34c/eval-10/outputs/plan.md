# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated license identifier
lists. Also add integration tests for the new endpoint.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

Register the new `license_summary` route in the existing route configuration. Add a
`mod license_summary;` declaration and wire the handler into the Axum router alongside
the existing package endpoints. Follow the same route registration pattern used in
`modules/fundamental/src/sbom/endpoints/mod.rs` and
`modules/fundamental/src/advisory/endpoints/mod.rs`.

### 2. `modules/fundamental/src/package/model/mod.rs`

Add `pub mod license_summary;` to expose the new model module, following the same
pattern as `pub mod summary;` already present in this file.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

Create the `LicenseSummary` response struct:

```rust
/// Categorized summary of package licenses within an SBOM.
#[derive(Debug, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseSummary {
    /// Licenses classified as permissive (e.g., MIT, Apache-2.0).
    pub permissive: LicenseCategory,
    /// Licenses classified as copyleft (e.g., GPL-3.0, AGPL-3.0).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be classified.
    pub unknown: LicenseCategory,
}

/// A single license category with count and deduplicated identifiers.
#[derive(Debug, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct licenses in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers.
    pub licenses: Vec<String>,
}
```

Add documentation comments on both structs and all fields.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

Create the GET handler following the pattern from `list.rs`:

- Accept path parameter `{id}` (SBOM ID)
- Query `package_license` entity joined through `sbom_package` for the given SBOM ID
- Return 404 via `AppError` with `.context()` if SBOM does not exist
- Classify each license as permissive, copyleft, or unknown
- Deduplicate licenses within each category using a `HashSet`
- Return `LicenseSummary` as JSON

Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping,
consistent with all other handlers in the codebase.

### 5. `tests/api/package_license.rs`

Create integration tests (detailed in test-plan.md). Follow the sibling test structure
from `tests/api/advisory.rs` and `tests/api/sbom.rs` for setup, naming, and
organization -- but use value-based assertions per skill guidance.

## Additional Considerations

- The `package_license` entity at `entity/src/package_license.rs` provides the
  underlying data model for the JOIN query.
- Query helpers from `common/src/db/query.rs` may be reused for filtering.
- No new dependencies need to be added since `modules/fundamental` already depends
  on the `entity` and `common` crates.
- Documentation in `docs/api.md` should be updated to include the new endpoint.
