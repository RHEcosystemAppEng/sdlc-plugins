# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint.
The parameter supports both single-value (`?license=MIT`) and comma-separated
multi-value (`?license=MIT,Apache-2.0`) filtering, returning only packages whose
declared SPDX license identifier matches one of the supplied values. The response
shape (`PaginatedResults<PackageSummary>`) remains unchanged.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add `license` query parameter extraction and filtering to the package
list endpoint handler.

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern established in
  `modules/fundamental/src/advisory/endpoints/list.rs` (where the advisory list
  endpoint has a `severity` field on its Query struct), add an `Option<String>` field
  named `license` to the package list endpoint's Query struct. This field captures the
  raw query parameter value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

- **Pass the license filter to the service layer:** In the handler function, extract
  `query.license` and pass it as an argument to `PackageService::list()`. If the
  parameter is `None`, no license filtering is applied (preserving the current behavior
  for requests without the parameter).

- **Validate the license parameter:** If the `license` parameter is present but
  contains invalid values (e.g., empty string, malformed input), return a
  `400 Bad Request` response using the existing `AppError` enum from
  `common/src/error.rs`. Follow the same validation pattern used by the advisory
  endpoint's severity filter.

**Reuse applied:**
- The Query struct pattern (optional filter field) is taken directly from the advisory
  list endpoint (`modules/fundamental/src/advisory/endpoints/list.rs`).
- No new parsing logic is written in this file. The raw comma-separated string is
  passed to the service layer, which delegates to `apply_filter` for parsing.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering logic to the `PackageService::list` method.

**Changes:**

- **Add `license` parameter to the `list` method signature:** Accept an
  `Option<String>` parameter for the license filter value.

- **Apply the filter using `apply_filter`:** When the `license` parameter is `Some`,
  call `common::db::query::apply_filter` to parse the comma-separated string into
  individual values and generate the appropriate SQL `IN` clause. This is the same
  utility used across the codebase for multi-value query parameter handling.
  **Do NOT write new parsing logic** -- `apply_filter` already handles splitting on
  commas and generating the correct filter expression.

- **JOIN through `package_license` entity:** Use the existing SeaORM entity defined in
  `entity/src/package_license.rs` to join the `package` table to the
  `package_license` table. This entity already maps the relationship between packages
  and their licenses. Apply the filter condition on the license identifier column from
  the `package_license` entity. No raw SQL is needed -- use SeaORM's query builder
  with the entity's column definitions.

- **Preserve existing behavior when no filter:** When `license` is `None`, the query
  proceeds without the join or filter, returning all packages as before.

**Reuse applied:**
- `common::db::query::apply_filter` for comma-separated value parsing and SQL IN
  clause generation.
- `entity::package_license` entity for the JOIN, avoiding raw SQL or a new entity
  definition.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests verifying the license filter on the package list endpoint.

**Test cases:**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: Verifies that filtering by a single license returns only packages
     with that license.
   - Given: seed the test database with packages having licenses MIT, Apache-2.0,
     and GPL-3.0.
   - When: `GET /api/v2/package?license=MIT`
   - Then: assert response status is 200; assert all returned items have license
     equal to `"MIT"`; assert specific package names appear in the results (value-based
     assertion, not just length).

2. **`test_list_packages_filter_comma_separated_licenses`**
   - Doc comment: Verifies that comma-separated license values return packages
     matching any of the listed licenses.
   - Given: seed the test database with packages having licenses MIT, Apache-2.0,
     and GPL-3.0.
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert response status is 200; assert returned items have licenses that
     are either `"MIT"` or `"Apache-2.0"`; assert the GPL-3.0 package is not
     included; assert on specific package names.

3. **`test_list_packages_no_license_filter`**
   - Doc comment: Verifies that omitting the license parameter returns all packages
     unchanged (no regression).
   - Given: seed the test database with packages having various licenses.
   - When: `GET /api/v2/package` (no license parameter)
   - Then: assert response status is 200; assert all seeded packages are present in
     the results.

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: Verifies that an invalid license value returns a 400 Bad Request.
   - Given: test database is available.
   - When: `GET /api/v2/package?license=` (empty value) or other invalid input
   - Then: assert response status is 400.

**Conventions followed:**
- Test function naming: `test_<endpoint>_<scenario>` pattern (matching sibling tests
  in `tests/api/`).
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body
  deserialization into `PaginatedResults<PackageSummary>`.
- Each test function has a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Tests hit the real PostgreSQL test database (matching the project's integration test
  approach from `tests/api/advisory.rs` and `tests/api/sbom.rs`).

**Module registration:** The new test file must be registered in `tests/api/` module
structure (e.g., added as a `mod` declaration if the test directory uses `mod.rs`, or
simply present as a file if Cargo discovers it automatically via the `[[test]]` target
in `tests/Cargo.toml`).

---

## Files NOT modified (out of scope)

The following files are relevant but are NOT modified, in compliance with constraint 5.1
(scope to task files):

- `common/src/db/query.rs` -- used as-is; `apply_filter` is called but not modified.
- `entity/src/package_license.rs` -- used as-is for the JOIN; no schema changes needed.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- used as a reference pattern
  only; not modified.
- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration is not
  changed (the existing route handler is modified in place, not replaced).
- `modules/fundamental/src/package/model/summary.rs` -- the `PackageSummary` struct
  already includes a `license` field; no changes needed.

---

## Data-flow trace

```
GET /api/v2/package?license=MIT,Apache-2.0
  -> list.rs: extract Query { license: Some("MIT,Apache-2.0"), ... }
  -> list.rs: validate license parameter (non-empty values)
  -> list.rs: call PackageService::list(..., license=Some("MIT,Apache-2.0"))
  -> service/mod.rs: call apply_filter("MIT,Apache-2.0") -> vec!["MIT", "Apache-2.0"]
  -> service/mod.rs: JOIN package_license entity, WHERE license_id IN ("MIT", "Apache-2.0")
  -> service/mod.rs: execute query, return PaginatedResults<PackageSummary>
  -> list.rs: return 200 OK with JSON body (response shape unchanged)
```

All stages are connected. The data flow is complete from input to output.
