# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and
comma-separated multi-value filtering by SPDX license identifier. The implementation
reuses existing query infrastructure and follows established patterns from the advisory
module.

## Structural Guide

The advisory list endpoint at `modules/fundamental/src/advisory/endpoints/list.rs`
already implements an optional `severity` query parameter using the same filtering
approach needed here. This file serves as the structural template for all changes: the
Query struct pattern with an optional filter field, the extraction of the parameter in
the handler, and the delegation to the service layer with the filter applied.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint handler.

**Changes**:
- Add an optional `license: Option<String>` field to the `Query` (or equivalent
  query-parameter extraction struct), following the same pattern used for the `severity`
  field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` value from the query parameters.
- Pass the extracted `license` filter value down to `PackageService::list()` (or the
  equivalent service method) as an additional parameter.
- Use `common/src/db/query.rs::apply_filter` to handle both single-value (`license=MIT`)
  and comma-separated multi-value (`license=MIT,Apache-2.0`) parsing. Do NOT write
  custom parsing logic for splitting comma-separated values -- `apply_filter` already
  handles this.
- Add input validation for the license parameter: return 400 Bad Request for invalid
  values (empty strings after splitting, malformed identifiers).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the PackageService list method.

**Changes**:
- Modify the `list` method (or equivalent query-building method) to accept the optional
  license filter parameter.
- When the license filter is present, add a JOIN to the `package_license` table using
  the `entity/src/package_license.rs` SeaORM entity. This entity already defines the
  package-to-license relationship and column mappings -- use it directly rather than
  writing raw SQL or creating a new entity.
- Apply the filter using `common/src/db/query.rs::apply_filter` to generate the
  appropriate SQL `IN` clause for multi-value filtering against the license column
  of the joined `package_license` table.
- Ensure that when no `license` parameter is provided, the query remains unchanged
  (no JOIN, no filter) to prevent regression on existing behavior.
- Follow the same `Result<T, AppError>` error handling pattern with `.context()`
  wrapping used by sibling service methods (e.g., `AdvisoryService`, `SbomService`).

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter feature.

**Changes**:
- Create integration tests following the patterns in sibling test files
  (`tests/api/advisory.rs`, `tests/api/sbom.rs`).
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with existing tests.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

**Test cases**:

1. `test_list_packages_filter_single_license` -- verifies that `GET /api/v2/package?license=MIT`
   returns only packages with the MIT license. Asserts on specific package identifiers in
   the response, not just the count.

2. `test_list_packages_filter_multi_license` -- verifies that
   `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
   Asserts that the result set contains packages with both license types and excludes
   packages with other licenses.

3. `test_list_packages_no_license_filter` -- verifies that `GET /api/v2/package` without
   the license parameter returns all packages unchanged (no regression). Compares the
   full result set against the expected baseline.

4. `test_list_packages_invalid_license` -- verifies that an invalid license value returns
   `400 Bad Request`. Asserts on the status code and error response shape.

- Register the test file in `tests/api/` module structure (e.g., add `mod package_license_filter;`
  to the appropriate `mod.rs` or `main.rs` test harness file if required by the project's
  test organization).

## What This Plan Does NOT Do

- Does not create new utility functions for parsing comma-separated values -- reuses
  `apply_filter` from `common/src/db/query.rs` which already provides this functionality.
- Does not write raw SQL for the package-license join -- uses the existing SeaORM entity
  at `entity/src/package_license.rs`.
- Does not modify the response shape (`PaginatedResults<PackageSummary>`) -- only the
  input accepts a new optional parameter.
- Does not modify any files outside the scope defined in Files to Modify and Files to
  Create.

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` request arrives at handler in `endpoints/list.rs`
  -> query parameter extracted into Query struct -> `license` value passed to
  `PackageService::list()` in `service/mod.rs` -> `apply_filter` from
  `common/src/db/query.rs` parses comma-separated values and generates SQL IN clause
  -> JOIN with `package_license` entity from `entity/src/package_license.rs` filters
  matching rows -> `PaginatedResults<PackageSummary>` returned unchanged -> JSON
  response -- COMPLETE
