# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Project Configuration Validation

- Repository Registry: `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key `TC`, Cloud ID present, Feature issue type ID `10142`
- Code Intelligence: Serena instance `serena_backend` using `rust-analyzer`

All required sections are present. Proceed with implementation.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** This file implements the `GET /api/v2/package` endpoint handler. It defines a query parameter struct (likely named `PackageQuery` or similar) and an Axum handler function that extracts query parameters, calls `PackageService::list()`, and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` field to the query parameter struct:** Add an `Option<String>` field named `license` to the existing query struct (e.g., `PackageQuery`). This follows the same pattern used by `advisory/endpoints/list.rs` which has an `Option<String>` field for `severity` on its query struct.

2. **Parse the license parameter using `apply_filter`:** In the handler function, after extracting query parameters, call `common::db::query::apply_filter` on the `license` field to parse comma-separated values into a filter condition. This reuses the existing utility rather than writing custom parsing logic.

3. **Pass the license filter to the service layer:** Pass the parsed license filter to `PackageService::list()` as an additional parameter (or as part of an extended filter struct).

4. **Add validation:** Return `400 Bad Request` (via `AppError`) for invalid license values. Validate that license strings are non-empty after splitting on commas, and that they contain only valid SPDX identifier characters.

**Pattern reference:** Follow the exact structure from `advisory/endpoints/list.rs` -- the severity filter implementation uses the same `Option<String>` field on the Query struct, calls `apply_filter` for parsing, and passes the result to its service method.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** This file implements `PackageService` with methods including `fetch` and `list`. The `list` method queries the database for packages and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add a `license` filter parameter to the `list` method signature:** Add an optional filter parameter (e.g., `license_filter: Option<Vec<String>>` or a filter struct field) to the `list` method.

2. **Implement the JOIN query using `entity::package_license`:** When a license filter is present, add a JOIN from the `package` table to the `package_license` table using the SeaORM entity defined in `entity/src/package_license.rs`. This uses the existing entity rather than writing raw SQL.

3. **Apply the WHERE clause:** Use the parsed filter values to build a `Column::IsIn` condition on the license column of the `package_license` entity. This filters packages to those whose associated license SPDX identifiers match any of the provided values.

4. **Maintain existing behavior when no filter:** When the `license` parameter is `None`, skip the JOIN and WHERE clause entirely, preserving the existing behavior of returning all packages.

5. **Use `.context()` error wrapping:** Follow the codebase convention of wrapping database errors with `.context()` for `AppError` conversion.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Structure:** Follow the test conventions observed in sibling files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):
- Use a real PostgreSQL test database
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases

**Test cases:**

1. **`test_filter_packages_by_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Packages with MIT, Apache-2.0, and GPL-3.0 licenses exist in the database
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200; response body contains only packages with MIT license; assert on specific package names/identifiers, not just count

2. **`test_filter_packages_by_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license values return packages matching any listed license.`
   - Given: Packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200; response body contains packages with MIT and Apache-2.0 licenses but not GPL-3.0; assert on specific values

3. **`test_no_license_filter_returns_all_packages`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Packages with various licenses exist
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200; response body contains all packages; verify count and content match the full set

4. **`test_invalid_license_value_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Standard test data
   - When: `GET /api/v2/package?license=` (empty value)
   - Then: Response status is 400 Bad Request

**Additional module registration:** The new test file must be registered in `tests/api/mod.rs` (if one exists) or referenced in `tests/Cargo.toml` so it is discovered by the test runner. Check sibling test files for the registration pattern.

## Files NOT Modified (scope containment)

The following files are explicitly out of scope and will not be modified:

- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration should not need changes since the endpoint path (`GET /api/v2/package`) is unchanged; only its handler gains a new optional query parameter
- `modules/fundamental/src/package/model/summary.rs` -- the `PackageSummary` struct is unchanged; the license field already exists on it
- `entity/src/package_license.rs` -- used as-is for the JOIN; no modifications needed
- `common/src/db/query.rs` -- `apply_filter` is used as-is; no modifications needed
- `server/src/main.rs` -- no route changes needed

## Code Reuse Strategy

All three Reuse Candidates from the task description are used directly. No new utility functions are created that would duplicate existing ones.

1. **`common/src/db/query.rs::apply_filter`** -- called directly to parse the `license` query parameter string (including comma-separated values) into a filter condition. This avoids writing custom string-splitting or SQL IN clause generation.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- the severity filter pattern is followed structurally: same Query struct pattern with an `Option<String>` field, same `apply_filter` call, same pass-through to the service layer.

3. **`entity/src/package_license.rs`** -- the existing SeaORM entity is used to build the JOIN query in `PackageService::list()`, avoiding raw SQL and maintaining consistency with the ORM-based data access pattern used throughout the codebase.

## Data-Flow Trace

1. **Input:** HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Extraction:** Axum extracts `PackageQuery` from query string; `license` field is `Some("MIT,Apache-2.0")`
3. **Parsing:** `apply_filter` from `common/src/db/query.rs` parses the comma-separated string into `vec!["MIT", "Apache-2.0"]`
4. **Validation:** License values are validated (non-empty, valid characters); invalid values produce `AppError` -> 400 response
5. **Service call:** Handler calls `PackageService::list()` with the parsed license filter
6. **Query building:** Service builds a SeaORM query JOINing `package` to `package_license` via the entity in `entity/src/package_license.rs`, applying `WHERE license_spdx IN ('MIT', 'Apache-2.0')`
7. **Output:** Query results are mapped to `PaginatedResults<PackageSummary>` and returned as the JSON response

All stages are connected. The response shape is unchanged -- only the query filtering is new.

## Acceptance Criteria Verification Plan

| Criterion | Verification |
|-----------|-------------|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Test `test_filter_packages_by_single_license` + manual data-flow trace |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | Test `test_filter_packages_by_multiple_licenses` |
| No license parameter returns all packages | Test `test_no_license_filter_returns_all_packages` |
| Response shape unchanged | No modifications to `PackageSummary` or `PaginatedResults`; verified by all tests using the same response deserialization |
| Invalid license values return 400 | Test `test_invalid_license_value_returns_400` + validation logic in handler |
