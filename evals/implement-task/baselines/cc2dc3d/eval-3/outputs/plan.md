# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation follows the existing severity filter pattern from the advisory module and reuses shared query helpers.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add license query parameter extraction and filtering to the package list endpoint.

**Changes:**

- **Add `license` field to the `Query` struct**: Following the same pattern used in `modules/fundamental/src/advisory/endpoints/list.rs` for the `severity` filter, add an optional `license` field of type `Option<String>` to the existing `Query` struct that handles query parameter deserialization for `GET /api/v2/package`.

  ```rust
  // In the Query struct (following advisory list.rs severity pattern):
  pub license: Option<String>,
  ```

- **Pass the license filter to the service layer**: In the list handler function, extract `query.license` and pass it to `PackageService::list()` (or equivalent method) as an additional filter parameter. This mirrors how the advisory list endpoint passes its `severity` filter to `AdvisoryService`.

- **Validation**: Add validation for the `license` parameter value. If the value is present but contains invalid characters or is empty after splitting, return a `400 Bad Request` response using the project's `AppError` enum with `.context()` wrapping.

- **No changes to response shape**: The handler continues to return `PaginatedResults<PackageSummary>` unchanged. Only the input query parameters are extended.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filter logic to the PackageService list method.

**Changes:**

- **Accept the license filter parameter**: Modify the `list` method (or equivalent) in `PackageService` to accept an additional `license: Option<String>` parameter.

- **Reuse `apply_filter` from `common/src/db/query.rs`**: When the `license` parameter is `Some`, call the existing `apply_filter` function to handle comma-separated multi-value parsing and SQL `IN` clause generation. This is the critical reuse point -- `apply_filter` already handles splitting comma-separated values and generating the correct SQL filter clause. Do NOT write custom parsing logic for splitting the comma-separated string.

  ```rust
  // Reuse apply_filter directly:
  if let Some(license) = &license {
      apply_filter(query, "license", license);
  }
  ```

- **Join through `package_license` entity**: Use the existing `entity::package_license` entity (from `entity/src/package_license.rs`) to construct the JOIN between the `package` table and the `package_license` table. This uses SeaORM's relation/join capabilities rather than writing raw SQL. The entity already defines the relationship and column mappings needed for the JOIN.

  ```rust
  // Use the existing entity for the JOIN:
  use entity::package_license;
  // ... join through package_license when license filter is active
  ```

- **Conditional JOIN**: Only add the JOIN when the `license` filter is present, to avoid unnecessary JOINs when no license filter is applied. This follows the same conditional pattern used for the severity filter in the advisory service.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter feature.

**Test cases (following sibling test conventions in `tests/api/`):**

All tests use `assert_eq!(resp.status(), StatusCode::OK)` (or `StatusCode::BAD_REQUEST` for error cases) followed by body deserialization, consistent with the existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Every test function includes a `///` doc comment and given-when-then section comments.

1. **`test_list_packages_filter_single_license`**
   - Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist in the database
   - When: `GET /api/v2/package?license=MIT`
   - Then: response contains only packages with MIT license; assert on specific package identifiers (not just count)

2. **`test_list_packages_filter_multiple_licenses`**
   - Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response contains packages matching either MIT or Apache-2.0; assert on specific identifiers

3. **`test_list_packages_no_license_filter`**
   - Given: packages with various licenses exist
   - When: `GET /api/v2/package` (no license parameter)
   - Then: response contains all packages unchanged (no regression); validate total_count and items

4. **`test_list_packages_invalid_license`**
   - Given: the endpoint is available
   - When: `GET /api/v2/package?license=` (empty value or invalid)
   - Then: response is 400 Bad Request

**Module registration:** The new test file must be registered in `tests/api/` module structure (likely via a `mod` declaration in `tests/api/mod.rs` or as a separate test binary in `tests/Cargo.toml`).

## Code Reuse Summary

| Reuse Candidate | How It Is Used |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in `service/mod.rs` to parse comma-separated license values and generate SQL IN clause. No new parsing logic written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as structural guide: the `Query` struct pattern with an optional filter field and its propagation to the service layer is replicated for the license filter in `package/endpoints/list.rs`. |
| `entity/src/package_license.rs` | Used for the SeaORM JOIN between `package` and `package_license` tables in `service/mod.rs`, avoiding raw SQL. |

## Data Flow

```
HTTP Request (GET /api/v2/package?license=MIT,Apache-2.0)
  -> list.rs: Query struct deserializes `license` parameter
  -> list.rs: passes license value to PackageService::list()
  -> service/mod.rs: calls apply_filter() with license value (comma-split + IN clause)
  -> service/mod.rs: JOINs through package_license entity
  -> Database: filtered query executes
  -> service/mod.rs: returns PaginatedResults<PackageSummary>
  -> list.rs: serializes response (unchanged shape)
  -> HTTP Response (200 OK with filtered results)
```

## Scope Boundaries

- Only the three files listed above are modified or created
- No changes to response types, entity definitions, or route registration
- No new utility functions that duplicate `apply_filter` behavior
- No changes to `entity/src/package_license.rs` (used as-is for JOINs)
- No changes to `common/src/db/query.rs` (used as-is for filtering)
