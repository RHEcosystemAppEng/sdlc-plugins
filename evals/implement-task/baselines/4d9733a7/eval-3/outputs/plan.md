# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint to allow filtering packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) must remain unchanged.

## Reuse Strategy

This implementation leverages three existing codebase components rather than writing new parsing, filtering, or query logic:

1. **`common/src/db/query.rs::apply_filter`** -- reuse directly for comma-separated multi-value query parameter parsing and SQL IN clause generation. This function already handles splitting comma-separated strings into individual values and constructing the appropriate SQL `IN` clause. No new parsing logic will be written; the license filter will call `apply_filter` in the same way other filters in the codebase do.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- follow this file as the structural guide for the endpoint-layer changes. The advisory list endpoint already supports a `severity` query parameter using the same filtering approach needed here. The implementation will replicate the same Query struct pattern (adding an optional `license` field) and the same wiring from query parameter extraction through to service invocation.

3. **`entity/src/package_license.rs`** -- use this existing SeaORM entity for the JOIN query between packages and licenses. This entity maps the `package_license` join table and will be used in the service layer to perform the filtered query, avoiding any raw SQL.

## Step-by-step Plan

### Step 1: Modify `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add the `license` query parameter to the package list endpoint.

**Changes:**

1. **Extend the Query struct** -- Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` where the advisory Query struct has an optional `severity` field, add an optional `license` field to the package list Query struct:
   - Add `license: Option<String>` to the Query struct used for deserializing query parameters.
   - Apply the same serde attributes and OpenAPI annotations as the `severity` field in the advisory list endpoint.

2. **Pass the license filter to the service layer** -- In the list handler function, extract the `license` value from the deserialized Query struct and pass it to `PackageService::list()` (or the equivalent service method). Follow the same parameter-passing pattern used in the advisory list endpoint for the severity filter.

3. **Validation** -- Add validation for the `license` parameter value. If an invalid license value is provided (e.g., empty string after splitting), return a `400 Bad Request` response. Follow the error handling pattern (`Result<T, AppError>` with `.context()`) established in sibling endpoint files.

**Files involved:** `modules/fundamental/src/package/endpoints/list.rs` (modify)

### Step 2: Modify `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering logic to the PackageService list method.

**Changes:**

1. **Update the list method signature** -- Add an optional license filter parameter to the `PackageService` list method. This follows the same approach used in `AdvisoryService` for its severity filter.

2. **Build the filtered query using `apply_filter`** -- When the `license` parameter is present:
   - Import and call `common::db::query::apply_filter` to parse the comma-separated license string into individual values and generate the SQL `IN` clause. Do NOT write custom parsing logic -- `apply_filter` already handles this.
   - Use `entity::package_license::Entity` (from `entity/src/package_license.rs`) to construct a JOIN between the `package` table and the `package_license` table.
   - Apply the filter condition on the license SPDX identifier column from the `package_license` entity.

3. **Preserve existing behavior** -- When the `license` parameter is `None`, the query must behave identically to the current implementation (return all packages with standard pagination). No regression in the unfiltered path.

4. **Return type unchanged** -- The method continues to return `PaginatedResults<PackageSummary>`, ensuring the response shape is not affected.

**Files involved:** `modules/fundamental/src/package/service/mod.rs` (modify)

### Step 3: Create `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter feature.

**Changes:**

1. **Test single license filter** -- Send `GET /api/v2/package?license=MIT` and verify only packages with the MIT license are returned. Assert on specific package fields (not just count) to ensure correctness.

2. **Test comma-separated multi-value filter** -- Send `GET /api/v2/package?license=MIT,Apache-2.0` and verify packages matching either license are returned. Assert that the result set contains packages for both license values.

3. **Test no license filter (regression)** -- Send `GET /api/v2/package` without the license parameter and verify all packages are returned unchanged. Compare against the baseline to ensure no regression.

4. **Test invalid license value** -- Send `GET /api/v2/package?license=` (or another invalid value per validation rules) and verify a `400 Bad Request` response is returned.

5. **Test conventions** -- Follow the patterns from sibling test files in `tests/api/` (e.g., `advisory.rs`, `sbom.rs`):
   - Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
   - Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
   - Validate response body deserialization into `PaginatedResults<PackageSummary>`
   - Assert on `total_count`, `items.len()`, and specific item field values
   - Follow `test_<endpoint>_<scenario>` naming convention
   - Add `///` doc comments to every test function explaining what it verifies
   - Use `// Given`, `// When`, `// Then` section comments for non-trivial tests

6. **Register the test module** -- Add `mod package_license_filter;` to the test infrastructure as required by `tests/Cargo.toml`.

**Files involved:** `tests/api/package_license_filter.rs` (create)

### Step 4: Verification

1. **Run tests** -- `cargo test` to ensure all new and existing tests pass.
2. **Scope containment** -- Verify that only the three files listed above were modified/created.
3. **Acceptance criteria check**:
   - `GET /api/v2/package?license=MIT` returns only MIT-licensed packages
   - `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license
   - `GET /api/v2/package` without license param returns all packages (no regression)
   - Response shape `PaginatedResults<PackageSummary>` is unchanged
   - Invalid license values return 400 Bad Request
4. **Duplication check** -- Confirm no new utility functions were created that duplicate `apply_filter` functionality.
5. **Data-flow trace** -- Verify the complete path: HTTP request with `license` query param -> endpoint deserialization -> service method invocation with filter -> `apply_filter` for parsing -> JOIN query via `package_license` entity -> filtered results returned as `PaginatedResults<PackageSummary>`.

## Files Summary

| File | Action | Purpose |
|---|---|---|
| `modules/fundamental/src/package/endpoints/list.rs` | Modify | Add `license` query param to Query struct and pass to service |
| `modules/fundamental/src/package/service/mod.rs` | Modify | Add license filter using `apply_filter` and `package_license` entity JOIN |
| `tests/api/package_license_filter.rs` | Create | Integration tests for single, multi-value, no-filter, and invalid cases |

## What is NOT being done

- No new utility functions for parsing comma-separated values -- `apply_filter` from `common/src/db/query.rs` handles this.
- No raw SQL -- the `package_license` entity from `entity/src/package_license.rs` provides the SeaORM model for the JOIN.
- No changes to the response shape -- `PaginatedResults<PackageSummary>` remains unchanged.
- No changes to files outside the three listed above.
