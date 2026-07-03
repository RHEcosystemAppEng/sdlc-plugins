# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses existing patterns from the advisory severity filter, the shared `apply_filter` helper, and the `package_license` entity.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- Add an optional `license` field (type `Option<String>`) to the query parameter struct used by the `GET /api/v2/package` handler, following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` query parameter from the request and pass it to the `PackageService::list` method.
- No changes to the response shape -- `PaginatedResults<PackageSummary>` remains unchanged.

**How (structural guide from advisory severity filter):**

The advisory list endpoint (`modules/fundamental/src/advisory/endpoints/list.rs`) defines a Query struct with an optional `severity` field and passes it through to the service layer. Replicate this pattern exactly:

```rust
#[derive(Debug, Deserialize)]
pub struct PackageListQuery {
    // ... existing fields (pagination, sorting) ...
    pub license: Option<String>,  // NEW: optional license filter
}
```

In the handler, pass `query.license` to `PackageService::list()`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- Modify the `PackageService::list` method signature to accept an optional `license` parameter (or accept it as part of an expanded filter/query struct).
- When `license` is `Some(value)`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string into individual values and generate the appropriate SQL `IN` clause.
- Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers.
- When `license` is `None`, skip the filter entirely so the existing behavior (return all packages) is preserved.

**How (reusing apply_filter and package_license entity):**

1. Import `apply_filter` from `common::db::query`.
2. Import the `package_license` entity from `entity::package_license`.
3. When `license` is provided:
   - Use `apply_filter` to parse the comma-separated license string (e.g., `"MIT,Apache-2.0"`) into individual values. `apply_filter` handles both single and multi-value inputs and generates the appropriate SQL `IN` clause.
   - Build a SeaORM query that JOINs `package` to `package_license` on the foreign key relationship defined in the `package_license` entity.
   - Apply the filter condition to match `package_license.license` against the parsed values.
   - Use `.distinct()` on the query to avoid duplicate packages when a package matches multiple license values.
4. When `license` is `None`, do not add the JOIN or filter -- the query remains unchanged.

**Validation:**

- If the `license` parameter is present but empty (e.g., `?license=`), return `400 Bad Request` using `AppError` from `common::error`.
- If any license value in the comma-separated list is not a valid string, return `400 Bad Request`.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**What this file contains:**

Integration tests for the new license filter on `GET /api/v2/package`. Tests hit a real PostgreSQL test database following the same patterns as `tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Test cases (from Test Requirements):**

1. **`test_list_packages_filter_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Seeds the database with packages having different licenses, asserts that the response contains only MIT-licensed packages by checking specific package identifiers (not just count).

2. **`test_list_packages_filter_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Seeds packages with MIT, Apache-2.0, and GPL-3.0 licenses, asserts the response contains exactly the MIT and Apache-2.0 packages.

3. **`test_list_packages_no_license_filter`** -- Verifies that `GET /api/v2/package` without a `license` parameter returns all packages unchanged (no regression). Seeds multiple packages and asserts the full set is returned.

4. **`test_list_packages_invalid_license`** -- Verifies that an invalid/empty license value returns `400 Bad Request`. Asserts `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions followed:**

- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks.
- Deserialize response body and validate `total_count`, `items.len()`, and specific item fields.
- Test naming follows `test_<endpoint>_<scenario>` pattern.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Register the new test file in `tests/Cargo.toml` if needed.

## Module Registration

No new routes or modules are created -- the `license` parameter is added to the existing `GET /api/v2/package` handler in the existing endpoint file. No changes to `modules/fundamental/src/package/endpoints/mod.rs` or `server/src/main.rs` are needed.

## Data-Flow Trace

1. **Input**: HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at Axum handler in `list.rs`.
2. **Extraction**: Axum deserializes `license` from query string into `PackageListQuery.license` (`Option<String>`).
3. **Service call**: Handler passes `query.license` to `PackageService::list()` in `service/mod.rs`.
4. **Filter construction**: Service calls `apply_filter` (from `common/src/db/query.rs`) to parse `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]` and generate the SQL `IN` clause.
5. **JOIN**: Service builds a SeaORM query joining `package` to `package_license` (from `entity/src/package_license.rs`) and applies the `IN` filter on the license column.
6. **Execution**: Query executes against PostgreSQL, returning matching packages.
7. **Response**: Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON -- response shape unchanged.

## Scope Boundaries

- Only the three files listed above are touched (two modified, one created).
- No changes to the response shape (`PaginatedResults<PackageSummary>`).
- No changes to other endpoints or modules.
- No new utility functions -- `apply_filter` from `common/src/db/query.rs` is reused directly.
- No database migrations needed -- `package_license` table already exists.
