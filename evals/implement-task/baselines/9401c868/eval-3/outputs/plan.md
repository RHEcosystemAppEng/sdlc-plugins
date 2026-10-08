# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages
by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and
comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape
(`PaginatedResults<PackageSummary>`) must remain unchanged.

## Project Configuration Validation

- Repository Registry: `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration: project key TC, Cloud ID present, feature issue type ID present
- Code Intelligence: Serena with `rust-analyzer` available

## Step 4 -- Code Understanding

### Files to inspect before implementation

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate) -- read the
   severity filter to understand the Query struct pattern: how the optional query parameter
   is declared, extracted from Axum's `Query` extractor, and passed to the service layer.
2. **`common/src/db/query.rs`** -- read the `apply_filter` function to understand its
   signature, how it parses comma-separated values, and how it generates `IN` clauses.
3. **`entity/src/package_license.rs`** -- inspect the SeaORM entity to understand the
   table schema (columns, relations) for the package-license join table.
4. **`modules/fundamental/src/package/endpoints/list.rs`** -- read the current list
   endpoint handler to understand its existing Query struct and handler signature.
5. **`modules/fundamental/src/package/service/mod.rs`** -- read the PackageService `list`
   method to understand its current query builder and how to add a JOIN + WHERE clause.
6. **`modules/fundamental/src/package/model/summary.rs`** -- confirm PackageSummary
   includes a `license` field (noted in repo-backend.md).
7. **`modules/fundamental/src/package/endpoints/mod.rs`** -- confirm route registration
   for `GET /api/v2/package`.
8. **`tests/api/advisory.rs`** -- read sibling integration test to understand test
   conventions (setup, assertion patterns, request building).

### Convention conformance analysis

Based on the repository structure and conventions documented in repo-backend.md:

- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Response types**: list endpoints return `PaginatedResults<T>`
- **Query helpers**: shared filtering via `common/src/db/query.rs`
- **Test pattern**: integration tests in `tests/api/`, assert with
  `assert_eq!(resp.status(), StatusCode::OK)`
- **Module pattern**: `model/ + service/ + endpoints/` structure per domain

### CONVENTIONS.md

Check for `CONVENTIONS.md` at the repository root. If present, extract CI check commands
and code generation commands for use in Step 9.

### Documentation files identified

- `docs/api.md` -- REST API reference, may need updating to document the new `license`
  query parameter on `GET /api/v2/package`

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: Contains the handler for `GET /api/v2/package` with a Query struct for
extracting query parameters (likely pagination and sorting params). No license filter exists.

**Changes**:

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named
   `license` to the existing `Query` (or `PackageQuery`, depending on naming) struct used
   by Axum's `Query` extractor. Follow the exact same pattern used by the `severity` field
   in `modules/fundamental/src/advisory/endpoints/list.rs`.

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (pagination, sorting) ...
       /// Optional SPDX license identifier filter. Supports comma-separated values.
       pub license: Option<String>,
   }
   ```

2. **Pass the license parameter to the service layer**: In the handler function, extract
   `query.license` and pass it to `PackageService::list()`. This mirrors how the advisory
   list handler passes `query.severity` to `AdvisoryService::list()`.

3. **Validate the license parameter**: Before passing to the service, validate the license
   value. If the value is present but empty or contains only whitespace/commas, return a
   400 Bad Request via `AppError`. Follow the existing error handling pattern
   (`Result<T, AppError>` with `.context()`).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: Contains `PackageService` with a `list` method that builds a SeaORM
query to fetch packages, applies pagination/sorting, and returns
`PaginatedResults<PackageSummary>`.

**Changes**:

