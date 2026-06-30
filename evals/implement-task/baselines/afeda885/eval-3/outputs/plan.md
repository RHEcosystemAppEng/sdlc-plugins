# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and
comma-separated multi-value filtering by SPDX license identifier. The response shape
(`PaginatedResults<PackageSummary>`) remains unchanged.

## Repository

trustify-backend (target branch: main)

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with existing query parameters (pagination,
sorting) but no license filter.

**Changes:**

- Add an optional `license: Option<String>` field to the `Query` struct used for
  query parameter extraction (following the same pattern as the `severity` field in the
  advisory list endpoint's Query struct at `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, pass the extracted `license` parameter through to
  `PackageService::list()` so the service layer can apply the filter.
- Validate the `license` parameter: if provided but empty or containing only whitespace,
  return 400 Bad Request using `AppError` from `common/src/error.rs`.
- Reuse `common/src/db/query.rs::apply_filter` to parse the comma-separated license
  string into individual values and generate the SQL `IN` clause. Do NOT write custom
  parsing logic for comma separation — `apply_filter` already handles this.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list()` method that queries the `package` table
with pagination and sorting but no license filtering.

**Changes:**

- Add an optional `license` parameter (e.g., `license_filter: Option<String>`) to the
  `list()` method signature.
- When `license_filter` is `Some`, join the `package_license` table using the entity
  definition from `entity/src/package_license.rs`. Use SeaORM's relation-based join
  (following the existing entity relationship) rather than writing raw SQL.
- Apply the filter using `apply_filter` from `common/src/db/query.rs` to handle
  comma-separated values, generating a `WHERE package_license.license IN (...)` clause.
- When `license_filter` is `None`, skip the join and filter entirely, preserving the
  existing behavior (no regression).

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on `GET /api/v2/package`.

**Test cases:**

1. **`test_filter_single_license`** — Verify that `GET /api/v2/package?license=MIT` returns
   only packages with MIT license. Assert on specific package identifiers in the response,
   not just the count. Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body
   deserialization into `PaginatedResults<PackageSummary>`.

2. **`test_filter_comma_separated_licenses`** — Verify that
   `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
   Assert that returned packages have either MIT or Apache-2.0 license, and that the
   response includes packages for both licenses.

3. **`test_no_license_filter_returns_all`** — Verify that `GET /api/v2/package` without a
   license parameter returns all packages unchanged (no regression). Compare against a
   known test dataset count and spot-check specific package entries.

4. **`test_invalid_license_returns_400`** — Verify that an invalid license value returns
   `StatusCode::BAD_REQUEST`. Assert on the response status code.

**Conventions to follow (from sibling test analysis of `tests/api/advisory.rs`, `tests/api/sbom.rs`):**
- Use `assert_eq!(resp.status(), ...)` pattern for status checks.
- Validate `total_count`, `items.len()`, and at least one item's key fields.
- Include error case tests (400/404).
- Follow `test_<endpoint>_<scenario>` naming convention.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

## How Existing Code Is Reused

1. **`common/src/db/query.rs::apply_filter`** — Reused directly for parsing the
   comma-separated `license` parameter and generating the SQL `IN` clause. No new
   parsing utility is created; `apply_filter` already handles both single and
   multi-value comma-separated parameters.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** — The severity filter
   implementation serves as the structural template. The package list endpoint's
   `Query` struct will add an optional `license` field following the exact same
   pattern as the advisory endpoint's optional `severity` field. The handler passes
   the filter to the service layer in the same way.

3. **`entity/src/package_license.rs`** — The existing SeaORM entity for the
   package-license join table is used for the JOIN query in the service layer.
   No raw SQL is written; the entity's defined relations are used to perform
   the join through SeaORM's query builder.

## Data-Flow Trace

- **Input:** `license` query parameter arrives in the HTTP request to `GET /api/v2/package`.
- **Extraction:** The `Query` struct in `list.rs` extracts the optional `license` string
  from query parameters.
- **Validation:** If present but invalid (empty/whitespace), return 400 via `AppError`.
- **Processing:** `PackageService::list()` receives the filter, joins `package_license`
  using the entity, and applies `apply_filter` to generate the `IN` clause.
- **Output:** Filtered results are returned as `PaginatedResults<PackageSummary>` — same
  response shape as before, just with filtered contents.

All stages are connected end-to-end. No stage is missing or disconnected.

## Scope Boundaries

All modifications are strictly within the files listed in Files to Modify and Files to
Create. No other files need changes:
- Route registration in `modules/fundamental/src/package/endpoints/mod.rs` does not need
  modification (the list handler signature change is internal).
- `PackageSummary` model is unchanged.
- `PaginatedResults` wrapper is unchanged.
- No new migration is needed (the `package_license` table already exists).
