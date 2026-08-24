# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Target Branch

main

## Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 4 -- Understand the Code

Before making any changes, inspect the existing codebase to understand current patterns and confirm the structures referenced in Implementation Notes.

### Code inspection plan

1. **Read `modules/fundamental/src/advisory/endpoints/list.rs`** using `mcp__serena_backend__get_symbols_overview` followed by `mcp__serena_backend__find_symbol` on the query struct and handler function. This is the structural guide for the license filter -- it already implements a `severity` query parameter using the same filtering approach we need. Examine how the Query struct defines the optional filter field, how it extracts the value from query parameters, and how it passes the filter down to the service layer.

2. **Read `common/src/db/query.rs`** using `mcp__serena_backend__find_symbol` on `apply_filter`. This function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. We will reuse `apply_filter` directly -- no new parsing logic needed.

3. **Read `entity/src/package_license.rs`** using `mcp__serena_backend__get_symbols_overview` to understand the package-license join table entity. We will use this existing SeaORM entity for the JOIN query rather than writing raw SQL or creating a new entity.

4. **Read `modules/fundamental/src/package/endpoints/list.rs`** and `modules/fundamental/src/package/service/mod.rs` to understand the current package list endpoint structure and service method signature.

5. **Read `modules/fundamental/src/package/model/summary.rs`** to confirm the PackageSummary struct includes a license field and understand the response shape.

6. **Convention conformance analysis**: Examine sibling files (`modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`) for recurring patterns in naming, error handling, query parameter structs, and filter propagation.

### Conventions discovered

- Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping
- Module structure: `model/ + service/ + endpoints/` pattern per domain module
- Query parameter structs: optional filter fields in a `Query` struct deserialized from query string
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Filter logic: uses `apply_filter` from `common/src/db/query.rs` for multi-value comma-separated parameter parsing
- Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

- Add an optional `license` field to the existing `Query` struct (or create one if it doesn't exist), following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`:
  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing fields ...
      pub license: Option<String>,
  }
  ```
- In the handler function, extract the `license` value from the query parameters and pass it to `PackageService::list()`. Follow the advisory list handler's pattern for how filter values are propagated to the service layer.
- Do NOT write any new parsing logic for comma-separated values -- that is handled by `apply_filter` in the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Changes:**

- Modify the `PackageService::list` method signature to accept an optional `license` filter parameter (e.g., `license: Option<String>`).
- When `license` is `Some(value)`, use `common::db::query::apply_filter` to parse the comma-separated values and generate the appropriate SQL IN clause. Reuse `apply_filter` directly -- it handles both single and multi-value comma-separated parameters.
- Join through the `entity::package_license` table (from `entity/src/package_license.rs`) to filter packages by license. Use the existing SeaORM entity for the JOIN rather than writing raw SQL or creating a new entity.
- When `license` is `None`, skip the filter entirely so the endpoint returns all packages without regression.
- Add validation: if the license parameter value is empty or contains invalid characters, return a 400 Bad Request error using the `AppError` pattern (with `.context()`).

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Changes:**

- Create integration tests following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Tests to include:
  - `test_single_license_filter`: verify `GET /api/v2/package?license=MIT` returns only MIT-licensed packages. Use value-based assertions (`assert_eq!` on specific license identifiers in results) rather than just checking counts.
  - `test_multi_license_filter`: verify `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert on specific package names/licenses in the result set.
  - `test_no_license_filter`: verify `GET /api/v2/package` without the license parameter returns all packages unchanged (no regression).
  - `test_invalid_license_value`: verify that an invalid license value returns 400 Bad Request.
- Each test function will have a doc comment explaining what it verifies.
- Non-trivial tests will use given-when-then section comments.

## Reuse Strategy

This implementation relies heavily on existing code rather than writing new logic:

1. **`common/src/db/query.rs::apply_filter`** -- Reused directly for parsing comma-separated multi-value query parameters and generating SQL IN clauses. No new parsing functions will be created. This is the core reuse that prevents duplication of filtering logic (constraint 5.4).

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Used as the structural template. The advisory severity filter implementation is structurally identical to the license filter needed here. We follow the same Query struct pattern with an optional field, the same handler pattern for extracting and passing filter values, and the same service-layer integration pattern.

3. **`entity/src/package_license.rs`** -- Used for the JOIN query between packages and licenses. This existing SeaORM entity maps the package-license relationship. We use it directly rather than writing raw SQL joins or creating a new entity.

No new utility functions that duplicate `apply_filter` functionality will be created. The `apply_filter` function already handles exactly the use case we need (comma-separated multi-value parsing and SQL IN clause generation).

## Scope Verification

All files in this plan are within the scope defined by the task description:

- **Files to Modify**: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` (matches task exactly)
- **Files to Create**: `tests/api/package_license_filter.rs` (matches task exactly)

No files outside these sections are modified or created.

## Commit Message

```
feat(package): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX identifier filtering.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203
```

With `--trailer='Assisted-by: Claude Code'`.
