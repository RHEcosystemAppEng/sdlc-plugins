# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) must remain unchanged.

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What exists:** The current `GET /api/v2/package` endpoint handler with a Query struct for extracting query parameters and a handler function that calls `PackageService::list`.

**Changes:**

- **Add `license` field to the Query struct:** Add an `Option<String>` field named `license` to the existing query parameter extraction struct, following the same pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate #2). The field is optional so that omitting the parameter returns all packages (no regression).

- **Pass the license filter to the service layer:** In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter (or within an updated query/filter struct). This mirrors how the advisory list endpoint passes its `severity` filter to `AdvisoryService::list()`.

- **Validate the license parameter:** Add validation logic that returns a `400 Bad Request` (via `AppError`) when the license parameter contains invalid values. Use the same validation approach seen in the advisory severity filter pattern.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What exists:** `PackageService` with a `list` method that queries the database and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Accept a license filter parameter:** Update the `list` method signature to accept an optional license filter (e.g., `license: Option<String>`).

- **Apply the filter using `apply_filter` from `common/src/db/query.rs`** (Reuse Candidate #1): Call the existing `apply_filter` function to handle parsing of comma-separated values and generation of the SQL `IN` clause. This function already handles both single-value (`license=MIT`) and multi-value (`license=MIT,Apache-2.0`) cases. Do NOT write custom parsing or splitting logic -- reuse `apply_filter` directly.

- **JOIN through `entity/src/package_license.rs`** (Reuse Candidate #3): Use the existing `package_license` SeaORM entity to join the `package` table to the `package_license` table when the license filter is present. This follows the SeaORM join pattern -- use `JoinType::InnerJoin` with the `package_license` relation to filter packages by their associated license SPDX identifiers. Do NOT write raw SQL for this join.

- **Conditional join:** Only add the JOIN and WHERE clause when the `license` parameter is provided. When `license` is `None`, the query remains unchanged (no regression).

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter feature.

**Structure:** Follow the test patterns established in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for validation errors
- Validate response body by deserializing into `PaginatedResults<PackageSummary>` and asserting on specific item values (not just counts)
- Follow `test_<endpoint>_<scenario>` naming convention
- Add doc comments (`///`) on every test function explaining what it verifies
- Use given-when-then section comments (`// Given`, `// When`, `// Then`) for non-trivial tests

**Test cases:**

1. `test_list_packages_filter_single_license` -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Seeds test data with packages having MIT, Apache-2.0, and GPL-3.0 licenses. Asserts that all returned items have `license == "MIT"`.

2. `test_list_packages_filter_multiple_licenses` -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Seeds test data with packages having MIT, Apache-2.0, and GPL-3.0 licenses. Asserts returned items have licenses in `["MIT", "Apache-2.0"]` and that GPL-3.0 packages are excluded.

3. `test_list_packages_no_license_filter` -- Verifies that `GET /api/v2/package` without a license parameter returns all packages unchanged. Seeds test data and asserts total count matches expected count of all seeded packages.

4. `test_list_packages_invalid_license` -- Verifies that `GET /api/v2/package?license=!!!invalid` returns 400 Bad Request. Asserts `resp.status() == StatusCode::BAD_REQUEST`.

**Integration with test module:** Register the new test file in the test module's `mod.rs` or `Cargo.toml` test configuration as needed, following the existing pattern for `sbom.rs` and `advisory.rs`.

## No New Utility Functions

The implementation does NOT create any new utility functions for parsing or filtering. All parsing of comma-separated values and SQL clause generation is handled by the existing `apply_filter` function in `common/src/db/query.rs`. The JOIN query uses the existing `package_license` entity. The endpoint structure follows the existing advisory severity filter pattern. This avoids any code duplication.

## Data-Flow Trace

1. **Input:** HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Extraction:** Axum deserializes query parameters into the Query struct, populating `license: Some("MIT,Apache-2.0")`
3. **Validation:** The handler validates the license parameter format; invalid values produce 400 Bad Request
4. **Service call:** Handler passes `license` to `PackageService::list()`
5. **Query building:** Service calls `apply_filter` (from `common/src/db/query.rs`) which parses `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]` and generates an SQL `IN` clause
6. **JOIN:** Service uses the `package_license` entity to join packages to their licenses, applying the filter condition
7. **Output:** Query results are wrapped in `PaginatedResults<PackageSummary>` and returned -- response shape unchanged

## Commit Strategy

Single commit following Conventional Commits:

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203
```
