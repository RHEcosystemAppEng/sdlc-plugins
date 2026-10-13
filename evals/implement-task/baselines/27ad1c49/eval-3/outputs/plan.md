# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged; only the input accepts a new optional parameter.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

- Add an optional `license` field (type `Option<String>`) to the query parameter struct used by the `GET /api/v2/package` handler. Follow the same Query struct pattern used in `modules/fundamental/src/advisory/endpoints/list.rs`, where the advisory list endpoint defines an optional `severity` field on its query struct.
- In the handler function, extract the `license` value from the query parameters and pass it through to `PackageService::list()`.
- Add input validation: if the `license` value is present but contains invalid characters or is otherwise malformed, return a `400 Bad Request` response using the existing `AppError` enum from `common/src/error.rs`.
- Do NOT implement custom comma-separated parsing logic here. Instead, pass the raw `license` string to the service layer, which will delegate to `apply_filter` for parsing.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Changes:**

- Modify the `PackageService::list()` method signature to accept an additional optional `license` filter parameter (e.g., `license: Option<&str>`).
- When the `license` parameter is `Some`, build a filter query that:
  1. Uses `common/src/db/query.rs::apply_filter` to parse the comma-separated license string into individual values and generate the appropriate SQL `IN` clause. This reuses the existing multi-value parsing logic rather than duplicating it.
  2. JOINs through the `entity/src/package_license.rs` entity (the `package_license` SeaORM entity) to filter packages by their associated license SPDX identifiers. The join connects the `package` table to the `package_license` table on the package ID foreign key.
- When the `license` parameter is `None`, the query behaves identically to the current implementation (no regression).
- Use the existing `Result<T, AppError>` return type with `.context()` wrapping for error handling, consistent with the conventions established in sibling service methods.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Test cases:**

- `test_filter_single_license` -- Verify that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Assert on specific package identifiers in the response, not just the count.
- `test_filter_multiple_licenses` -- Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that the response contains packages with both MIT and Apache-2.0 licenses and excludes packages with other licenses.
- `test_no_license_filter` -- Verify that `GET /api/v2/package` without a license parameter returns all packages unchanged (no regression).
- `test_invalid_license_value` -- Verify that an invalid license value returns `400 Bad Request`.

**Conventions:**
- Follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern used in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`).
- Each test function gets a `///` documentation comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Tests hit a real PostgreSQL test database, consistent with the project's integration test approach.

**Module registration:**
- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) so the new test file is compiled. This is a minor out-of-scope addition that would be flagged during Step 9 scope containment for user approval.

## Reuse Strategy

This implementation reuses three existing code assets rather than writing new utilities:

1. **`common/src/db/query.rs::apply_filter`** -- Reuse directly for comma-separated multi-value query parameter parsing and SQL IN clause generation. The `license` filter string (e.g., `"MIT,Apache-2.0"`) is passed to `apply_filter`, which splits on commas, trims whitespace, and generates the appropriate SQL `IN (...)` clause. No new parsing utility is created; this function already handles the exact use case.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Follow as a structural template. The advisory list endpoint's severity filter implementation is structurally identical to the license filter: an optional field on a Query struct, extracted in the handler, passed to the service layer. The same pattern is replicated in the package endpoint rather than inventing a different approach.

3. **`entity/src/package_license.rs`** -- Use the existing SeaORM entity for the package-license join table. The JOIN query in `PackageService::list()` references this entity's `Column` and `Relation` definitions to connect packages to their licenses. No raw SQL is written; the existing entity provides the type-safe query building blocks.

## Data-Flow Trace

1. **Input**: HTTP GET request with optional `?license=MIT,Apache-2.0` query parameter arrives at the package list endpoint handler in `list.rs`.
2. **Extraction**: Axum deserializes the query string into the Query struct; the `license` field is `Option<String>`.
3. **Validation**: The handler validates the license value (if present). Invalid values produce a `400 Bad Request` via `AppError`.
4. **Service call**: The handler passes the license filter to `PackageService::list()`.
5. **Query building**: The service method calls `apply_filter` to parse comma-separated values into a filter clause, then builds a SeaORM query joining `package` to `package_license` and applying the IN filter on the license SPDX identifier column.
6. **Execution**: The query runs against PostgreSQL, returning matching `Package` rows.
7. **Response**: Results are wrapped in `PaginatedResults<PackageSummary>` (unchanged response shape) and serialized as JSON.

All stages are connected. The response shape is unchanged, so downstream consumers are unaffected.

## Scope Boundaries

All changes are strictly confined to the files listed in Files to Modify and Files to Create. No modifications are planned for:
- `common/src/db/query.rs` (reused as-is, not modified)
- `entity/src/package_license.rs` (reused as-is, not modified)
- `modules/fundamental/src/advisory/endpoints/list.rs` (referenced as a pattern, not modified)
- `modules/fundamental/src/package/endpoints/mod.rs` (route registration -- only flagged if the existing registration does not already cover the list handler)
- Any other files outside the specified scope

If test module registration (`mod package_license_filter;`) requires touching an additional file, this would be flagged during the Step 9 scope containment check for explicit user approval before committing.
