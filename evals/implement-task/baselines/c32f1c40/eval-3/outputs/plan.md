# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint to allow filtering packages by their declared SPDX license identifier. Support both single-value and comma-separated multi-value filtering (exact match).

## Step 0 -- Validate Project Configuration

Project Configuration verified in `claude-md-mock.md`:
- Repository Registry: present (trustify-backend, serena_backend, path `./`)
- Jira Configuration: present (Project key: TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (serena_backend with rust-analyzer)

All required sections are present. Proceed.

## Step 1 -- Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add `license` query parameter to `GET /api/v2/package` list endpoint. Support single-value and comma-separated multi-value filtering on SPDX identifiers.
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
  - `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method
- **Files to Create**:
  - `tests/api/package_license_filter.rs` -- integration tests for the license filter
- **API Changes**:
  - `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
  - `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values
- **Reuse Candidates**: 3 items (see reuse-analysis.md)
- **Acceptance Criteria**: 5 items (single filter, multi filter, no-filter regression, response shape unchanged, 400 on invalid)
- **Test Requirements**: 4 items
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

## Step 4 -- Understand the Code (planned investigation)

### 4.1 Files to Modify -- inspect current state

1. **`modules/fundamental/src/package/endpoints/list.rs`**
   - Use `mcp__serena_backend__get_symbols_overview` to understand the current endpoint handler structure
   - Identify the existing `Query` struct (or equivalent) used for query parameter extraction
   - Identify where the handler calls into `PackageService`

2. **`modules/fundamental/src/package/service/mod.rs`**
   - Use `mcp__serena_backend__get_symbols_overview` to see `PackageService` struct and its `list` method signature
   - Understand how the current list query is built (SeaORM query builder calls)
   - Identify where filtering is applied (if any existing filters exist)

### 4.2 Reuse candidates -- verify patterns exist

3. **`common/src/db/query.rs`**
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the `apply_filter` function
   - Confirm it handles comma-separated multi-value parsing and SQL IN clause generation
   - Understand its signature and how to call it from the package service

4. **`modules/fundamental/src/advisory/endpoints/list.rs`**
   - Use `mcp__serena_backend__get_symbols_overview` to see the advisory list endpoint structure
   - Use `mcp__serena_backend__find_symbol` on the Query struct to see how the `severity` field is declared
   - This is the structural template for the license filter implementation

5. **`entity/src/package_license.rs`**
   - Use `mcp__serena_backend__get_symbols_overview` to see the entity definition
   - Understand the columns (package_id, license) and relationships
   - Confirm SeaORM entity structure for JOIN usage

### 4.3 Sibling analysis -- convention conformance

6. **Advisory list endpoint** (`modules/fundamental/src/advisory/endpoints/list.rs`) -- already covered above as reuse candidate; also serves as the sibling for convention conformance
7. **SBOM list endpoint** (`modules/fundamental/src/sbom/endpoints/list.rs`) -- use `get_symbols_overview` for a second sibling comparison
8. **Existing integration tests** (`tests/api/advisory.rs`, `tests/api/sbom.rs`) -- inspect test patterns for assertion style, setup, naming

### 4.4 CONVENTIONS.md lookup

9. Check for `CONVENTIONS.md` at repository root. If present, read it for:
   - CI check commands to run in Step 9
   - Code generation commands
   - Naming and structure conventions

### 4.5 Documentation files

10. Identify docs:
    - `docs/api.md` -- REST API reference, may need updating for new query parameter
    - `README.md` -- unlikely to need changes
    - `docs/architecture.md` -- unlikely to need changes

### 4.6 Expected conventions (based on repo structure and task description)

- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Response types**: `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: `common/src/db/query.rs` for filtering/pagination/sorting
- **Naming**: Rust standard snake_case for functions and variables
- **Test pattern**: `assert_eq!(resp.status(), StatusCode::OK)`, real PostgreSQL test database

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the `Query` struct** (or equivalent query parameter struct):
   - Add `pub license: Option<String>` field
   - Follow the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`
   - Add appropriate serde deserialization attributes to match sibling query structs

2. **Pass the license parameter to the service layer**:
   - In the handler function, extract `query.license` and pass it to `PackageService::list()`
   - Follow the same parameter-passing pattern used in the advisory list handler

**Reuse**: The Query struct pattern is reused directly from the advisory endpoint's Query struct. No new abstraction needed -- just add the field.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Update the `list` method signature** to accept an optional license filter parameter:
   - Add `license: Option<String>` parameter (or equivalent, matching how advisory service receives `severity`)

2. **Implement the license filter logic**:
   - When `license` is `Some(value)`:
     a. Call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value into individual license identifiers
     b. JOIN with the `package_license` entity (`entity/src/package_license.rs`) to access the license column
     c. Apply an `IN` clause filter using the parsed values
   - When `license` is `None`: no additional filtering (existing behavior preserved)

3. **Add validation**:
   - Validate license values are non-empty strings
   - Return `AppError` (400 Bad Request) for invalid/empty license values
   - Use `.context()` wrapping for error handling per project conventions

**Reuse**:
- `apply_filter` from `common/src/db/query.rs` -- handles comma-separated parsing and IN clause generation
- `entity::package_license` -- used for the JOIN, no raw SQL needed
- Advisory service filter pattern -- structural template for how to integrate `apply_filter` into the query builder

### File 3: `tests/api/package_license_filter.rs` (NEW)

**Changes:**

1. **Create integration test file** following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`

2. **Test functions to implement**:

   ```rust
   /// Verifies that filtering by a single license returns only packages with that license.
   #[tokio::test]
   async fn test_single_license_filter() {
       // Given: packages with MIT and Apache-2.0 licenses exist in the test database
       // When: GET /api/v2/package?license=MIT
       // Then: only MIT-licensed packages are returned
       // Assert on specific package identifiers, not just count
   }

   /// Verifies that comma-separated license filter returns packages matching any listed license.
   #[tokio::test]
   async fn test_comma_separated_license_filter() {
       // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
       // When: GET /api/v2/package?license=MIT,Apache-2.0
       // Then: packages with MIT or Apache-2.0 are returned, but not GPL-3.0
       // Assert on specific package identifiers
   }

   /// Verifies that omitting the license parameter returns all packages unchanged.
   #[tokio::test]
   async fn test_no_license_filter_returns_all() {
       // Given: packages with various licenses exist
       // When: GET /api/v2/package (no license parameter)
       // Then: all packages are returned (same behavior as before the feature)
       // Assert on specific package identifiers to confirm no regression
   }

   /// Verifies that an invalid license value returns 400 Bad Request.
   #[tokio::test]
   async fn test_invalid_license_returns_400() {
       // Given: the endpoint is available
       // When: GET /api/v2/package?license= (empty value)
       // Then: response status is 400 Bad Request
   }
   ```

3. **Register the test module**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the appropriate test harness entry point). This is an out-of-scope file change that would be flagged in Step 9 for user approval.

