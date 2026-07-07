# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing infrastructure throughout: `apply_filter` for parsing and SQL generation, the advisory list endpoint pattern for structural guidance, and the `package_license` entity for the JOIN query.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add the `license` query parameter to the package list endpoint handler.

**Changes:**

- **Extend the `Query` struct** (or equivalent request-parameter struct) to include a new optional field:
  ```rust
  pub license: Option<String>,
  ```
  This follows the exact same pattern used for filter parameters in `modules/fundamental/src/advisory/endpoints/list.rs` (e.g., the `severity` field on its Query struct).

- **Pass the license parameter to the service layer.** In the handler function that processes `GET /api/v2/package`, extract `query.license` and forward it to `PackageService::list()` (or equivalent method). No manual parsing of comma-separated values is performed here — that responsibility belongs to `apply_filter` in the service layer.

- **No new utility functions are created.** The endpoint layer is a thin pass-through; all filtering logic is delegated to the service via `apply_filter`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Apply the license filter when building the database query for listing packages.

**Changes:**

- **Add a `license` parameter** to the `list` method signature (or to whatever options/filter struct it accepts), typed as `Option<String>`.

- **Join through the `package_license` entity.** When a license filter is present, add a JOIN from the package table to the `package_license` table using the relationship defined in `entity/src/package_license.rs`. Use SeaORM's relation-based join (e.g., `.join()` or `.find_also_related()`) referencing the `PackageLicense` entity — do NOT write raw SQL or create a new entity.

- **Call `apply_filter` from `common/src/db/query.rs`** to handle the license value. `apply_filter` already handles:
  - Comma-separated multi-value parsing (splitting `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`)
  - SQL `IN` clause generation for multi-value filters
  - Single-value exact-match filtering

  The call will look structurally similar to how filters are applied in the advisory list service, e.g.:
  ```rust
  if let Some(license) = &license {
      query = apply_filter(query, package_license::Column::License, license)?;
  }
  ```
  This reuses `apply_filter` directly — no new parsing or filter-building logic is written.

- **Return 400 for invalid license values.** If `apply_filter` returns an error (e.g., empty string after splitting, malformed input), propagate it as a 400 Bad Request. This mirrors the error-handling pattern in the advisory endpoints.

- **Response shape is unchanged.** The SELECT columns and serialization remain the same; only the WHERE/JOIN clauses are modified.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests validating the license filter end-to-end.

**Test cases:**

1. **Single license filter** — `GET /api/v2/package?license=MIT`
   - Seed the database with packages having different licenses (MIT, Apache-2.0, GPL-3.0).
   - Assert the response contains only packages with the MIT license.
   - Assert response shape matches the unfiltered response shape.

2. **Comma-separated multi-value filter** — `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert the response contains packages matching either MIT or Apache-2.0.
   - Assert packages with other licenses (e.g., GPL-3.0) are excluded.

3. **No license filter** — `GET /api/v2/package`
   - Assert all packages are returned regardless of license.
   - Confirms the filter is truly optional and does not regress existing behavior.

4. **Invalid license value returns 400** — `GET /api/v2/package?license=`
   - Assert the endpoint returns HTTP 400.
   - Test other invalid inputs as appropriate (e.g., only commas: `?license=,,,`).

**Structure:** Follow the test patterns already established in the `tests/api/` directory — use the existing test harness, HTTP client setup, and database seeding utilities.

---

## Summary of changes by layer

| Layer | File | Action |
|-------|------|--------|
| Endpoint | `modules/fundamental/src/package/endpoints/list.rs` | Add `license` field to Query struct, pass to service |
| Service | `modules/fundamental/src/package/service/mod.rs` | JOIN `package_license`, call `apply_filter`, handle errors |
| Test | `tests/api/package_license_filter.rs` | Create — 4 integration test cases |

No new utility functions, entities, or modules are created. All filtering logic is delegated to the existing `apply_filter` function.
