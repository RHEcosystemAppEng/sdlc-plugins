# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that supports both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing filtering infrastructure rather than introducing new parsing or query-building logic.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Defines the handler for `GET /api/v2/package` with a Query struct for extracting query parameters. Does not currently include a license filter.

**Changes:**

- **Add `license` field to the Query struct:** Add an `Option<String>` field named `license` to the existing Query struct used for parameter extraction. This follows the same pattern used in `modules/fundamental/src/advisory/endpoints/list.rs`, where the advisory list endpoint's Query struct has an optional `severity` field for filtering. The field is `Option<String>` because `apply_filter` from `common/src/db/query.rs` accepts a string and handles comma-separated parsing internally.

- **Pass the license filter to the service layer:** In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter. No parsing of the comma-separated values is done at the endpoint layer -- that responsibility belongs to `apply_filter` in the service/query layer.

- **Add validation:** Return `400 Bad Request` (via `AppError`) when the license parameter is present but contains empty or whitespace-only values.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that builds a database query to fetch packages. Does not currently filter by license.

**Changes:**

- **Add `license` parameter to the `list` method signature:** Accept `license: Option<String>` as an additional parameter.

- **Build the license filter using `apply_filter` from `common/src/db/query.rs`:** When `license` is `Some`, call `apply_filter` with the license string. `apply_filter` handles splitting comma-separated values and generating the appropriate SQL `IN` clause. This is the same function used throughout the codebase for multi-value filtering -- no new parsing logic is written.

- **JOIN through `entity::package_license` for the filter query:** Use the `package_license` entity from `entity/src/package_license.rs` to join the `package` table to the `package_license` table. This entity already maps the relationship between packages and their SPDX license identifiers. The JOIN is expressed using SeaORM's relation API (e.g., `Package::find().join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())`) rather than raw SQL. Apply the `apply_filter`-generated condition on the license column of the `package_license` entity.

- **Preserve existing behavior when filter is absent:** When `license` is `None`, skip the JOIN and filter entirely, returning all packages as before (no regression).

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Test cases:**

- **`test_filter_single_license`** -- Verify that `GET /api/v2/package?license=MIT` returns only packages with a MIT license. Assert on specific package identifiers in the response, not just the count.

- **`test_filter_multiple_licenses`** -- Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that the response contains packages with both MIT and Apache-2.0 licenses and excludes packages with other licenses.

- **`test_no_license_filter_returns_all`** -- Verify that `GET /api/v2/package` without a license parameter returns all packages unchanged (regression check). Compare against a known baseline count and specific expected packages.

- **`test_invalid_license_returns_400`** -- Verify that an invalid/empty license value returns `400 Bad Request` with an appropriate error message.

**Conventions followed:**
- Tests hit a real PostgreSQL test database (per project convention).
- Assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests use given-when-then section comments.
- Response shape is `PaginatedResults<PackageSummary>` -- assert on fields within this structure.

## Data Flow Trace

1. **Input:** HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at the Axum handler in `list.rs`.
2. **Extraction:** Axum deserializes query parameters into the Query struct; `license` field captures `Some("MIT,Apache-2.0")`.
3. **Validation:** Handler validates the license string is non-empty; returns 400 if invalid.
4. **Service call:** Handler passes `license: Some("MIT,Apache-2.0")` to `PackageService::list()`.
5. **Filter construction:** Service calls `apply_filter("MIT,Apache-2.0")` from `common/src/db/query.rs`, which splits on commas and produces an `IN ('MIT', 'Apache-2.0')` condition.
6. **Query building:** Service builds a SeaORM select on `Package`, joins to `package_license` entity, applies the filter condition on the license column.
7. **Execution:** Query executes against PostgreSQL, returning matching rows.
8. **Response:** Results are wrapped in `PaginatedResults<PackageSummary>` and serialized as JSON. The response shape is unchanged -- only the input accepts the new parameter.

## Scope Boundaries

All changes are strictly within the files listed in the task's Files to Modify and Files to Create sections. No other files are modified. Specifically:
- No changes to `common/src/db/query.rs` -- `apply_filter` is used as-is.
- No changes to `entity/src/package_license.rs` -- the entity is used as-is.
- No changes to route registration (`endpoints/mod.rs`) -- the existing route handler is modified in place.
- No changes to response types -- `PaginatedResults<PackageSummary>` is unchanged.
