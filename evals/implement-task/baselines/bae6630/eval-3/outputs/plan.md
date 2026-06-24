# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses existing query infrastructure and follows the established advisory filter pattern.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with pagination and sorting but no license filter.

**Changes:**
- Add an optional `license` field (type `Option<String>`) to the `Query` struct used for extracting query parameters from the request. This follows the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, check if `query.license` is `Some`. If so, call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value and generate the appropriate SQL `IN` clause against the `package_license` join table.
- Add the `package_license` entity join (`entity/src/package_license.rs`) to the query builder so the filter can reference the license column on the join table.
- Return 400 Bad Request for invalid license values by leveraging the existing `AppError` pattern (Result<T, AppError> with `.context()` wrapping).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries packages with pagination/sorting but no license filter.

**Changes:**
- Add an optional `license_filter: Option<Vec<String>>` parameter (or an equivalent filter struct field) to the `list` method signature.
- When the license filter is provided, join the `package_license` entity table and add a `WHERE package_license.license IN (...)` condition to the SeaORM query.
- Reuse `apply_filter` from `common/src/db/query.rs` to handle the comma-separated parsing and SQL IN clause generation, exactly as the advisory service does for severity filtering.
- Ensure the join does not alter the response shape — `PaginatedResults<PackageSummary>` remains unchanged.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license query parameter.

**Contents:**
- `test_filter_single_license` — Seed packages with different licenses (MIT, Apache-2.0, GPL-3.0). Query `GET /api/v2/package?license=MIT`. Assert only MIT-licensed packages are returned. Validate specific package identifiers in the response, not just count.
- `test_filter_multi_license` — Query `GET /api/v2/package?license=MIT,Apache-2.0`. Assert packages with either MIT or Apache-2.0 are returned. Verify both licenses are represented in results.
- `test_no_license_filter` — Query `GET /api/v2/package` without the `license` parameter. Assert all seeded packages are returned (no regression).
- `test_invalid_license_value` — Query `GET /api/v2/package?license=` or with a malformed value. Assert 400 Bad Request response.

All tests follow the existing integration test conventions in `tests/api/`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Deserialize response body and validate `total_count`, `items.len()`, and key fields
- Each test function has a `///` doc comment explaining what it verifies
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments

## How Existing Code Is Reused

### `common/src/db/query.rs::apply_filter`

This is the primary reuse target. The `apply_filter` function already handles:
- Parsing a comma-separated string into individual values
- Generating a SQL `IN (...)` clause for multi-value filtering
- Handling single-value as a degenerate case of multi-value

The license filter will call `apply_filter` directly with the raw `license` query parameter string. No new utility functions are needed for parsing or SQL generation — `apply_filter` provides the complete pipeline.

### `modules/fundamental/src/advisory/endpoints/list.rs` (structural guide)

The advisory list endpoint's `severity` filter is the structural template:
1. The `Query` struct has an `Option<String>` field for the filter parameter
2. The handler extracts the field and passes it to the service layer
3. The service layer calls `apply_filter` to build the SQL condition
4. The join and filter are added to the SeaORM query builder

The package license filter replicates this exact pattern — same `Query` struct approach, same `apply_filter` call, same service-layer integration.

### `entity/src/package_license.rs` (JOIN entity)

The `package_license` entity defines the SeaORM model for the package-license join table. Instead of writing raw SQL for the join, the implementation uses this entity in the SeaORM query builder:
- `PackageLicense::find()` or a `.join()` call referencing the entity's `Relation`
- The entity's column definitions provide type-safe access to the license identifier column
- This maintains consistency with how other join tables (e.g., `sbom_package`, `sbom_advisory`) are used throughout the codebase

## Scope Boundaries

All changes are confined to the three files listed above (two modifications, one creation). No changes to:
- Route registration (`endpoints/mod.rs`) — the existing route for `GET /api/v2/package` already dispatches to `list.rs`
- Response types (`PackageSummary`, `PaginatedResults`) — the response shape is unchanged
- Database migrations — the `package_license` table already exists
- Other modules — no cross-module changes needed
