# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint that supports both single-value and comma-separated multi-value filtering by SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) must remain unchanged.

## Branch

Create branch `TC-9203` from `main` (the Target Branch).

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** This file implements the `GET /api/v2/package` endpoint handler. It accepts query parameters for pagination and sorting but has no license filter.

**Changes:**
- Add an optional `license` field (type `Option<String>`) to the query parameter extraction struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, extract the `license` query parameter value and pass it through to the `PackageService::list` method.
- If the `license` parameter is present, call `apply_filter` from `common/src/db/query.rs` to parse comma-separated values and build the SQL filter clause.
- Add validation for the license value: if the parameter is present but contains invalid characters or is empty after trimming, return a `400 Bad Request` using the `AppError` enum from `common/src/error.rs`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** This file contains `PackageService` with a `list` method that queries packages from the database without license filtering.

**Changes:**
- Add an optional `license` parameter (type `Option<String>`) to the `list` method signature.
- When the `license` parameter is `Some`, add a JOIN to the `package_license` entity (`entity/src/package_license.rs`) and apply a filter condition using `apply_filter` from `common/src/db/query.rs`.
- The `apply_filter` function handles both single values and comma-separated multi-value parsing, generating an `IN` clause for multiple values — reuse it directly rather than implementing custom parsing.
- Ensure the JOIN does not produce duplicate results (use `DISTINCT` or `group_by` if the join table has multiple rows per package for different licenses).
- Wrap any database errors with `.context()` following the project's error handling convention.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Contents:**
- Import test utilities and HTTP client setup following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Seed the test database with packages that have known licenses (e.g., MIT, Apache-2.0, GPL-3.0).
- Implement the following test functions (each with a `///` doc comment and given-when-then structure):

  1. `test_list_packages_filter_single_license` — Verify that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Assert on specific package identifiers, not just count.
  2. `test_list_packages_filter_multiple_licenses` — Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that the result set contains the expected packages and excludes non-matching ones.
  3. `test_list_packages_no_license_filter` — Verify that `GET /api/v2/package` (without the `license` parameter) returns all packages, confirming no regression.
  4. `test_list_packages_invalid_license` — Verify that an invalid license value returns `400 Bad Request`. Assert on the response status code.

- Follow assertion patterns from sibling test files: use `assert_eq!(resp.status(), StatusCode::OK)` for success cases, deserialize response body to `PaginatedResults<PackageSummary>`, and verify specific field values (not just collection lengths).
- Use the `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` pattern for error cases.

## Additional Integration Points

### Module registration

- If `tests/api/package_license_filter.rs` is a new test file, it may need to be registered in `tests/Cargo.toml` as a test target or referenced via `mod` declaration depending on the project's test organization. Check how `tests/api/sbom.rs` and `tests/api/advisory.rs` are registered and follow the same pattern.

### No changes needed to

- `entity/src/package_license.rs` — The existing package-license entity is reused as-is for the JOIN query. No schema or entity changes needed.
- `common/src/db/query.rs` — The existing `apply_filter` function already handles comma-separated multi-value parsing and SQL IN clause generation. No changes needed.
- `modules/fundamental/src/package/model/summary.rs` — The `PackageSummary` response struct already includes a `license` field. The response shape is unchanged.
- `modules/fundamental/src/package/endpoints/mod.rs` — Route registration does not change; the list endpoint handler already exists.
- `server/src/main.rs` — No new modules or routes to mount.

## Implementation Sequence

1. Modify `modules/fundamental/src/package/service/mod.rs` — add the license filter to the service layer first (data layer before API layer).
2. Modify `modules/fundamental/src/package/endpoints/list.rs` — add the query parameter extraction and pass it to the service.
3. Create `tests/api/package_license_filter.rs` — write integration tests.
4. Run `cargo test` to verify all tests pass.
5. Verify acceptance criteria against the running test suite.
6. Run CI checks from `CONVENTIONS.md` if present.
7. Commit with message: `feat(api): add license filter to package list endpoint\n\nImplements TC-9203`

## Conventions to Follow

Based on the repository structure and key conventions documented in the repo:

- **Framework patterns:** Axum for HTTP handling, SeaORM for database queries.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Query helpers:** Use shared filtering, pagination, and sorting from `common/src/db/query.rs`.
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure.
- **Testing:** Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` request received by Axum router
  -> Query parameter extracted in `endpoints/list.rs` (input)
  -> Passed to `PackageService::list()` in `service/mod.rs` (processing)
  -> `apply_filter` parses comma-separated values, builds SQL IN clause (processing)
  -> JOIN with `package_license` entity, query executed via SeaORM (processing)
  -> Results wrapped in `PaginatedResults<PackageSummary>` and returned as JSON response (output)
  -> **COMPLETE**
