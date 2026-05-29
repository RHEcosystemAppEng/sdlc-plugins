# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing infrastructure throughout: the `apply_filter` utility for parameter parsing, the advisory severity-filter pattern for endpoint structure, and the `package_license` entity for the database join.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Goal**: Accept and forward the new `license` query parameter.

**Changes**:

- **Add a `license` field to the `Query` struct** (or the equivalent query-parameter struct used by this endpoint). Follow the exact pattern used by `modules/fundamental/src/advisory/endpoints/list.rs` for its `severity` field: declare an `Option<String>` field named `license` with the same serde/actix-web extraction attributes. This ensures the parameter is optional and absent requests continue to return all packages.

- **Pass the `license` value into the service layer**. After extracting the query parameters, forward `query.license` to `PackageService::list()` (or the equivalent list method) as an additional argument. This mirrors how the advisory endpoint forwards its `severity` value to the advisory service.

- **Validation**: If the license value is present but contains only whitespace or empty segments after splitting on commas, return a `400 Bad Request`. Follow whatever validation pattern the advisory severity filter uses (e.g., checking for empty strings after split). If the advisory endpoint delegates validation to `apply_filter`, do the same here.

No new utility functions are introduced here; the endpoint struct gains one field and the handler gains one forwarded argument.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Goal**: Apply the license filter to the database query in the PackageService list method.

**Changes**:

- **Add a `license` parameter** to the list method signature (e.g., `license: Option<String>`), matching the type used in the advisory service for its severity filter.

- **Build the filter using `common::db::query::apply_filter`**. When `license` is `Some(value)`:
  1. Call `apply_filter` with the license string. `apply_filter` handles splitting the comma-separated values and generating the appropriate SQL `IN` clause. No custom parsing or splitting logic is written.
  2. The filter targets the `license` column (SPDX identifier column) in the `package_license` table.

- **Join through `entity::package_license`**. Use the `package_license` entity (from `entity/src/package_license.rs`) to perform a JOIN between the `package` table and the `package_license` table. This is necessary because licenses are stored in a separate join table, not inline on the package row. The join condition links `package.id` to `package_license.package_id`.

- **Preserve existing query behavior**. When `license` is `None`, the existing query executes unchanged -- no join is added, no filter is applied, and the response shape (`PaginatedResults<PackageSummary>`) is identical. This guarantees no regression for callers that omit the parameter.

- **Return 400 on invalid license values**. If `apply_filter` or surrounding validation detects an invalid value (empty string, malformed SPDX identifiers based on the existing validation approach), propagate the error as a 400 response.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Goal**: Integration tests covering all acceptance criteria and test requirements.

**Test cases**:

1. **`test_single_license_filter`** -- Seed packages with various licenses. Send `GET /api/v2/package?license=MIT`. Assert the response contains only MIT-licensed packages. Assert the response shape is `PaginatedResults<PackageSummary>`.

2. **`test_multi_license_filter`** -- Send `GET /api/v2/package?license=MIT,Apache-2.0`. Assert the response contains packages matching either MIT or Apache-2.0. Assert no packages with other licenses appear.

3. **`test_no_license_filter`** -- Send `GET /api/v2/package` (no license parameter). Assert the response contains all seeded packages. This is the regression check.

4. **`test_invalid_license_returns_400`** -- Send `GET /api/v2/package?license=` (empty value) or a clearly invalid value. Assert a 400 Bad Request response.

**Test infrastructure**: Follow the existing test patterns in `tests/api/` for setting up the test server, seeding data, and making HTTP requests. Use the same test utilities and fixtures already present in the test suite.

---

## Reuse Strategy Summary

| Existing Code | How It Is Reused |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly to parse comma-separated license values and generate the SQL IN clause. No custom parsing logic is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Its severity filter pattern is followed structurally: same Query struct field declaration, same parameter forwarding to the service layer, same validation approach. |
| `entity/src/package_license.rs` | Used as the join entity to connect packages to their licenses in the database query, avoiding raw SQL. |

## Scope Boundaries

- No new utility functions are created that would duplicate `apply_filter` functionality.
- No changes to the response shape (`PaginatedResults<PackageSummary>`).
- All modifications stay within the three files listed above.
- No changes to entity definitions, database migrations, or other endpoints.
