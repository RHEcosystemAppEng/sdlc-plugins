# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint that
supports both single-value (`?license=MIT`) and comma-separated multi-value
(`?license=MIT,Apache-2.0`) filtering by SPDX license identifier.

## Target Branch

main

## Dependencies

None.

## Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests. Contains a query
parameter extraction struct and a handler function that calls `PackageService::list`.

**Changes:**

- **Add `license` field to the query parameter struct**: Following the pattern
  established in the advisory list endpoint (`modules/fundamental/src/advisory/endpoints/list.rs`),
  add an `Option<String>` field named `license` to the existing query parameters
  struct (e.g., `PackageListQuery` or equivalent). This mirrors how the advisory
  endpoint has an optional `severity` field in its query struct.

- **Pass the license filter to the service layer**: In the handler function,
  extract the `license` value from the query struct and pass it to
  `PackageService::list()` as an additional parameter. If `license` is `Some`,
  use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated
  string and build the filter. If `None`, no filtering is applied (preserving
  existing behavior).

- **Validation**: Add input validation for the `license` parameter. If the value
  is present but empty or contains invalid characters, return a `400 Bad Request`
  using the project's `AppError` pattern (from `common/src/error.rs`).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries
packages from the database and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add license filter parameter to `list` method signature**: Add an
  `Option<Vec<String>>` parameter (or equivalent) for the parsed license values.

- **Build the filtered query**: When the license filter is provided, join the
  `package` table with the `package_license` entity
  (`entity/src/package_license.rs`) and add a `WHERE license_id IN (...)` clause.
  Use the `apply_filter` function from `common/src/db/query.rs` to generate the
  SQL IN clause from the parsed comma-separated values. This reuses the exact
  same filtering mechanism used by the advisory severity filter.

- **Preserve existing behavior**: When no license filter is provided, the query
  must remain unchanged — no join, no WHERE clause. This ensures backward
  compatibility.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on the package list endpoint.

**Test cases (following conventions from sibling test files like `tests/api/advisory.rs`):**

1. **`test_list_packages_filter_single_license`** — Verify that
   `GET /api/v2/package?license=MIT` returns only packages with MIT license.
   Assert on specific package identifiers in the response, not just count.

2. **`test_list_packages_filter_multiple_licenses`** — Verify that
   `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either
   license. Assert on the actual license values of returned packages.

3. **`test_list_packages_no_license_filter`** — Verify that
   `GET /api/v2/package` (no license param) returns all packages unchanged.
   Compare response against a known baseline to confirm no regression.

4. **`test_list_packages_invalid_license`** — Verify that an invalid license
   value returns `400 Bad Request`. Assert on the status code and error response
   shape.

All tests will:
- Use `assert_eq!(resp.status(), StatusCode::OK)` (or `StatusCode::BAD_REQUEST`)
  pattern per project conventions
- Deserialize response body and assert on `PaginatedResults<PackageSummary>` fields
- Include `///` doc comments explaining what each test verifies
- Include `// Given` / `// When` / `// Then` section comments

**Registration:** The new test file must be registered in `tests/api/` module
(likely via a `mod package_license_filter;` declaration in the test module root
or `Cargo.toml` test configuration).

---

## API Changes

- `GET /api/v2/package` — MODIFY: add optional `license` query parameter
  - `?license=MIT` — filter by single SPDX license identifier (exact match)
  - `?license=MIT,Apache-2.0` — filter by multiple licenses (OR semantics)
  - Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
  - Missing or empty `license` parameter returns all packages (no filter)
  - Invalid license value returns `400 Bad Request`

---

## Implementation Approach

### Query parameter parsing flow

1. Axum extracts `PackageListQuery` from the request query string
2. The `license` field is `Option<String>`
3. If `Some`, pass to `apply_filter` which splits on commas and returns a `Vec<String>`
4. Pass the parsed values to `PackageService::list()`

### Database query construction flow

1. `PackageService::list()` starts with the base package query
2. If license filter values are present:
   - Join `package` to `package_license` on `package.id = package_license.package_id`
   - Add `WHERE package_license.license_id IN (...)` using the values
   - Use `apply_filter` from `common/src/db/query.rs` to construct the IN clause
3. Apply existing pagination and sorting
4. Return `PaginatedResults<PackageSummary>`

### Error handling

- Follow the `Result<T, AppError>` pattern with `.context()` wrapping
- Invalid license values → `AppError` mapped to `400 Bad Request`

### Convention conformance

- **Error handling:** `Result<T, AppError>` with `.context()` (matches all handlers in the project)
- **Naming:** Method and field names follow `verb_noun` / `snake_case` patterns
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Use shared `apply_filter` from `common/src/db/query.rs`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Test assertions:** `assert_eq!(resp.status(), StatusCode::...)` followed by body deserialization

---

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` → Axum extracts query params (input) ✓
  → `apply_filter` parses comma-separated values (processing) ✓
  → `PackageService::list()` builds filtered query with JOIN (processing) ✓
  → SeaORM executes query against PostgreSQL (persistence) ✓
  → `PaginatedResults<PackageSummary>` returned as JSON (output) ✓
  → **COMPLETE**

---

## Scope Containment

Only the files listed in Files to Modify and Files to Create will be touched.
No out-of-scope changes are planned. The response shape is not modified — only
the input query parameter set is extended.

## Documentation Impact

- The API accepts a new query parameter. If `docs/api.md` documents the package
  list endpoint, it should be updated to include the `license` parameter.
- No other documentation changes expected.

## Commit Message

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203
```
