# Implementation Plan: TC-9203 -- Add Package License Filter to List Endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Repository

trustify-backend

## Target Branch

main

## Branch Name

TC-9203

---

## Step 0 -- Project Configuration Validation

The mock CLAUDE.md contains all required sections:
- **Repository Registry**: present, maps `trustify-backend` to Serena instance `serena_backend`
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present with tool naming convention `mcp__serena_backend__<tool>` and rust-analyzer

Validation passes. Proceed.

## Step 1 -- Task Parsing

Parsed sections from the task description:

| Section | Value |
|---------|-------|
| Repository | trustify-backend |
| Target Branch | main |
| Dependencies | None |
| Target PR | Not present (new PR flow) |
| Bookend Type | Not present (standard implementation flow) |

### Files to Modify
1. `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method

### Files to Create
1. `tests/api/package_license_filter.rs` -- integration tests for the license filter

### API Changes
- `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
- `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values

### Acceptance Criteria
1. `GET /api/v2/package?license=MIT` returns only packages with MIT license
2. `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license
3. `GET /api/v2/package` without license parameter returns all packages (no regression)
4. Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
5. Invalid license values return 400 Bad Request

### Test Requirements
1. Test single license filter returns only matching packages
2. Test comma-separated license filter returns packages matching any listed license
3. Test no license filter returns all packages unchanged
4. Test invalid license value returns 400

---

## Step 2 -- Dependency Verification

No dependencies listed. Proceed.

## Step 4 -- Code Understanding Plan

### Files to Inspect

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to see the current Query struct and handler function
   - Identify the existing query parameter struct (likely a `PackageQuery` or `Query` struct with `#[derive(Deserialize)]`)
   - Find the handler function (likely `list_packages` or similar)

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to see PackageService methods
   - Identify the `list` method signature and how it currently builds queries

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- structural reference)
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` on the advisory query struct and handler
   - Understand how the `severity` filter parameter is defined in the Query struct
   - Understand how the severity filter is passed to the service layer and applied

4. **`common/src/db/query.rs`** (reuse candidate -- direct reuse)
   - Use `mcp__serena_backend__find_symbol` on `apply_filter` to read its full implementation
   - Understand its signature: how it accepts filter values and generates SQL IN clauses
   - Confirm it handles comma-separated parsing

5. **`entity/src/package_license.rs`** (reuse candidate -- entity for JOIN)
   - Use `mcp__serena_backend__get_symbols_overview` to understand the entity structure
   - Identify the SeaORM entity fields (likely `package_id` and `license` columns)
   - Understand the relation definitions for joining with the `package` entity

6. **`modules/fundamental/src/package/model/summary.rs`** (context)
   - Confirm PackageSummary struct includes a `license` field
   - Understand the response shape that must remain unchanged

7. **`modules/fundamental/src/package/endpoints/mod.rs`** (context)
   - Understand route registration to ensure no changes needed there

### Sibling/Convention Analysis

- **Advisory list endpoint** (`modules/fundamental/src/advisory/endpoints/list.rs`) serves as the primary sibling for endpoint pattern analysis
- **Advisory service** (`modules/fundamental/src/advisory/service/advisory.rs`) serves as the sibling for service-layer filtering pattern
- **Existing test files** (`tests/api/advisory.rs`, `tests/api/sbom.rs`) serve as siblings for test convention analysis

### Conventions to Follow (from repo Key Conventions)
- Framework: Axum for HTTP, SeaORM for database
- Module pattern: model/ + service/ + endpoints/
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Response types: list endpoints return `PaginatedResults<T>`
- Query helpers: shared filtering via `common/src/db/query.rs`
- Testing: integration tests in `tests/api/`, hit real PostgreSQL, use `assert_eq!(resp.status(), StatusCode::OK)` pattern

### CONVENTIONS.md Lookup
- Check for `CONVENTIONS.md` at repo root (listed in directory tree)
- Extract CI check commands if present
- Extract code generation commands if present

### Documentation Files Identified
- `README.md` at repo root
- `docs/api.md` -- REST API reference (may need license parameter documented)
- `CONVENTIONS.md` at repo root

---

## Step 5 -- Branch Creation

```
git checkout main
git pull
git checkout -b TC-9203
```

---

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Current state (expected):** Contains a query parameter struct (e.g., `PackageQuery`) and a handler function for `GET /api/v2/package`. The struct likely has optional fields for pagination and sorting but no license filter.

**Changes:**

1. **Add `license` field to the query parameter struct:**
   ```rust
   /// Optional license filter. Supports single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```
   This follows the same pattern as the `severity` field in the advisory endpoint's query struct.

2. **Add license filter application in the handler function:**
   - After extracting query parameters, check if `license` is `Some`
   - Call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value and generate the SQL filter condition
   - Pass the parsed filter values to the service layer's list method

3. **Add validation for invalid license values:**
   - Validate that license values are non-empty strings after splitting
   - Return `AppError` (400 Bad Request) for invalid values using `.context()` error wrapping