**Conventions applied**:
- Doc comments on every test function
- Given/When/Then section comments inside test bodies
- Value-based assertions (assert on specific package identifiers, not just counts)
- `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Real PostgreSQL test database (per project conventions)

### Documentation impact

- **`docs/api.md`**: Update to document the new `license` query parameter on `GET /api/v2/package`. Add parameter description, type (string), optionality (optional), and examples showing single and multi-value usage. This is an out-of-scope file that would be flagged in Step 9 for user approval.

## Step 8 -- Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| GET /api/v2/package?license=MIT returns only MIT packages | `test_single_license_filter` |
| GET /api/v2/package?license=MIT,Apache-2.0 returns either | `test_comma_separated_license_filter` |
| No license param returns all packages (no regression) | `test_no_license_filter_returns_all` |
| Response shape (PaginatedResults<PackageSummary>) unchanged | All tests verify response deserializes to PaginatedResults<PackageSummary> |
| Invalid license values return 400 | `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification Checklist

1. **Scope containment**: `git diff --name-only` should show only:
   - `modules/fundamental/src/package/endpoints/list.rs` (modified)
   - `modules/fundamental/src/package/service/mod.rs` (modified)
   - `tests/api/package_license_filter.rs` (created)
   - Potentially `tests/api/mod.rs` (out-of-scope -- flag for user approval)
   - Potentially `docs/api.md` (out-of-scope -- flag for user approval)

2. **Sensitive-pattern check**: scan staged diff for secrets/credentials

3. **Duplication check**: search for existing license filter logic elsewhere in the codebase

4. **Dead parameter detection**: verify no unused parameters after changes

5. **CI checks**: run CONVENTIONS.md CI commands if present; otherwise run `cargo check`, `cargo fmt --check`, `cargo clippy`

6. **Module-level tests**: run `cargo test -p fundamental` (or appropriate crate name from `cargo metadata`)

7. **Data-flow trace**:
   - Input: HTTP query parameter `license` extracted by Axum from request URL
   - Processing: parsed by Query struct deserialization, passed to PackageService, `apply_filter` parses comma-separated values, SeaORM builds JOIN + IN clause query
   - Output: filtered packages returned as `PaginatedResults<PackageSummary>` (unchanged response shape)
   - All stages connected -- complete data flow

8. **Contract and sibling parity**:
   - Contract: handler returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>` -- unchanged
   - Sibling parity: license filter follows same pattern as advisory severity filter
   - Cross-module entity: `package_license` entity used read-only, no write conflicts
   - Caller-site: no new shared abstractions introduced

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that filters
packages by SPDX license identifier. Supports single-value and comma-separated
multi-value filtering using the existing apply_filter helper from common/db/query.rs.

Reuses the advisory severity filter pattern for structural consistency.
Joins through the package_license entity for license matching.

Implements TC-9203"
```

Then:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment summarizing changes and linking to PR
- Transition TC-9203 to In Review
