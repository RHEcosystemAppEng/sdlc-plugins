# Implementation Plan: TC-9203 -- Add Package License Filter to List Endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation follows existing patterns established by the advisory severity filter.

## Branch Strategy

- Base branch: `main`
- Task branch: `TC-9203`
- PR target: `main`

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with pagination and sorting but no license filtering.

**Changes:**
- Add an optional `license` field to the `PackageListQuery` struct (or equivalent query parameter struct). This follows the exact same pattern as the `severity` field in the advisory list endpoint's query struct at `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` query parameter value.
- Pass the license filter value down to the `PackageService::list` method call.
- Use `common/src/db/query.rs::apply_filter` to parse the comma-separated license string and generate the appropriate SQL IN clause. This function already handles both single and multi-value comma-separated parameters, so no new parsing logic is needed.
- Add validation: if the `license` parameter is present but contains invalid/empty values, return a 400 Bad Request using the `AppError` enum from `common/src/error.rs`.

**Pattern reference:** The `severity` filter in `modules/fundamental/src/advisory/endpoints/list.rs` demonstrates the exact same pattern -- an optional query parameter field parsed with `apply_filter` and passed to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries packages with pagination/sorting but no license filtering.

**Changes:**
- Add an optional `license` parameter (e.g., `Option<Vec<String>>` or `Option<String>`) to the `list` method signature.
- When the license filter is provided, add a JOIN to the `package_license` table (using the `entity/src/package_license.rs` SeaORM entity) and a WHERE clause filtering on the license SPDX identifier column.
- Use `apply_filter` from `common/src/db/query.rs` to build the filter condition if it is not already parsed at the endpoint layer. The exact placement of the `apply_filter` call depends on whether the advisory pattern parses at the endpoint or service layer -- follow whichever pattern the advisory severity filter uses.
- When the license parameter is `None`, the query remains unchanged (no JOIN, no filter), preserving backward compatibility.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test functions (following `test_<endpoint>_<scenario>` naming convention from sibling tests):**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200 OK. Response body is `PaginatedResults<PackageSummary>`. Only packages with MIT license are returned. Assert on specific package names/identifiers, not just count.

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license values return packages matching any listed license.`
   - Given: Same seeded database.
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200 OK. Packages with MIT OR Apache-2.0 licenses are returned. GPL-3.0-only packages are excluded. Assert on specific values.

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Same seeded database.
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200 OK. All packages are returned regardless of license. Total count matches expected.

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Same seeded database.
   - When: `GET /api/v2/package?license=` (empty value or invalid format, depending on validation rules)
   - Then: Response status is 400 Bad Request.

**Conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests.
- Validate `total_count`, `items.len()`, and key fields of returned items.
- Include error case with status code assertion.
- Add given-when-then section comments inside each test body.
- Each test function has a `///` doc comment.

**Integration with test suite:**
- Register the new test file in `tests/api/` module (e.g., add `mod package_license_filter;` to the test module's `mod.rs` or `main.rs` depending on the project's test organization).

## Module Registration

No new route registration is needed -- the `GET /api/v2/package` endpoint already exists in `modules/fundamental/src/package/endpoints/mod.rs`. The change only adds a new optional query parameter to the existing handler.

## Data Flow Trace

1. **Input:** HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at the Axum handler in `list.rs`.
2. **Extraction:** The `license` query parameter is deserialized into the query struct's optional `license` field.
3. **Parsing:** `apply_filter` from `common/src/db/query.rs` splits the comma-separated string into individual values (`["MIT", "Apache-2.0"]`).
4. **Service call:** The handler passes the parsed license values to `PackageService::list`.
5. **Query building:** The service JOINs the `package_license` entity table and adds a WHERE ... IN clause for the license identifiers.
6. **Database execution:** SeaORM executes the query against PostgreSQL.
7. **Response:** Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON. The response shape is unchanged -- only the result set is filtered.

## Acceptance Criteria Verification Plan

| Criterion | Verification |
|---|---|
| `?license=MIT` returns only MIT packages | Integration test `test_list_packages_filter_single_license` |
| `?license=MIT,Apache-2.0` returns matching packages | Integration test `test_list_packages_filter_multiple_licenses` |
| No license parameter returns all packages | Integration test `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` -- compilation fails if shape changes |
| Invalid license returns 400 | Integration test `test_list_packages_invalid_license` |
