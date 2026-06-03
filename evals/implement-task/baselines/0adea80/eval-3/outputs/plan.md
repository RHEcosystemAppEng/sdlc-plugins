# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Supports both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the existing severity filter pattern from the advisory list endpoint and reuses shared query utilities throughout.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint handler.

**Changes**:

- **Add `license` field to the Query struct**: Following the pattern established in `modules/fundamental/src/advisory/endpoints/list.rs` (where the `severity` field is an `Option<String>` on the advisory Query struct), add an `Option<String>` field named `license` to the package endpoint's Query struct. This field will capture the raw query parameter value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing fields (pagination, sorting, etc.)
      pub license: Option<String>,
  }
  ```

- **Pass the license filter to the service layer**: In the handler function that processes `GET /api/v2/package`, extract `query.license` and pass it to `PackageService::list()`. This mirrors how the advisory handler passes `query.severity` to the advisory service.

- **Validation**: If the `license` parameter is present but contains invalid values (empty segments after splitting on commas, or other malformed input), return a 400 Bad Request via `AppError`. This follows the existing error handling convention where handlers return `Result<T, AppError>` with `.context()` wrapping.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService::list` method.

**Changes**:

- **Update `list` method signature**: Add an optional `license: Option<String>` parameter (or accept it as part of an expanded filter/query struct, depending on the existing method signature pattern).

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`**: When the `license` parameter is `Some`, call the shared `apply_filter` function to parse the comma-separated values and generate the appropriate SQL `IN` clause. This is the same function used throughout the codebase for multi-value filtering, and it handles:
  - Single value: generates a `WHERE license = 'MIT'` equivalent
  - Comma-separated values: generates a `WHERE license IN ('MIT', 'Apache-2.0')` equivalent

- **JOIN through `package_license` entity**: Use the SeaORM entity defined in `entity/src/package_license.rs` to join the packages table to the package_license table. This avoids writing raw SQL and stays consistent with the SeaORM-based query building used elsewhere. The join condition links `package.id` to `package_license.package_id`, and the filter is applied on `package_license.license` (the SPDX identifier column).

  ```rust
  // Pseudocode for the query construction:
  use entity::package_license;

  let mut query = Package::find();

  if let Some(license_param) = license {
      query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
      query = apply_filter(query, &license_param, package_license::Column::License)
          .context("invalid license filter")?;
  }
  ```

- **Preserve existing behavior**: When no `license` parameter is provided, the query runs without the join or filter, returning all packages exactly as before. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests verifying the license filter behavior end-to-end.

**Test cases**:

1. **Single license filter**: Send `GET /api/v2/package?license=MIT`. Assert that only packages with an MIT license are returned. Verify response shape is `PaginatedResults<PackageSummary>`.

2. **Comma-separated multi-value filter**: Send `GET /api/v2/package?license=MIT,Apache-2.0`. Assert that packages matching either MIT or Apache-2.0 are returned. Verify no duplicates if a package has both licenses.

3. **No license filter (regression test)**: Send `GET /api/v2/package` without the `license` parameter. Assert that all packages are returned, matching the pre-change behavior exactly.

4. **Invalid license value**: Send `GET /api/v2/package?license=` (empty value) or a request with malformed license identifiers. Assert that a 400 Bad Request response is returned with an appropriate error message.

**Test setup**: Each test will set up test data in the database including packages with known license associations via the `package_license` join table, then issue HTTP requests to the endpoint and assert on the filtered results.

---

## Changes NOT Made

- **No changes to `common/src/db/query.rs`**: The existing `apply_filter` function already handles comma-separated multi-value parsing and SQL IN clause generation. No modifications or new utility functions are needed.
- **No changes to `entity/src/package_license.rs`**: The existing entity already maps the package-license relationship and provides the SeaORM column and relation definitions needed for the JOIN.
- **No changes to response types**: `PaginatedResults<PackageSummary>` remains untouched. Only the input (query parameters) is extended.
- **No new utility or helper functions**: All parsing and filtering logic is delegated to the existing `apply_filter` function.
