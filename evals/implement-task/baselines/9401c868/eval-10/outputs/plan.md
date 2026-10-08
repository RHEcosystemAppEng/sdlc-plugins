# Implementation Plan -- TC-9208

## Task Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a summary of
license types for packages within an SBOM, aggregated by category (permissive, copyleft,
unknown) with counts and deduplicated license identifier lists.

## Project Configuration Validation

- Repository Registry: trustify-backend, Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID present
- Code Intelligence: serena_backend with rust-analyzer

All required sections present. Proceed.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**Current state:** Registers routes for `/api/v2/package` (e.g., the list endpoint from
`list.rs`).

**Changes:**
- Add `pub mod license_summary;` to import the new endpoint module.
- Register the new route `GET /api/v2/sbom/{id}/license-summary` by adding it to the
  router builder, following the same pattern used for existing routes (e.g., how `list.rs`
  is registered). The route is mounted under the SBOM path scope since the endpoint
  operates on an SBOM ID, but lives in the package module since it aggregates package
  license data.

### 2. `modules/fundamental/src/package/model/mod.rs`

**Current state:** Declares `pub mod summary;` for the `PackageSummary` struct.

**Changes:**
- Add `pub mod license_summary;` to register the new model module.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**Purpose:** Define the `LicenseSummary` response struct.

**Contents:**
```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of license types for packages within an SBOM, grouped by category.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    /// Licenses classified as permissive (e.g., MIT, Apache-2.0, BSD).
    pub permissive: LicenseCategory,
    /// Licenses classified as copyleft (e.g., GPL, AGPL, LGPL).
    pub copyleft: LicenseCategory,
    /// Licenses that could not be classified into permissive or copyleft.
    pub unknown: LicenseCategory,
}

/// A single license category with a count and list of deduplicated license identifiers.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct license identifiers in this category.
    pub count: usize,
    /// Deduplicated list of SPDX license identifiers in this category.
    pub licenses: Vec<String>,
}
```

- Derive `Serialize`, `Deserialize`, `ToSchema` following sibling model patterns
  (`summary.rs`, `details.rs`).
- Add doc comments on every public struct and field per skill quality guidance.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/license-summary`.

**Contents:**
- Import `AppError` from `common/src/error.rs` for error handling.
- Import `package_license` entity from `entity/src/package_license.rs` for the JOIN query.
- Import `sbom_package` entity from `entity/src/sbom_package.rs` to join SBOM to packages.
- Import `LicenseSummary` and `LicenseCategory` from the model module.

**Handler function:**
```rust
/// Returns a categorized summary of package licenses for the given SBOM.
pub async fn get_license_summary(
    Path(sbom_id): Path<Uuid>,
    db: Extension<DatabaseConnection>,
) -> Result<Json<LicenseSummary>, AppError> {
    // 1. Verify SBOM exists -- query sbom entity by ID, return 404 if not found
    // 2. Query package_license joined through sbom_package for the given SBOM ID
    // 3. Collect all license identifiers
    // 4. Classify each license into permissive/copyleft/unknown using a categorization function
    // 5. Deduplicate within each category using HashSet
    // 6. Build and return LicenseSummary with counts derived from Vec::len()
}
```

**License classification helper:**
```rust
/// Classifies an SPDX license identifier into permissive, copyleft, or unknown.
fn classify_license(license_id: &str) -> LicenseType {
    // Known permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, Zlib
    // Known copyleft: GPL-2.0, GPL-3.0, AGPL-3.0, LGPL-2.1, LGPL-3.0, MPL-2.0, EUPL-1.2
    // Everything else: Unknown
}
```

**Error handling:** Follow the sibling pattern -- return `Result<T, AppError>` with
`.context()` wrapping on all fallible operations (DB queries, entity lookups).

**Route registration:** The handler is registered in `endpoints/mod.rs` following the
pattern from `list.rs`.

### 5. `tests/api/package_license.rs`

**Purpose:** Integration tests for the license summary endpoint.

**Contents:** Four test functions covering all Test Requirements (see `test-plan.md`
for detailed assertion approach). Tests follow sibling structural conventions (setup,
naming, test DB) but use value-based assertions per skill guidance.

### 6. `tests/api/mod.rs` (or test harness registration)

**Note:** If `tests/api/` uses a `mod.rs` or the tests `Cargo.toml` lists test targets,
the new `package_license.rs` test file must be registered. Check existing structure
(how `sbom.rs`, `advisory.rs`, `search.rs` are discovered) and follow the same pattern.
This is an out-of-scope file that would be flagged in Step 9 scope containment for user
approval.

## Data Flow Trace

1. **Input:** HTTP GET request to `/api/v2/sbom/{id}/license-summary` with SBOM UUID
   in path.
2. **Processing:**
   - Validate SBOM exists (query `sbom` entity) -- return 404 if missing.
   - Query `sbom_package` JOIN `package_license` filtered by `sbom_id`.
   - Collect license identifiers from query results.
   - Classify each license using `classify_license()`.
   - Deduplicate per category using `HashSet`.
   - Build `LicenseSummary` response with counts from `Vec::len()`.
3. **Output:** JSON response with `LicenseSummary` struct, status 200.

All stages are connected. The query path (sbom -> sbom_package -> package_license) uses
existing entity definitions. No missing stages.

## Implementation Notes Adherence

- Follow existing endpoint pattern from `list.rs` (handler signature, error return type,
  route registration pattern).
- Use `package_license` entity from `entity/src/package_license.rs` for the JOIN query.
- Error handling with `AppError` and `.context()` wrapping -- matches sibling pattern.

## Scope Containment

Files strictly within scope: the 2 files to modify and 3 files to create listed in the
task. Any additional files (e.g., test module registration, Cargo.toml dependency
additions) would be flagged in Step 9 for user approval before committing.
