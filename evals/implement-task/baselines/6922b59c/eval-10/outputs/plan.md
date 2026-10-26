# Implementation Plan for TC-9208

## Task Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns a categorized
summary of package license types (permissive, copyleft, unknown) for packages within an
SBOM, including counts and deduplicated license identifier lists.

## Repository

trustify-backend (Rust, Axum + SeaORM)

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

**What to change:** Register the new `license_summary` route in the existing route
registration block. Following the sibling pattern from `list.rs` and `get.rs` (which
are already registered here), add a `.route()` call for the new
`GET /api/v2/sbom/{id}/license-summary` path pointing to the handler in the new
`license_summary` endpoint module. Also add `pub mod license_summary;` to import the
new endpoint module.

### 2. `modules/fundamental/src/package/model/mod.rs`

**What to change:** Add `pub mod license_summary;` to expose the new `LicenseSummary`
response struct module.

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

**What to create:** Define the `LicenseSummary` response struct and its nested
`LicenseCategorySummary` struct.

```rust
/// Categorized summary of package licenses within an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseSummary {
    /// Licenses classified as permissive (e.g., MIT, Apache-2.0, BSD).
    pub permissive: LicenseCategorySummary,
    /// Licenses classified as copyleft (e.g., GPL, AGPL, LGPL).
    pub copyleft: LicenseCategorySummary,
    /// Licenses that could not be classified into permissive or copyleft.
    pub unknown: LicenseCategorySummary,
}

/// Count and deduplicated list of license identifiers for a single category.
#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]
pub struct LicenseCategorySummary {
    /// Number of distinct license identifiers in this category.
    pub count: usize,
    /// Deduplicated list of license identifiers (e.g., ["MIT", "Apache-2.0"]).
    pub licenses: Vec<String>,
}
```

Include a helper function or `impl` block for classification logic that maps known
SPDX identifiers to categories (permissive, copyleft, unknown). Use `HashSet` for
deduplication before converting to `Vec<String>`.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

**What to create:** The GET handler for `/api/v2/sbom/{id}/license-summary`.

Key implementation details:
- Follow the sibling pattern from `modules/fundamental/src/package/endpoints/list.rs`
  for handler structure
- Accept the SBOM ID as a path parameter via Axum's `Path<Uuid>` extractor
- Return `Result<Json<LicenseSummary>, AppError>` following the project's error
  handling convention
- Query logic:
  1. Verify the SBOM exists using the SBOM entity -- return 404 (`AppError::NotFound`)
     if it does not
  2. JOIN `sbom_package` with `package_license` to retrieve all licenses for packages
     in the given SBOM, using the `package_license` entity from
     `entity/src/package_license.rs`
  3. Classify each license identifier into permissive/copyleft/unknown
  4. Deduplicate licenses within each category using `HashSet`
  5. Build and return the `LicenseSummary` response
- Wrap all database errors with `.context()` per project convention

### 5. `tests/api/package_license.rs`

**What to create:** Integration tests for the new endpoint. See `outputs/test-plan.md`
for detailed test assertion approach.

Structure follows sibling files `tests/api/sbom.rs` and `tests/api/advisory.rs` for
test setup, HTTP client configuration, and database bootstrapping patterns. However,
assertion style will use value-based assertions per the skill's quality guidance (see
`outputs/conventions.md` for the conflict analysis).

## Data Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/license-summary` with SBOM UUID
   path parameter
2. **Validation**: Verify SBOM exists via `sbom` entity query; return 404 if not found
3. **Processing**: JOIN `sbom_package` + `package_license` tables, classify licenses
   into categories, deduplicate with `HashSet`
4. **Output**: JSON response with `LicenseSummary` struct containing three categories,
   each with count and license list

All stages are connected; no missing or disconnected stages.

## Dependencies

None -- the task has no prerequisite tasks.
