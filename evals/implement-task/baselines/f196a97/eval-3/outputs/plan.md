# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Contains the handler for `GET /api/v2/package` with a query parameter struct for pagination/sorting but no license filter.

**Changes:**

- **Add `license` field to the query parameter struct:** Add an `Option<String>` field named `license` to the existing query/params struct used by the list handler. This follows the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate).

- **Pass the license parameter to the service layer:** In the handler function, extract the `license` value from the query struct and pass it to `PackageService::list()`. If `None`, no filter is applied (preserving backward compatibility).

- **Validate the license parameter:** If the `license` value is present but contains invalid characters or empty segments (e.g., trailing commas, empty strings between commas), return a `400 Bad Request` using the existing `AppError` enum from `common/src/error.rs`.

**Pattern reference:** The advisory list endpoint (`modules/fundamental/src/advisory/endpoints/list.rs`) already implements an identical pattern with the `severity` query parameter. The new code should mirror that struct field definition, extraction logic, and pass-through to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list()` method that queries packages with pagination but no license filtering.

**Changes:**

- **Add a `license` filter parameter to the `list()` method signature:** Add an `Option<String>` parameter (or an equivalent filter struct field) to accept the license filter value from the endpoint layer.

- **Build the filter query using `apply_filter`:** When a `license` value is provided, use the existing `apply_filter` function from `common/src/db/query.rs` (Reuse Candidate) to parse the comma-separated values and generate a SQL `IN` clause. The `apply_filter` function already handles both single and multi-value comma-separated parameters, so no custom parsing logic is needed.

- **Join through `package_license` entity:** Use the `package_license` entity from `entity/src/package_license.rs` (Reuse Candidate) to join the `package` table to the `package_license` table when the license filter is active. This follows SeaORM's join pattern rather than raw SQL.

- **Preserve existing behavior when no filter:** When `license` is `None`, the query should remain unchanged, returning all packages as before (no regression).

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test cases (following existing test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`):**

1. **`test_list_packages_filter_single_license`** -- Verify that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Assert on specific package fields (not just count) to ensure correctness.

2. **`test_list_packages_filter_multiple_licenses`** -- Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that the result set contains packages with both license types and excludes packages with other licenses.

3. **`test_list_packages_no_license_filter`** -- Verify that `GET /api/v2/package` without a `license` parameter returns all packages unchanged. Compare against a known baseline count and verify no filtering is applied.

4. **`test_list_packages_invalid_license`** -- Verify that `GET /api/v2/package?license=` (empty value) or a malformed value returns `400 Bad Request`. Assert on `resp.status()` using `StatusCode::BAD_REQUEST`.

**Conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
- Deserialize response body and validate `PaginatedResults` fields (`total_count`, `items`)
- Assert on specific item field values, not just `items.len()`
- Follow `test_<endpoint>_<scenario>` naming convention
- Each test function gets a `///` doc comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments
- Tests hit a real PostgreSQL test database (integration test pattern)

**Additional integration point:** The test file needs to be registered in `tests/api/` module structure (likely via a `mod` declaration in a parent module file or in `tests/Cargo.toml` test target configuration).

## Files NOT Modified (out of scope)

- `entity/src/package_license.rs` -- Used as-is for the join query; no modifications needed.
- `common/src/db/query.rs` -- The `apply_filter` function is reused directly; no changes needed.
- `modules/fundamental/src/package/endpoints/mod.rs` -- Route registration; no changes needed since the endpoint path (`GET /api/v2/package`) already exists and we are only adding a query parameter.
- `modules/fundamental/src/package/model/summary.rs` -- `PackageSummary` struct already includes a `license` field; the response shape is unchanged.
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper is unchanged.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` (service layer filter logic)
2. Modify `modules/fundamental/src/package/endpoints/list.rs` (endpoint parameter extraction)
3. Create `tests/api/package_license_filter.rs` (integration tests)
4. Run `cargo test` to verify all tests pass
5. Verify acceptance criteria
6. Self-verification (scope check, duplication check, data-flow trace)

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` -> endpoint `list.rs` extracts `license` query param -> passes to `PackageService::list()` -> `apply_filter` parses comma-separated values -> SeaORM query joins `package_license` table and applies `IN` clause -> filtered `PaginatedResults<PackageSummary>` returned -- **COMPLETE**

## API Contract Verification

- The `GET /api/v2/package` endpoint already exists in `modules/fundamental/src/package/endpoints/list.rs`
- Adding an optional query parameter is backward-compatible -- existing clients that do not send `license` will see no change
- Response type `PaginatedResults<PackageSummary>` remains unchanged
