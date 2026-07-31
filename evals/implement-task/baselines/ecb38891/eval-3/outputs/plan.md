# Implementation Plan: TC-9203 -- Add Package License Filter to List Endpoint

## Task Summary

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and
comma-separated multi-value filtering by SPDX license identifier.

## Branch Strategy

- Target Branch: `main`
- Task Branch: `TC-9203`
- Checkout sequence: `git checkout main && git pull && git checkout -b TC-9203`

## Step 4 -- Code Understanding

### Files Inspected Before Modification

Before making any changes, inspect the following existing files to understand current
patterns and confirm the Implementation Notes references:

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Read the severity filter
   implementation to understand the Query struct pattern with optional filter fields and
   how `apply_filter` is invoked. This is the structural template for the license filter.
2. **`common/src/db/query.rs`** -- Read `apply_filter` function signature and behavior to
   understand how it parses comma-separated values and generates SQL IN clauses. This
   function will be reused directly -- no new parsing logic needed.
3. **`entity/src/package_license.rs`** -- Read the package-license join entity to understand
   its column names, relations, and how to construct the JOIN query using SeaORM.
4. **`modules/fundamental/src/package/endpoints/list.rs`** -- Read the current endpoint
   handler to understand the existing Query struct and request processing flow.
5. **`modules/fundamental/src/package/service/mod.rs`** -- Read PackageService::list to
   understand the current query construction and where to insert the license filter.
6. **`modules/fundamental/src/package/model/summary.rs`** -- Read PackageSummary to confirm
   the response shape includes a license field.

### Sibling Convention Analysis

Analyzed sibling modules (advisory, sbom) for conventions:

- **Error handling**: Handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module structure**: Each domain follows `model/ + service/ + endpoints/` pattern
- **Query pattern**: Query structs with optional filter fields, deserialized from query string
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Test patterns**: Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)`
- **Naming**: `verb_noun` pattern for functions, descriptive struct names

### Description Digest Check (Step 1.5)

No digest comment found -- skipping integrity check. This task may have been created
before digest tracking was introduced.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

- Add an optional `license` field (type `Option<String>`) to the existing `Query` struct
  used for deserializing query parameters. Follow the exact same pattern used for the
  `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` value from the deserialized Query struct
  and pass it to `PackageService::list()`.
- Use `common/src/db/query.rs::apply_filter` to process the license parameter. This
  function already handles both single-value (`license=MIT`) and comma-separated
  multi-value (`license=MIT,Apache-2.0`) parsing, plus SQL IN clause generation.
  **Do not write new parsing logic** -- reuse `apply_filter` directly.
- For invalid license values, ensure the existing error handling (which returns 400 via
  `AppError`) is propagated.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Changes:**

- Add a `license` parameter (type `Option<String>`) to the `PackageService::list` method
  signature.
- When a license filter is provided, JOIN through the `package_license` table using
  `entity/src/package_license.rs` entity. Use SeaORM's relation-based join (e.g.,
  `find().join(JoinType::InnerJoin, package_license::Relation::Package.def())`) rather
  than writing raw SQL.
- Apply the filter using `apply_filter` from `common/src/db/query.rs` to handle the
  comma-separated values and generate the appropriate SQL IN clause for
  `package_license.license` column.
- The `PaginatedResults<PackageSummary>` response shape remains unchanged -- only the
  query is filtered, not the output format.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Changes:**

- Create integration tests following the existing test patterns from `tests/api/advisory.rs`
  and `tests/api/sbom.rs`.
- Tests to implement:
  1. **Single license filter**: POST test packages with known licenses, then
     `GET /api/v2/package?license=MIT` and assert only MIT-licensed packages are returned.
     Use value-based assertions (assert on specific package names/license values, not just
     count).
  2. **Multi-value license filter**: `GET /api/v2/package?license=MIT,Apache-2.0` and
     assert packages matching either license are returned. Assert on specific values.
  3. **No filter regression**: `GET /api/v2/package` without license param returns all
     packages unchanged. Compare against known test data.
  4. **Invalid license value**: `GET /api/v2/package?license=` with empty/invalid value
     returns 400 Bad Request.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

## How Existing Code Is Reused

This implementation reuses all three Reuse Candidates from the task description rather
than duplicating any existing logic:

1. **`common/src/db/query.rs::apply_filter`** -- Reused directly for comma-separated
   multi-value query parameter parsing and SQL IN clause generation. No new utility
   function is created for parsing or filtering. The `apply_filter` function already
   handles the exact use case needed (single and multi-value comma-separated parameters).

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Used as the structural
   template. The severity filter pattern (optional field in Query struct, extraction in
   handler, pass-through to service) is followed exactly for the license filter. This
   ensures consistency across endpoints.

3. **`entity/src/package_license.rs`** -- Used for the JOIN query in PackageService::list.
   The existing SeaORM entity provides the relation definitions needed to join packages
   to their licenses without writing raw SQL or creating a new entity.

## Scope Verification

All planned changes are strictly within the task's defined scope:
- **Files to Modify**: `list.rs` (package endpoints) and `mod.rs` (package service) -- both listed
- **Files to Create**: `package_license_filter.rs` (tests) -- listed
- No out-of-scope files are modified or created

## Commit Message

```
feat(package): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX license
identifier. Reuses apply_filter from common/db/query.rs for parameter
parsing and package_license entity for the join query.

Implements TC-9203
```

With flag: `--trailer='Assisted-by: Claude Code'`

## Acceptance Criteria Verification

- [x] GET /api/v2/package?license=MIT returns only MIT-licensed packages -- handled by apply_filter + package_license JOIN
- [x] GET /api/v2/package?license=MIT,Apache-2.0 returns packages matching either -- handled by apply_filter's multi-value support
- [x] GET /api/v2/package without license returns all packages -- optional parameter, no filter applied when absent
- [x] Response shape (PaginatedResults<PackageSummary>) unchanged -- only query modified, not output
- [x] Invalid license values return 400 -- existing AppError handling propagated