4. **Import additions:**
   - Import `apply_filter` from `common::db::query`
   - Import `package_license` entity from `entity::package_license`

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Current state (expected):** Contains `PackageService` with a `list` method that queries packages from the database using SeaORM and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` parameter to the `list` method signature:**
   ```rust
   /// Lists packages, optionally filtered by license SPDX identifiers.
   pub async fn list(
       &self,
       // ... existing params (pagination, sorting, etc.)
       license_filter: Option<Vec<String>>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Add JOIN and WHERE clause for license filtering:**
   - When `license_filter` is `Some` and non-empty, join the `package_license` entity table
   - Use SeaORM's `JoinType::InnerJoin` on `package_license::Entity` relating `package.id = package_license.package_id`
   - Apply a `WHERE package_license.license IN (...)` condition using the parsed filter values
   - Add `.distinct()` to the query to avoid duplicate packages when a package has multiple matching licenses

3. **Preserve existing behavior:**
   - When `license_filter` is `None`, no JOIN or WHERE is added -- query returns all packages as before
   - The return type `PaginatedResults<PackageSummary>` remains unchanged

### File 3 (new): `tests/api/package_license_filter.rs`

**Create integration tests following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:**

1. **Test module setup:**
   - Import test utilities, HTTP client, status codes
   - Set up test database with known package-license data

2. **Test functions:**

   ```rust
   /// Verifies that filtering by a single license returns only packages with that license.
   #[tokio::test]
   async fn test_single_license_filter() {
       // Given packages with MIT, Apache-2.0, and GPL-3.0 licenses in the database
       // When requesting GET /api/v2/package?license=MIT
       // Then only MIT-licensed packages are returned
       // Assert on specific package names/IDs, not just count
   }

   /// Verifies that comma-separated license filter returns packages matching any listed license.
   #[tokio::test]
   async fn test_multi_license_filter() {
       // Given packages with MIT, Apache-2.0, and GPL-3.0 licenses
       // When requesting GET /api/v2/package?license=MIT,Apache-2.0
       // Then packages with MIT or Apache-2.0 licenses are returned
       // Assert on specific package identifiers
   }

   /// Verifies that omitting the license parameter returns all packages unchanged.
   #[tokio::test]
   async fn test_no_license_filter_returns_all() {
       // Given packages with various licenses
       // When requesting GET /api/v2/package (no license param)
       // Then all packages are returned
       // Assert count and specific values match expected full set
   }

   /// Verifies that an invalid license value returns 400 Bad Request.
   #[tokio::test]
   async fn test_invalid_license_returns_400() {
       // Given the API endpoint
       // When requesting GET /api/v2/package?license= (empty value)
       // Then the response status is 400 Bad Request
   }
   ```

3. **Test registration:**
   - Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness root) if test modules are registered explicitly

### Additional Integration Points

- **`tests/Cargo.toml`**: may need to be updated if the new test file requires additional test dependencies (unlikely if following existing test patterns)
- **`modules/fundamental/src/package/endpoints/mod.rs`**: no changes needed -- the existing route registration for `GET /api/v2/package` already points to `list.rs`, and we are modifying the existing handler, not adding a new route

---

## Step 7 -- Test Execution

Run:
```
cargo test -p trustify-tests  # or whatever crate contains tests/api/
cargo test -p trustify-fundamental  # for unit tests in the service module
```

---

## Step 8 -- Acceptance Criteria Verification

Each criterion maps to implementation and tests:

| Criterion | Verified By |
|-----------|-------------|
| Single license filter works | `test_single_license_filter` + endpoint handler + service filter |
| Multi-value filter works | `test_multi_license_filter` + `apply_filter` comma parsing |
| No filter returns all | `test_no_license_filter_returns_all` + `None` branch in service |
| Response shape unchanged | Return type is still `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | `test_invalid_license_returns_400` + validation in handler |

---

## Step 9 -- Self-Verification Checklist

1. **Scope containment**: only `list.rs`, `service/mod.rs`, and `package_license_filter.rs` are modified/created -- matches task spec
2. **Sensitive-pattern check**: no secrets or env files in changes
3. **Dead parameter detection**: no parameters removed
4. **Duplication check**: reusing `apply_filter` instead of writing new filter parsing logic
5. **Documentation currency**: `docs/api.md` may need a note about the new `license` query parameter
6. **Data-flow trace**: Request `?license=MIT` -> handler extracts from query struct -> `apply_filter` parses comma-separated values -> service receives `Vec<String>` -> SeaORM JOIN + WHERE on `package_license` table -> filtered `PaginatedResults<PackageSummary>` returned
7. **Contract & sibling parity**: follows same pattern as advisory severity filter; `Result<T, AppError>` return type maintained; `.context()` error wrapping used

---

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value filtering by
SPDX license identifier. Reuses the existing apply_filter helper from
common/src/db/query.rs and joins through the package_license entity.

Implements TC-9203"
```

Then:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

---

## Step 11 -- Jira Update

1. Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
2. Add comment with PR link and summary of changes
3. Transition TC-9203 to In Review
