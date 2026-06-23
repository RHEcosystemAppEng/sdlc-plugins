# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint that supports
both single-value and comma-separated multi-value filtering by SPDX license identifier.
The implementation reuses existing filtering infrastructure throughout.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Defines the handler for `GET /api/v2/package` with a query parameter
struct for pagination/sorting but no license filtering.

**Changes:**

- **Add `license` field to the query parameter struct:** Add an `Option<String>` field
  named `license` to the existing query parameters struct (following the same pattern as
  the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`). This
  field accepts a raw comma-separated string from the query string.

- **Pass the license filter to the service layer:** In the handler function, extract
  `query.license` and pass it to `PackageService::list()` as an additional parameter.
  Do not parse or split the comma-separated value here — that responsibility belongs to
  `apply_filter` in the service/query layer.

- **Validation:** Add input validation for the `license` parameter. If the value is
  present but empty or contains only commas/whitespace, return a `400 Bad Request`
  using the existing `AppError` enum from `common/src/error.rs`. Follow the same
  validation pattern used in the advisory severity filter.

**Reuse:**
- Follow the exact struct field pattern from `advisory/endpoints/list.rs` (the `severity`
  query parameter field).
- Use `AppError` from `common/src/error.rs` for validation errors.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list()` method that queries the
`package` table with pagination/sorting but no license filtering.

**Changes:**

- **Add `license` parameter to `list()` method signature:** Add an `Option<String>`
  parameter for the license filter value.

- **Apply the license filter using `apply_filter`:** When the `license` parameter is
  `Some(value)`, call `apply_filter` from `common/src/db/query.rs` to parse the
  comma-separated string and generate the appropriate SQL `IN` clause. This function
  already handles splitting on commas and building the filter condition.

- **Join through `package_license` entity:** Use the `package_license` entity from
  `entity/src/package_license.rs` to join the `package` table to the `package_license`
  table. Apply the `apply_filter` result against the `license` column of the
  `package_license` table. Use SeaORM's relation-based join (following the entity's
  defined relations) rather than writing raw SQL.

- **Preserve existing behavior:** When `license` is `None`, the query executes without
  the join or filter, preserving the current behavior exactly (no regression).

- **Return type unchanged:** The method continues to return `PaginatedResults<PackageSummary>`.

**Reuse:**
- `apply_filter` from `common/src/db/query.rs` — called directly to handle comma-separated
  parsing and SQL IN clause generation.
- `package_license` entity from `entity/src/package_license.rs` — used for the JOIN, not
  raw SQL.
- Pattern from `advisory/service/advisory.rs` or `advisory/service/mod.rs` — follow how
  the advisory service applies the severity filter to its query.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test cases (following sibling test conventions in `tests/api/`):**

1. **`test_filter_by_single_license`** — Verify that `GET /api/v2/package?license=MIT`
   returns only packages with the MIT license. Assert on specific package identifiers
   in the response, not just the count.

2. **`test_filter_by_multiple_licenses`** — Verify that
   `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
   Assert that each returned package has one of the specified licenses.

3. **`test_no_license_filter_returns_all`** — Verify that `GET /api/v2/package` without a
   `license` parameter returns all packages (regression test). Compare against a known
   total count from test fixtures.

4. **`test_invalid_license_returns_400`** — Verify that an invalid license value returns
   `400 Bad Request`. Assert on `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions to follow (from sibling tests in `tests/api/`):**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for success cases.
- Deserialize response body to `PaginatedResults<PackageSummary>`.
- Validate `total_count`, `items.len()`, and specific item field values.
- Use `/// doc comments` on every test function.
- Use `// Given`, `// When`, `// Then` section comments for non-trivial tests.
- Follow `test_<endpoint>_<scenario>` naming convention.

**Integration with test infrastructure:**
- The test file must be added to `tests/api/mod.rs` (or equivalent module declaration)
  so the test runner discovers it. This is a minor modification to an existing file that
  is within the scope of `tests/api/` integration test infrastructure.

## Files NOT Modified

- `entity/src/package_license.rs` — used as-is for the JOIN, no changes needed.
- `common/src/db/query.rs` — `apply_filter` is used as-is, no changes needed.
- `modules/fundamental/src/advisory/endpoints/list.rs` — referenced as a pattern only,
  not modified.
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` already includes
  the `license` field; the response shape does not change.
- `modules/fundamental/src/package/endpoints/mod.rs` — route registration does not change
  since the endpoint path remains the same; only the handler's accepted query parameters
  change.

## Data Flow

```
HTTP Request: GET /api/v2/package?license=MIT,Apache-2.0
  |
  v
list.rs (endpoint handler)
  - Extracts `license: Option<String>` from query params
  - Validates input (non-empty if present)
  - Calls PackageService::list(..., license)
  |
  v
service/mod.rs (PackageService::list)
  - If license is Some, calls apply_filter() from common/src/db/query.rs
  - apply_filter splits "MIT,Apache-2.0" into ["MIT", "Apache-2.0"]
  - Builds SeaORM query with JOIN on package_license entity
  - Applies WHERE package_license.license IN ('MIT', 'Apache-2.0')
  - Executes query with existing pagination
  |
  v
Response: PaginatedResults<PackageSummary> (unchanged shape)
```

## Commit Strategy

A single commit following Conventional Commits:

```
feat(api): add license filter to GET /api/v2/package

Support filtering packages by SPDX license identifier via the `license`
query parameter. Accepts single values and comma-separated multi-values.

Implements TC-9203
```
