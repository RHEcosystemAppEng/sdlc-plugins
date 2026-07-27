# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports both single-value
(`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering by
SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) remains
unchanged; only the input accepts a new optional parameter.

## Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with pagination and sorting but no license
filtering.

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern established in
  `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate #2), add an
  optional `license: Option<String>` field to the endpoint's query parameter struct.
  This matches how the advisory list endpoint handles its `severity` filter -- an optional
  string field deserialized from query parameters by Axum's extractor.

- **Parse and validate the license parameter:** When the `license` query parameter is
  present, pass it to `common/src/db/query.rs::apply_filter` (Reuse Candidate #1) to
  handle comma-separated multi-value parsing and SQL `IN` clause generation. Do NOT
  write a custom parser for comma-separated values -- `apply_filter` already handles
  this. If the license value is empty or contains invalid characters, return a 400 Bad
  Request using the existing `AppError` enum from `common/src/error.rs`.

- **Pass the filter to the service layer:** Propagate the parsed license filter value
  to `PackageService::list()` as an additional parameter (or via a filter/options struct,
  matching whatever pattern the advisory service uses).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries packages with
pagination/sorting but no license filtering.

**Changes:**

- **Accept a license filter parameter:** Add an optional license filter parameter to
  the `list` method signature. Follow the same pattern used in
  `modules/fundamental/src/advisory/service/advisory.rs` where the advisory service
  accepts filter parameters from the endpoint layer.

- **Build a JOIN query using `entity::package_license`:** When the license filter is
  present, construct a query that JOINs the `package` table with the `package_license`
  table (Reuse Candidate #3, `entity/src/package_license.rs`). Use SeaORM's relation
  and join capabilities rather than raw SQL. The `package_license` entity already maps
  the package-to-license relationship, so leverage its defined `Relation` for the JOIN.

- **Apply the filter via `apply_filter`:** Pass the license values through
  `common/src/db/query.rs::apply_filter` (Reuse Candidate #1) to generate the
  appropriate `WHERE ... IN (...)` clause on the license SPDX identifier column from
  the `package_license` entity. This handles both single-value and multi-value cases
  uniformly.

- **Preserve existing behavior:** When no license filter is provided, the query must
  remain unchanged -- no JOIN is added, no filtering occurs. The
  `PaginatedResults<PackageSummary>` response shape is unaffected.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test cases (following sibling test conventions from `tests/api/advisory.rs` and
`tests/api/sbom.rs`):**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist in the test DB
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status is 200; all returned packages have MIT license; assert on
     specific package identifiers (value-based, not just count)

2. **`test_list_packages_filter_multi_license`**
   - Doc comment: `/// Verifies that comma-separated license values return packages matching any listed license.`
   - Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status is 200; returned packages have either MIT or Apache-2.0
     license; GPL-3.0 packages are excluded; assert on specific values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: packages with various licenses exist
   - When: `GET /api/v2/package` (no license parameter)
   - Then: response status is 200; all packages returned; response shape matches
     `PaginatedResults<PackageSummary>`

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: test DB is set up
   - When: `GET /api/v2/package?license=` (empty value or obviously invalid)
   - Then: response status is 400

**Conventions followed:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Use given-when-then section comments inside non-trivial tests
- Test naming follows `test_<endpoint>_<scenario>` pattern
- Hit real PostgreSQL test database (integration test pattern)
- Each test function has a `///` doc comment

**Module registration:** Add `mod package_license_filter;` to `tests/api/mod.rs` (or
the test harness entry point) so the new test file is compiled and run.

---

## Data-Flow Trace

```
Request: GET /api/v2/package?license=MIT,Apache-2.0
  -> Axum extracts Query struct (endpoints/list.rs) with license: Some("MIT,Apache-2.0")
  -> Endpoint handler passes license value to PackageService::list()
  -> Service calls apply_filter() to parse "MIT,Apache-2.0" into ["MIT", "Apache-2.0"]
  -> Service builds SeaORM query: JOIN package_license, WHERE spdx_id IN ("MIT", "Apache-2.0")
  -> Query executes against PostgreSQL
  -> Results mapped to PaginatedResults<PackageSummary>
  -> Response returned as JSON (shape unchanged)
```

All stages connected -- COMPLETE.

---

## Scope Boundaries

Only the files listed in Files to Modify and Files to Create are touched. No changes to:
- `entity/src/package_license.rs` (used as-is for the JOIN)
- `common/src/db/query.rs` (used as-is for `apply_filter`)
- `modules/fundamental/src/advisory/endpoints/list.rs` (referenced as a pattern only)
- `modules/fundamental/src/package/model/summary.rs` (response shape unchanged)
- `modules/fundamental/src/package/endpoints/mod.rs` (route registration unchanged -- the
  existing route for `GET /api/v2/package` already points to `list.rs`)

## Commit Message

```
feat(api): add license filter to GET /api/v2/package

Support single and comma-separated SPDX license filtering on the
package list endpoint using apply_filter and package_license JOIN.

Implements TC-9203
```
