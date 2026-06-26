# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation follows the existing severity filter pattern from the advisory list endpoint and reuses the shared `apply_filter` utility.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles the `GET /api/v2/package` endpoint with existing query parameter extraction and service invocation. Contains a `Query` struct for deserializing query parameters (pagination, sorting, existing filters).

**Changes:**

- **Add `license` field to the `Query` struct**: Add an `Option<String>` field named `license` to the existing query parameters struct, following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`. The field is optional so that requests without the parameter continue to return all packages.

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing fields (pagination, sorting, etc.)
      /// Optional license filter — single SPDX identifier or comma-separated list.
      pub license: Option<String>,
  }
  ```

- **Pass the license filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as a new parameter. Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string into individual values and build the SQL IN clause. This is the same approach used by the advisory severity filter.

  ```rust
  use common::db::query::apply_filter;
  
  // Inside the handler:
  let license_filter = query.license.as_deref();
  // Pass to service method
  let results = package_service
      .list(/* existing params */, license_filter)
      .await
      .context("failed to list packages")?;
  ```

- **Add input validation**: If the `license` parameter is present but contains empty strings after splitting (e.g., `license=,` or `license=MIT,,Apache-2.0`), return a 400 Bad Request with a descriptive error message. This follows the error handling convention of `Result<T, AppError>` with `.context()` wrapping.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries the `package` table and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add `license` parameter to the `list` method signature**: Accept an `Option<&str>` parameter for the license filter.

  ```rust
  pub async fn list(
      &self,
      // ... existing parameters
      license: Option<&str>,
  ) -> Result<PaginatedResults<PackageSummary>, AppError> {
  ```

- **Build the license filter using `apply_filter`**: When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate a SQL `IN` clause. This reuses the exact same utility that the advisory severity filter uses — no new parsing or filtering logic is needed.

  ```rust
  use common::db::query::apply_filter;
  use entity::package_license;
  
  // Inside the list method, after building the base query:
  if let Some(license_value) = license {
      let license_values = apply_filter(license_value);
      // JOIN with package_license entity and filter
      query = query
          .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
          .filter(package_license::Column::License.is_in(license_values));
  }
  ```

- **Use `entity::package_license` for the JOIN**: The `package_license` entity in `entity/src/package_license.rs` already maps the package-to-license relationship. Use its SeaORM relation definition to perform the JOIN rather than writing raw SQL. This follows the existing ORM conventions of the codebase.

- **Handle deduplication**: Since a package may have multiple licenses, the INNER JOIN could produce duplicate package rows. Add `.distinct()` to the query to ensure each package appears once in the results, even when it matches multiple license values.

- **Validate license values**: After `apply_filter` splits the comma-separated input, validate that each value is non-empty. If any value is empty, return `Err(AppError::BadRequest("Invalid license filter value"))`.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on the package list endpoint.

**Structure:** Follow the existing test conventions observed in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Validate `total_count`, `items.len()`, and specific item field values
- Follow `test_<endpoint>_<scenario>` naming convention
- Add documentation comment (`///`) before every test function
- Use given-when-then section comments for non-trivial tests

**Test cases:**

```rust
/// Verifies that filtering packages by a single license returns only matching packages.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    // When: GET /api/v2/package?license=MIT
    // Then: response contains only MIT-licensed packages, status 200
    // Assert on specific package names/identifiers, not just count
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given: test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: response contains packages with MIT OR Apache-2.0 licenses, status 200
    // Assert on specific package identifiers to verify correct filtering
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: test database seeded with packages having various licenses
    // When: GET /api/v2/package (no license parameter)
    // Then: response contains all packages, status 200
    // Assert total_count matches expected full count
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_filter() {
    // Given: test database with seeded packages
    // When: GET /api/v2/package?license=,
    // Then: response status is 400 Bad Request
}
```

**Test registration:** The new test file must be registered in `tests/api/mod.rs` (or equivalent test module file) so that `cargo test` discovers it.

## Integration Points

- **Module registration**: No new routes or modules are being added. The existing `GET /api/v2/package` route in `modules/fundamental/src/package/endpoints/mod.rs` continues to use the same handler function; only the handler's internal logic changes to accept and process the new query parameter.
- **Response shape**: `PaginatedResults<PackageSummary>` remains unchanged. The `license` parameter only affects which packages are included in the results, not the structure of the response.
- **Backward compatibility**: The `license` parameter is `Option<String>`, so existing API consumers that do not provide it will continue to receive the full unfiltered package list.

## Data-Flow Trace

1. **Input**: HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at the Axum handler in `list.rs`.
2. **Parsing**: Axum deserializes query params into the `Query` struct; `license` field populated as `Some("MIT,Apache-2.0")`.
3. **Processing**: Handler passes `license` to `PackageService::list()`. Service calls `apply_filter("MIT,Apache-2.0")` which returns `["MIT", "Apache-2.0"]`. Service builds SeaORM query with INNER JOIN on `package_license` table and `WHERE license IN ('MIT', 'Apache-2.0')`.
4. **Output**: Query executes, results wrapped in `PaginatedResults<PackageSummary>`, returned as JSON response with status 200.

All stages are connected end-to-end.
