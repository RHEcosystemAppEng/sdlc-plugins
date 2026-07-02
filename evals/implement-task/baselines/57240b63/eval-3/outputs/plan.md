# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the existing severity filter pattern from the advisory list endpoint and reuses shared query infrastructure.

## Scope

### Files to Modify

1. **`modules/fundamental/src/package/endpoints/list.rs`** -- add license query parameter extraction and filtering
2. **`modules/fundamental/src/package/service/mod.rs`** -- add license filter to PackageService list method

### Files to Create

1. **`tests/api/package_license_filter.rs`** -- integration tests for the license filter

No other files are created or modified.

---

## Detailed Changes

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Structural guide**: Follow the pattern in `modules/fundamental/src/advisory/endpoints/list.rs`, which already implements a `severity` query parameter on its list endpoint using an optional field in a Query struct.

**Changes**:

- **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing query parameter struct used for the package list endpoint. This mirrors how the advisory endpoint's Query struct carries an optional `severity` field.

  ```rust
  // In the existing Query struct for the package list endpoint:
  pub license: Option<String>,
  ```

- **Pass the license filter to the service layer**: In the handler function for `GET /api/v2/package`, extract `query.license` and pass it to `PackageService::list()` (or the equivalent method). This follows the same flow as the advisory endpoint passes its `severity` parameter down to its service.

- **No changes to the response shape**: The return type remains `PaginatedResults<PackageSummary>`. The `license` parameter is input-only.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Changes**:

- **Accept a license filter parameter**: Modify the `list` method (or equivalent) on `PackageService` to accept an optional license filter string (`Option<String>`).

- **Apply the filter using `common/src/db/query.rs::apply_filter`**: When the `license` parameter is `Some`, use the existing `apply_filter` function from `common/src/db/query.rs` to handle:
  - Parsing the comma-separated string into individual license identifiers
  - Generating a SQL `IN` clause for multi-value matching
  - Single-value matching as a degenerate case of the above

  This is the critical reuse point. The `apply_filter` function already handles both single and comma-separated multi-value parameters, so no new parsing logic is needed.

  ```rust
  // Pseudocode for the service method:
  if let Some(license_param) = license {
      // apply_filter handles comma-separated parsing and IN clause generation
      apply_filter(&mut query_builder, "license", &license_param);
  }
  ```

- **JOIN through `package_license` entity**: Use the `package_license` entity defined in `entity/src/package_license.rs` to join the packages table to the licenses table. This entity already maps the relationship between packages and their declared licenses. The join is done via SeaORM entity relations rather than raw SQL.

  ```rust
  // Use the existing PackageLicense entity for the join:
  use entity::package_license;

  // Join packages to package_license to filter by license identifier
  query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
  ```

- **Validate license values**: When the `license` parameter is provided but contains invalid values (empty strings after splitting, or malformed identifiers), return a 400 Bad Request error. This validation should happen early, before constructing the query.

### 3. `tests/api/package_license_filter.rs` (new file)

**Structure**: Follow the existing integration test patterns in `tests/api/`.

**Test cases**:

1. **Test single license filter**: Seed the database with packages having different licenses (e.g., MIT, Apache-2.0, GPL-3.0). Call `GET /api/v2/package?license=MIT`. Assert that only packages with the MIT license are returned and the response shape is `PaginatedResults<PackageSummary>`.

2. **Test comma-separated license filter**: Using the same seeded data, call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert that packages matching either MIT or Apache-2.0 are returned. Assert that GPL-3.0 packages are excluded.

3. **Test no license filter (no regression)**: Call `GET /api/v2/package` without a `license` parameter. Assert that all packages are returned, confirming backward compatibility.

4. **Test invalid license value returns 400**: Call `GET /api/v2/package?license=` (empty value) or with a clearly malformed value. Assert a 400 Bad Request response.

---

## Reuse Strategy

| Component | Reuse Approach |
|---|---|
| `common/src/db/query.rs::apply_filter` | Call directly for comma-separated parsing and SQL IN clause generation -- no new parsing logic written |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Follow the same Query struct + optional field + service pass-through pattern as the severity filter |
| `entity/src/package_license.rs` | Use the existing entity for the package-license JOIN; no raw SQL or new entity definition |

## Execution Order

1. Modify `modules/fundamental/src/package/endpoints/list.rs` -- add `license` field to Query struct and pass it to the service
2. Modify `modules/fundamental/src/package/service/mod.rs` -- accept the license filter, apply `apply_filter` with a join through `package_license`
3. Create `tests/api/package_license_filter.rs` -- write all four test cases
4. Run the full test suite to confirm no regressions
