# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Pre-Implementation Steps

### Step 0 - Validate Project Configuration

The project CLAUDE.md contains the required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: `serena_backend` configured with rust-analyzer

### Step 1 - Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new PR flow)

### Step 4 - Code Understanding

Use `mcp__serena_backend__get_symbols_overview` on the following files to understand current structure:
1. `modules/fundamental/src/package/endpoints/list.rs` - current package list endpoint
2. `modules/fundamental/src/package/service/mod.rs` - current PackageService
3. `modules/fundamental/src/advisory/endpoints/list.rs` - reference implementation for severity filter (reuse candidate)
4. `common/src/db/query.rs` - shared query helpers including `apply_filter` (reuse candidate)
5. `entity/src/package_license.rs` - package-license entity for JOIN

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:
- `apply_filter` in `common/src/db/query.rs` to understand its interface for comma-separated multi-value filtering
- The Query struct in `modules/fundamental/src/advisory/endpoints/list.rs` to see how `severity` is defined as an optional filter field
- The list handler function in `modules/fundamental/src/advisory/endpoints/list.rs` to see how the severity filter is wired through

Use `mcp__serena_backend__find_referencing_symbols` on:
- `PackageService::list` to identify all callers before modifying its signature
- The package list endpoint's query struct to see if anything else depends on its shape

Convention conformance analysis - inspect sibling files:
- `modules/fundamental/src/advisory/endpoints/list.rs` (sibling list endpoint)
- `modules/fundamental/src/sbom/endpoints/list.rs` (sibling list endpoint)
- `modules/fundamental/src/advisory/service/advisory.rs` (sibling service)

Test convention analysis - inspect sibling test files:
- `tests/api/advisory.rs` (sibling endpoint tests)
- `tests/api/sbom.rs` (sibling endpoint tests)

Documentation identification:
- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/api.md` (API reference)

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: Contains the `GET /api/v2/package` handler with a Query struct for extraction of query parameters (pagination, sorting) but no license filter.

**Changes**:

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing Query struct used for query parameter extraction, following the same pattern as the advisory endpoint's `severity` field.

   ```rust
   /// Optional license filter. Supports single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Pass `license` to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter.

3. **Add validation**: Before passing to the service, validate that if `license` is provided, it is non-empty. Return `400 Bad Request` via `AppError` for invalid/empty license values, following the existing error handling pattern (`Result<T, AppError>` with `.context()` wrapping).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: Contains `PackageService` with a `list` method that queries packages with pagination/sorting but no license filtering.

**Changes**:

1. **Add `license` parameter to the `list` method signature**: Add `license: Option<String>` as a parameter to the existing `list` method.

2. **Build license filter using `apply_filter`**: When `license` is `Some`, use the `apply_filter` function from `common/src/db/query.rs` to handle comma-separated values and generate the appropriate SQL IN clause.

3. **Add JOIN to `package_license` entity**: When the license filter is active, join the query through the `package_license` table (from `entity/src/package_license.rs`) to filter packages by their declared license. Use SeaORM's relation-based join rather than raw SQL.

4. **Preserve existing behavior**: When `license` is `None`, the query remains unchanged - no JOIN is added, all packages are returned.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter on the package list endpoint.

**Test functions** (following sibling test patterns from `tests/api/advisory.rs`):

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only matching packages.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200, response body contains only packages with MIT license, assert on specific package names/identifiers (value-based assertions, not just count)

2. **`test_list_packages_filter_comma_separated_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200, response body contains packages with MIT OR Apache-2.0 licenses, does not contain GPL-3.0 packages, assert on specific values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged (no regression).`
   - Given: Test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200, response body contains all seeded packages, response shape is `PaginatedResults<PackageSummary>`, assert on total count and specific items

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: No special setup needed
   - When: `GET /api/v2/package?license=` (empty license value)
   - Then: Response status is 400 Bad Request

**Integration with test infrastructure**:
- Register the new test file in `tests/Cargo.toml` if needed (check sibling test registration pattern)
- Use the same test database setup/teardown as `tests/api/advisory.rs`
- Follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern from sibling tests
- Include given-when-then section comments in each non-trivial test

---

## Files NOT Modified (confirming scope)

- `modules/fundamental/src/package/endpoints/mod.rs` - Route registration should not need changes since the route `/api/v2/package` already exists; only the handler's query extraction changes
- `modules/fundamental/src/package/model/summary.rs` - `PackageSummary` struct is NOT changed; the response shape remains identical
- `entity/src/package_license.rs` - Used as-is for the JOIN; no modifications needed
- `common/src/db/query.rs` - `apply_filter` is reused directly; no modifications needed
- `server/src/main.rs` - No new routes to mount

---

## Implementation Sequence

1. Modify `modules/fundamental/src/package/service/mod.rs` (service layer first - add filtering logic)
2. Modify `modules/fundamental/src/package/endpoints/list.rs` (endpoint layer - wire up query parameter)
3. Create `tests/api/package_license_filter.rs` (integration tests)
4. Run `cargo test` to verify all tests pass
5. Run CI checks from `CONVENTIONS.md` if present
6. Verify acceptance criteria
7. Self-verification (scope containment, sensitive-pattern check, data-flow trace)

---

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` -> Axum extracts Query struct with `license: Some("MIT")` -> handler validates non-empty -> passes to `PackageService::list(license: Some("MIT"))` -> service calls `apply_filter("MIT")` which parses comma-separated values -> SeaORM query joins `package_license` table and adds `WHERE license IN ('MIT')` -> returns `PaginatedResults<PackageSummary>` -> Axum serializes response -- **COMPLETE**

## Commit Strategy

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Uses existing apply_filter helper and package_license entity join.

Implements TC-9203
```

With `--trailer="Assisted-by: Claude Code"`.

PR created against `main` branch with description referencing `TC-9203` Jira URL.