1. **Add `license` parameter to the `list` method signature**: Add `license: Option<String>`
   as a parameter (or extend an existing filter/options struct if one exists).

   ```rust
   pub async fn list(
       &self,
       // ... existing params ...
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter using `apply_filter`**: When `license` is `Some`, use
   `common::db::query::apply_filter` to parse the comma-separated values and generate the
   SQL `IN` clause. This function already handles multi-value parsing -- reuse it directly
   rather than writing custom parsing logic.

3. **Add JOIN to `package_license` table**: Use the `entity::package_license` SeaORM entity
   to join the package table with the package_license table. Apply the filter on the
   license column of the joined table. This follows SeaORM's `join()` / `filter()` pattern.

   ```rust
   if let Some(license) = license {
       // Join package_license entity and apply filter
       query = query
           .join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())
           .filter(apply_filter(entity::package_license::Column::License, &license)?);
   }
   ```

4. **Add `.distinct()` to prevent duplicates**: When joining through the package_license
   table, a package with multiple matching licenses could appear multiple times. Add
   `.distinct()` to the query when the license filter is active.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter on `GET /api/v2/package`.

**Structure** (following sibling test conventions from `tests/api/advisory.rs`):

```rust
/// Integration tests for the license query parameter on GET /api/v2/package.

/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_single_license_filter() {
    // Given: test database seeded with packages having different licenses (MIT, Apache-2.0, GPL-3.0)
    // When: GET /api/v2/package?license=MIT
    // Then: response contains only MIT-licensed packages
    // Assert on specific package names/identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_comma_separated_license_filter() {
    // Given: test database seeded with packages having different licenses
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: response contains packages with MIT or Apache-2.0 licenses
    // Assert on specific package identifiers
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_no_license_filter_returns_all() {
    // Given: test database seeded with packages
    // When: GET /api/v2/package (no license parameter)
    // Then: response contains all packages
    // Assert total count matches expected and verify specific entries
}

/// Verifies that invalid license values return 400 Bad Request.
#[tokio::test]
async fn test_invalid_license_returns_400() {
    // Given: test database available
    // When: GET /api/v2/package?license= (empty value)
    // Then: response status is 400 Bad Request
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

**Test conventions applied**:
- Each test has a `///` doc comment explaining what it verifies
- Non-trivial tests use Given/When/Then section comments
- Value-based assertions on specific package identifiers, not just `.len()` checks
- Uses `assert_eq!(resp.status(), ...)` pattern from sibling tests
- Test database setup follows existing patterns from `tests/api/advisory.rs`

### Module registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test crate root)
  to register the new test module. This is an out-of-scope file modification that would
  need to be flagged in Step 9's scope containment check for user approval.

---

## Files NOT Modified (scope containment)

The following files are explicitly **not** modified:
- `entity/src/package_license.rs` -- used as-is for the JOIN query
- `common/src/db/query.rs` -- `apply_filter` used as-is, no changes needed
- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration unchanged
- `modules/fundamental/src/package/model/summary.rs` -- response shape unchanged
- `server/src/main.rs` -- no route changes

---

## Data-Flow Trace

1. **Input**: HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at Axum
2. **Extraction**: Axum `Query` extractor deserializes into `PackageQuery` struct, populating `license: Some("MIT,Apache-2.0")`
3. **Validation**: Handler validates the license string is non-empty; returns 400 if invalid
4. **Processing**: Handler calls `PackageService::list(..., license: Some("MIT,Apache-2.0"))`
5. **Query building**: Service calls `apply_filter` from `common/src/db/query.rs` which parses `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]` and generates a SeaORM `IN` condition
6. **JOIN**: Service adds `INNER JOIN package_license` and applies the filter condition on the license column, with `.distinct()` to prevent duplicates
7. **Execution**: SeaORM executes the query against PostgreSQL
8. **Response**: Results wrapped in `PaginatedResults<PackageSummary>` and serialized as JSON -- response shape unchanged

All stages connected. No missing or disconnected stages.

---

## Verification Plan (Step 9)

1. **Scope containment**: `git diff --name-only` must show only the two modified files and
   one created file (plus the test module registration if approved)
2. **CI checks**: Run commands from `CONVENTIONS.md` if present, otherwise `cargo check`,
   `cargo fmt --check`, `cargo clippy`
3. **Module-level tests**: `cargo test -p <crate-name>` for each modified crate
4. **Duplication check**: Grep for similar filter patterns to confirm no duplication with
   existing code
5. **Dead parameter detection**: Verify no parameters became unused
6. **Documentation currency**: Update `docs/api.md` if it documents `GET /api/v2/package`
   query parameters
