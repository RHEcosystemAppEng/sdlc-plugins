# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing infrastructure throughout: the `apply_filter` query helper for parameter parsing, the advisory severity filter as a structural template, and the `package_license` entity for the JOIN query.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add license query parameter extraction and filtering to the package list endpoint handler.

**Changes:**

- **Add `license` field to the `Query` struct**: Following the same pattern used in `modules/fundamental/src/advisory/endpoints/list.rs` for the `severity` filter, add an optional `license` field of type `Option<String>` to the existing `Query` struct (the Axum query parameter extractor). This field captures the raw query string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing fields (pagination, sorting, etc.)
      pub license: Option<String>,
  }
  ```

- **Pass the license filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter. Do NOT parse or split the comma-separated values here -- that responsibility belongs to the `apply_filter` helper in the service/query layer.

- **Validation**: Add validation for the license parameter value. If the value is present but empty or contains invalid characters, return a 400 Bad Request using the existing `AppError` pattern from `common/src/error.rs`. Follow the same `.context()` error wrapping convention used in sibling endpoint handlers.

- **No changes to response shape**: The handler continues to return `PaginatedResults<PackageSummary>` -- only the input extraction changes.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering logic to the PackageService list method.

**Changes:**

- **Add license parameter to the `list` method signature**: Add an `Option<String>` parameter for the license filter value. This matches how the advisory service accepts its `severity` filter.

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`**: When the `license` parameter is `Some`, call `apply_filter` to handle parsing the comma-separated string into individual values and generating the appropriate SQL `IN` clause. This is the same function used throughout the codebase for multi-value query parameter filtering. Do NOT write custom comma-splitting or SQL generation logic -- reuse `apply_filter` directly.

  ```rust
  use common::db::query::apply_filter;

  // Inside the list method:
  if let Some(license) = license_filter {
      apply_filter(&mut query, "license", &license);
  }
  ```

- **JOIN with `package_license` entity**: Use the `package_license` entity from `entity/src/package_license.rs` to join the `package` table with the `package_license` table when filtering. This entity already maps the relationship between packages and their licenses via SeaORM. Use SeaORM's `.join()` or `.inner_join()` with the entity's `Relation` definition rather than writing raw SQL.

  ```rust
  use entity::package_license;

  // When license filter is present, add the JOIN:
  query = query.join(
      JoinType::InnerJoin,
      package_license::Relation::Package.def().rev(),
  );
  ```

- **Ensure no duplicate results**: Since a package may have multiple licenses, the JOIN could produce duplicate rows. Add `.distinct()` to the query or use `GROUP BY` to ensure each package appears only once in the results, consistent with how other JOINed filters handle this in the codebase.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests verifying the license filter functionality.

**Changes:**

- **Follow the test conventions from sibling test files** (`tests/api/sbom.rs`, `tests/api/advisory.rs`): Use the same test setup pattern (PostgreSQL test database), assertion style (`assert_eq!(resp.status(), StatusCode::OK)`), response deserialization pattern, and naming convention (`test_<endpoint>_<scenario>`).

- **Test cases to implement:**

  1. **`test_list_packages_filter_single_license`**: Verify that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on specific package fields (not just count) to catch regressions. Add doc comment explaining what the test verifies. Use given-when-then section comments.

  2. **`test_list_packages_filter_multiple_licenses`**: Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that both MIT and Apache-2.0 licensed packages appear in results, and that packages with other licenses are excluded. Value-based assertions on the returned items.

  3. **`test_list_packages_no_license_filter`**: Verify that `GET /api/v2/package` without a license parameter returns all packages unchanged. Compare against the full expected set to ensure no regression.

  4. **`test_list_packages_invalid_license`**: Verify that an invalid license value returns 400 Bad Request. Assert on `StatusCode::BAD_REQUEST`.

- **Test structure**: Each test function gets a `///` doc comment and given-when-then internal comments. Test data setup seeds packages with known licenses (MIT, Apache-2.0, GPL-3.0) so assertions can verify exact matches.

- **Module registration**: Add `mod package_license_filter;` to the test module root (`tests/api/mod.rs` or equivalent) so the test file is compiled and discovered.

## Integration Points

- **Route registration**: The route in `modules/fundamental/src/package/endpoints/mod.rs` does NOT need modification -- the existing route for `GET /api/v2/package` already invokes the handler in `list.rs`. The new `Query` struct field is automatically extracted by Axum's query parameter deserializer (optional fields default to `None` when absent).

- **Module imports**: Add `use common::db::query::apply_filter;` and `use entity::package_license;` to the service module.

- **No migration needed**: The `package_license` table and entity already exist -- no database schema changes required.

## Code Reuse Summary

All three Reuse Candidates from the task description are used:

| Reuse Candidate | How It Is Used | Avoids Duplicating |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in PackageService to parse comma-separated license values and generate SQL IN clause | Custom comma-splitting logic and SQL generation |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as structural template for the Query struct pattern with optional filter field | Inventing a new parameter extraction approach |
| `entity/src/package_license.rs` | Used for the SeaORM JOIN between package and license tables | Raw SQL JOIN statements |

## Scope Boundaries

- Only the files listed in "Files to Modify" and "Files to Create" are touched
- The response shape (`PaginatedResults<PackageSummary>`) is not changed
- No new utility functions are created that would duplicate `apply_filter` functionality
- No unrelated refactoring is performed
