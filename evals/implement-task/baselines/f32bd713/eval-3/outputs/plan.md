# Implementation Plan -- TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting
both single-value and comma-separated multi-value filtering by SPDX license identifier.
The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests with existing query parameters
(pagination, sorting) but no license filter.

**Changes:**

- **Add `license` field to the Query struct.** Following the pattern established in
  `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter), add an
  `Option<String>` field named `license` to the existing query parameter extraction struct.
  This matches the advisory list endpoint's approach of using an optional string field on
  the Query struct for filter parameters.

- **Pass the license filter value to the service layer.** In the handler function, extract
  `query.license` and pass it to `PackageService::list()` as an additional parameter. If
  `query.license` is `None`, no filtering is applied (preserving backward compatibility).

- **Validate the license parameter.** If the `license` value is present but empty or
  contains invalid characters, return a `400 Bad Request` via `AppError`. Follow the
  existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping.

**Reuse:** The Query struct pattern with an optional filter field is reused directly from
the advisory list endpoint's severity filter implementation. No new query parameter
parsing utilities are needed.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries all packages with
pagination and sorting but no license filtering.

**Changes:**

- **Add a `license: Option<String>` parameter to the `list` method signature.** This
  parameter carries the raw comma-separated license string from the endpoint layer.

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`.** Call
  `apply_filter` with the `license` parameter value and the `package_license` entity's
  license column. `apply_filter` already handles:
  - Splitting comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
  - Generating the appropriate SQL `IN` clause
  - Handling single-value inputs without the comma split

  This is the core reuse point -- `apply_filter` provides all the multi-value filtering
  mechanics, so no new parsing or SQL generation code is needed.

- **Join through the `package_license` entity.** Use the SeaORM entity defined in
  `entity/src/package_license.rs` to join the `package` table to the `package_license`
  table. This entity already maps the package-license relationship, so no raw SQL or new
  entity definitions are needed. The join is added conditionally -- only when `license`
  is `Some`.

- **Preserve existing behavior when no filter is provided.** When `license` is `None`,
  the query runs without the join or filter, returning all packages as before.

**Reuse:**
- `apply_filter` from `common/src/db/query.rs` -- reused directly, not reimplemented.
- `package_license` entity from `entity/src/package_license.rs` -- used for the JOIN,
  not replaced with raw SQL.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on `GET /api/v2/package`.

**Test cases:**

- **`test_single_license_filter`** -- Verifies that `GET /api/v2/package?license=MIT`
  returns only packages with the MIT license. Asserts on specific package identifiers
  in the response, not just the count, following the skill's guidance to prefer value-based
  assertions over length-only checks.

- **`test_multi_license_filter`** -- Verifies that
  `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
  Asserts that the result set contains packages with both MIT and Apache-2.0 licenses
  and excludes packages with other licenses.

- **`test_no_license_filter_returns_all`** -- Verifies that `GET /api/v2/package` without
  a `license` parameter returns all packages unchanged (no regression).

- **`test_invalid_license_returns_400`** -- Verifies that an invalid license value
  results in a `400 Bad Request` response.

**Conventions followed:**
- Uses the `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling test files
  (`tests/api/advisory.rs`, `tests/api/sbom.rs`).
- Hits a real PostgreSQL test database (integration test pattern).
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- Test data setup seeds packages with known licenses before asserting filter results.

**Integration:** The test file must be registered in `tests/api/` (e.g., added as a
`mod` declaration if the test directory uses a `mod.rs` pattern, or added to `Cargo.toml`
if tests are listed explicitly).

---

## Data-Flow Trace

1. **Input:** HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Extraction:** Axum deserializes query parameters into the Query struct; `license`
   field is populated with `Some("MIT,Apache-2.0")`
3. **Validation:** Handler validates the license value is non-empty and well-formed;
   returns 400 if invalid
4. **Service call:** Handler passes `license` to `PackageService::list()`
5. **Filter application:** Service calls `apply_filter()` with the license string and
   the `package_license` entity column, producing an SQL `WHERE license IN ('MIT', 'Apache-2.0')`
   clause with a JOIN through `package_license`
6. **Query execution:** SeaORM executes the filtered, paginated query against PostgreSQL
7. **Response:** Results are wrapped in `PaginatedResults<PackageSummary>` and returned
   as JSON -- the response shape is unchanged

All stages are connected; no missing or disconnected stages.

---

## Scope Containment

All changes are strictly within the files specified in the task:

| File | Section | Action |
|------|---------|--------|
| `modules/fundamental/src/package/endpoints/list.rs` | Files to Modify | Modify |
| `modules/fundamental/src/package/service/mod.rs` | Files to Modify | Modify |
| `tests/api/package_license_filter.rs` | Files to Create | Create |

No out-of-scope files are modified. The `common/src/db/query.rs` file and
`entity/src/package_license.rs` file are used (imported) but not modified -- they
provide existing functionality that is reused as-is.
