# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages
by their declared SPDX license identifier. Supports both single-value (`?license=MIT`)
and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering via exact match.

## Project Configuration Validation (Step 0)

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with rust-analyzer

Configuration is valid; proceed with implementation.

## Task Parsing (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none (standard implementation task)
- **Target PR**: none (new PR flow)
- **Dependencies**: none

## Code Understanding (Step 4)

### Files to inspect before implementation

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- The advisory list endpoint
   already implements a `severity` query parameter filter. This is the structural template
   for the license filter. Inspect the `Query` struct to see how the optional filter field
   is declared, how it is extracted from query parameters, and how it is passed to the
   service layer.

2. **`common/src/db/query.rs`** -- Contains `apply_filter`, the shared utility for building
   SQL filter clauses from comma-separated query parameter values. Understand its signature,
   how it generates `IN` clauses, and what types it expects.

3. **`entity/src/package_license.rs`** -- The SeaORM entity for the package-license join
   table. Identify the column names (likely `package_id` and `license`) for the JOIN query.

4. **`modules/fundamental/src/package/endpoints/list.rs`** -- The current package list
   endpoint. Understand its existing `Query` struct fields, how it calls `PackageService`,
   and where the new `license` field should be added.

5. **`modules/fundamental/src/package/service/mod.rs`** -- The `PackageService::list` method.
   Understand how it builds the database query, what parameters it accepts, and where the
   license filter JOIN and WHERE clause should be inserted.

6. **`modules/fundamental/src/package/model/summary.rs`** -- The `PackageSummary` struct.
   Confirm it includes a `license` field (per the repo description) so the filter can
   meaningfully target it.

7. **`tests/api/advisory.rs`** -- Sibling test file for advisory endpoint integration tests.
   Study the test patterns: setup, request building, assertion style, error case coverage.

### Convention conformance analysis

Based on the repository conventions documented in `repo-backend.md`:

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping.
  The license filter must follow this pattern.
- **Naming**: Rust `snake_case` for functions and variables. Query struct fields match
  query parameter names.
- **Response types**: List endpoints return `PaginatedResults<T>` from
  `common/src/model/paginated.rs`. The response type must not change.
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern. Value-based
  assertions on response body content per skill guidance.
- **Module pattern**: `model/ + service/ + endpoints/` structure per domain module.

### CONVENTIONS.md lookup

The repository has a `CONVENTIONS.md` at root. Would read it for CI check commands and
code generation commands. Extract verification commands for Step 9 CI checks.

### Documentation files

- `docs/api.md` -- REST API reference; will need updating to document the new `license`
  query parameter.
- `README.md` -- General project docs; unlikely to need changes for a filter addition.

## Branch Creation (Step 5)

```
git checkout main
git pull
git checkout -b TC-9203
```

## Implementation Changes (Step 6)

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the `Query` struct**: Add an `Option<String>` field named
   `license` to the existing query parameter struct, following the same pattern as the
   advisory endpoint's `severity` field.

   ```rust
   /// Query parameters for package list endpoint.
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, search) ...
       /// Optional license filter. Supports comma-separated SPDX identifiers.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer**: In the handler function, extract
   `query.license` and pass it to `PackageService::list()`. Follow the same pattern
   as the advisory endpoint passes its severity filter.

   ```rust
   let result = service
       .list(
           // ... existing parameters ...
           query.license.as_deref(),
       )
       .await
       .context("Failed to list packages")?;
   ```

3. **Add license validation**: Before passing to the service, validate the license
   parameter if present. If the value is empty or contains invalid characters, return
   a 400 Bad Request via `AppError`. Follow existing validation patterns.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add `license` parameter to `PackageService::list`**: Add an `Option<&str>` parameter
   for the license filter.

   ```rust
   /// List packages with optional filtering by license.
   pub async fn list(
       &self,
       // ... existing parameters ...
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter using `apply_filter`**: When `license` is `Some`, use
   the shared `apply_filter` function from `common/src/db/query.rs` to parse the
   comma-separated values and generate an SQL `IN` clause. Join through the
   `package_license` entity table.

   ```rust
   use common::db::query::apply_filter;
   use entity::package_license;

   // Inside the list method, after building the base query:
   if let Some(license_filter) = license {
       let license_values = apply_filter(license_filter);
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(package_license::Column::License.is_in(license_values));
   }
   ```

3. **Ensure no regression when filter is absent**: When `license` is `None`, the query
   remains unchanged -- no JOIN is added, no WHERE clause is applied. All packages are
   returned as before.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create an integration test file following the patterns in `tests/api/advisory.rs`:

```rust
//! Integration tests for the package license filter (`GET /api/v2/package?license=...`).

/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_single_license_filter() {
    // Given a database with packages having MIT and Apache-2.0 licenses
    let app = test_app().await;
    seed_packages_with_licenses(&app, &[
        ("pkg-a", "MIT"),
        ("pkg-b", "Apache-2.0"),
        ("pkg-c", "MIT"),
    ]).await;

    // When requesting packages filtered by MIT
    let resp = app.get("/api/v2/package?license=MIT").await;

    // Then only MIT-licensed packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert!(body.items.iter().all(|p| p.license == "MIT"));
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_comma_separated_license_filter() {
    // Given a database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    let app = test_app().await;
    seed_packages_with_licenses(&app, &[
        ("pkg-a", "MIT"),
        ("pkg-b", "Apache-2.0"),
        ("pkg-c", "GPL-3.0-only"),
    ]).await;

    // When requesting packages filtered by MIT and Apache-2.0
    let resp = app.get("/api/v2/package?license=MIT,Apache-2.0").await;

    // Then packages with either license are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    let licenses: Vec<&str> = body.items.iter().map(|p| p.license.as_str()).collect();
    assert!(licenses.contains(&"MIT"));
    assert!(licenses.contains(&"Apache-2.0"));
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_no_license_filter_returns_all() {
    // Given a database with packages having various licenses
    let app = test_app().await;
    seed_packages_with_licenses(&app, &[
        ("pkg-a", "MIT"),
        ("pkg-b", "Apache-2.0"),
        ("pkg-c", "GPL-3.0-only"),
    ]).await;

    // When requesting packages without a license filter
    let resp = app.get("/api/v2/package").await;

    // Then all packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 3);
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_invalid_license_returns_400() {
    // Given a running test app
    let app = test_app().await;

    // When requesting packages with an empty license filter
    let resp = app.get("/api/v2/package?license=").await;

    // Then a 400 Bad Request is returned
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

The test file also needs to be registered in `tests/api/mod.rs` (if one exists) or in
the test crate's `Cargo.toml`. This would be flagged as an out-of-scope file in Step 9's
scope containment check, since `tests/api/mod.rs` is not listed in Files to Modify.

### Documentation impact

- **`docs/api.md`**: Add documentation for the new `license` query parameter on the
  `GET /api/v2/package` endpoint. Document the supported format (single value, comma-
  separated), the matching behavior (exact match on SPDX identifier), and the 400
  response for invalid values. This would be flagged as out-of-scope since it is not in
  Files to Modify.

## Verification (Step 9)

### Scope containment
- `modules/fundamental/src/package/endpoints/list.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/package/service/mod.rs` -- in scope (Files to Modify)
- `tests/api/package_license_filter.rs` -- in scope (Files to Create)
- Any other modified files (e.g., `tests/api/mod.rs` for test registration) would be
  flagged as out-of-scope for user approval.

### Data-flow trace
1. **Input**: HTTP GET request with `?license=MIT` query parameter
2. **Extraction**: Axum deserializes query params into `Query` struct, `license` field populated
3. **Validation**: Handler validates the license parameter (non-empty, valid characters)
4. **Service call**: Handler passes `license` to `PackageService::list()`
5. **Query building**: Service uses `apply_filter` to parse comma-separated values, JOINs
   `package_license` table, adds `WHERE license IN (...)` clause
6. **Database execution**: SeaORM executes the filtered query against PostgreSQL
7. **Response**: Results wrapped in `PaginatedResults<PackageSummary>`, serialized as JSON
8. **Output**: HTTP 200 with filtered package list (unchanged response shape)

Flow is complete -- every stage connects to the next.

### Contract and sibling parity
- **Contract**: `PackageService::list` returns `Result<PaginatedResults<PackageSummary>, AppError>`,
  unchanged by the addition of the filter parameter.
- **Sibling parity**: Advisory list endpoint's severity filter follows the same pattern
  (optional query param -> service param -> apply_filter -> JOIN + WHERE). The license
  filter mirrors this structure exactly.
- **Cross-module entity**: The `package_license` entity is read-only in this context (no
  writes), so transaction/conflict handling is not a concern.

### Duplication check
- The `apply_filter` function in `common/src/db/query.rs` already handles comma-separated
  parsing and IN clause generation. No duplication introduced -- we reuse it directly.
- No new utility functions are created that overlap with existing code.

### CI checks
- Run commands from `CONVENTIONS.md` (formatting, linting, clippy, compilation)
- Run `cargo test -p trustify-fundamental` (or the correct crate name from `cargo metadata`)
  for the module containing modified files
- Run integration tests in the `tests/` crate

## Commit and PR (Step 10)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to list endpoint

Add optional `license` query parameter to GET /api/v2/package that filters
packages by their declared SPDX license identifier. Supports single-value
and comma-separated multi-value filtering using the existing apply_filter
utility and package_license entity join.

Implements TC-9203"
```

PR created with `--base main`, description includes:
- `Implements [TC-9203](<jira-web-url>)`
- Summary of changes
- Test plan referencing the four integration tests

## Jira Update (Step 11)

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link and summary of changes
- Transition TC-9203 to In Review
