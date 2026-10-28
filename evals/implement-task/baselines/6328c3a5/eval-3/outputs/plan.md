# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages
by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and
comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering via exact match. The
response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md (`claude-md-mock.md`) contains all required sections:
- Repository Registry with `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration with Project key, Cloud ID, Feature issue type ID
- Code Intelligence section with tool naming convention and `serena_backend` instance

Validation passes. Proceed.

## Step 1 -- Parse Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None
- **Files to Modify**: 2 files
- **Files to Create**: 1 file
- **API Changes**: Modify `GET /api/v2/package` to accept optional `license` query parameter

## Step 4 -- Understand the Code (planned investigation)

### Files to inspect via Serena (`serena_backend`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** -- `get_symbols_overview` to see
   the current handler, query struct, and route registration. Then `find_symbol` with
   `include_body=true` on the handler function and the Query struct to understand parameter
   extraction.

2. **`modules/fundamental/src/package/service/mod.rs`** -- `get_symbols_overview` to see the
   `PackageService` struct and its `list` method signature. `find_symbol` on the `list` method
   to understand how it builds the database query.

3. **`common/src/db/query.rs`** -- `find_symbol` on `apply_filter` to read its signature,
   understand how it parses comma-separated values, and how it generates SQL `IN` clauses.

4. **`modules/fundamental/src/advisory/endpoints/list.rs`** (sibling reference) --
   `get_symbols_overview` to see the severity filter pattern: the Query struct with its
   optional `severity` field, how it is extracted from the request, and how it is passed
   to the service layer.

5. **`entity/src/package_license.rs`** -- `get_symbols_overview` to see the SeaORM entity
   definition, its columns, and its relation to the `package` entity.

6. **`modules/fundamental/src/package/model/summary.rs`** -- confirm `PackageSummary`
   includes a `license` field (as stated in repo structure).

7. **`common/src/model/paginated.rs`** -- confirm `PaginatedResults<T>` wrapper structure.

### Sibling convention analysis

Examine `modules/fundamental/src/advisory/endpoints/list.rs` and
`modules/fundamental/src/sbom/endpoints/list.rs` as siblings to the package list endpoint.
Extract patterns for:
- Query struct definition with optional filter fields
- Handler function signature (`Result<T, AppError>`)
- How filters are passed from endpoint to service
- Error handling with `.context()` wrapping

Examine `tests/api/advisory.rs` and `tests/api/sbom.rs` as siblings for test conventions:
- Test function naming
- Assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`)
- Test database setup
- Response body parsing

### Documentation file identification

- `CONVENTIONS.md` at repository root -- read for CI check commands and coding standards
- `docs/api.md` -- check if package endpoint is documented; update if so

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct**: Following the pattern from the advisory
   endpoint's Query struct (which has an optional `severity` field), add:

   ```rust
   /// Optional license filter. Supports comma-separated SPDX identifiers.
   pub license: Option<String>,
   ```

   This mirrors the advisory endpoint's `severity: Option<String>` field exactly.

2. **Pass the license filter to the service layer**: In the list handler function, extract
   `query.license` and pass it to `PackageService::list()`. Follow the same pattern used
   in the advisory endpoint where `query.severity` is passed to `AdvisoryService::list()`.

3. **Validate the license parameter**: Add validation for the license parameter. If the
   value is present but empty or contains invalid characters, return a 400 Bad Request
   using `AppError`. Follow the existing error handling pattern with `.context()`.

**Reuse:** The Query struct pattern is taken directly from the advisory endpoint's list.rs.
No new filtering logic is written here -- the actual filtering is delegated to
`apply_filter` in the service layer.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Update the `list` method signature**: Add an optional `license: Option<String>`
   parameter to the `list` method, following the pattern of the advisory service's `list`
   method which accepts `severity: Option<String>`.

2. **Apply the license filter using `apply_filter`**: When the `license` parameter is
   `Some`, use `common::db::query::apply_filter` to:
   - Parse the comma-separated license string into individual values
   - Generate a SQL `IN` clause filtering on the license column
   
   This reuses `apply_filter` directly -- no custom parsing or SQL generation needed.

3. **Join through `package_license` entity**: Use the SeaORM entity from
   `entity/src/package_license.rs` to join the `package` table to the `package_license`
   table when the license filter is active. This follows SeaORM's relation-based join
   pattern rather than raw SQL.

   ```rust
   // When license filter is present, join through package_license entity
   if let Some(ref license) = license {
       // Join package -> package_license
       // Apply apply_filter on the license column with the comma-separated value
       query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
       apply_filter(&mut query, package_license::Column::License, license);
   }
   ```

4. **Ensure DISTINCT results**: When joining through the package_license table, a package
   with multiple matching licenses could appear multiple times. Add `.distinct()` to the
   query when the license filter is active.

**Reuse:**
- `apply_filter` from `common/src/db/query.rs` handles all comma-separated parsing and
  IN clause generation
- `package_license` entity from `entity/src/package_license.rs` provides the join relation
- The overall pattern follows the advisory service's severity filtering approach

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create integration tests following the patterns in `tests/api/advisory.rs` and
`tests/api/sbom.rs`:

```rust
/// Verifies that filtering by a single license returns only matching packages.
#[tokio::test]
async fn test_single_license_filter() {
    // Given a test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0)
    // When requesting GET /api/v2/package?license=MIT
    // Then only packages with MIT license are returned
    // Assert on specific package identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_multi_license_filter() {
    // Given a test database with packages having different licenses
    // When requesting GET /api/v2/package?license=MIT,Apache-2.0
    // Then packages with either MIT or Apache-2.0 license are returned
    // Assert on specific package identifiers
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_no_license_filter_returns_all() {
    // Given a test database with packages
    // When requesting GET /api/v2/package (no license param)
    // Then all packages are returned
    // Assert response matches baseline (no regression)
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_invalid_license_returns_400() {
    // Given a test database
    // When requesting GET /api/v2/package?license=<invalid>
    // Then response status is 400 Bad Request
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

Each test:
- Uses the project's test database setup pattern from sibling tests
- Uses `assert_eq!(resp.status(), StatusCode::OK)` assertion style
- Asserts on actual package values, not just collection length
- Includes doc comments explaining what is verified
- Uses given-when-then section comments for non-trivial tests

### Module registration

Register the new test file in `tests/api/` by adding `mod package_license_filter;` to
the test module's `mod.rs` or `main.rs` (check the existing test module structure in
`tests/Cargo.toml` and `tests/api/`).

### Documentation impact

Check `docs/api.md` for package endpoint documentation. If the `GET /api/v2/package`
endpoint is documented there, add the new `license` query parameter to its parameter list
with description: "Optional. SPDX license identifier to filter by. Supports
comma-separated values for OR matching."

## Step 8 -- Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_single_license_filter` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | `test_multi_license_filter` |
| `GET /api/v2/package` without license returns all packages | `test_no_license_filter_returns_all` |
| Response shape (`PaginatedResults<PackageSummary>`) unchanged | All tests deserialize into same response type |
| Invalid license values return 400 | `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification Checks

1. **Scope containment**: Verify `git diff --name-only` only shows the 2 modified files
   and 1 created file plus any test module registration file.
2. **Duplication check**: Grep for `apply_filter` usage to confirm we are reusing it, not
   reimplementing filtering logic. Per constraint 5.4, do not duplicate existing filtering
   logic.
3. **Dead parameter detection**: Check that no parameters became unused after modifications.
4. **Data-flow trace**: license query param -> endpoint Query struct extraction -> service
   layer `list()` method -> `apply_filter` generates SQL IN clause -> SeaORM join through
   `package_license` entity -> filtered results returned as `PaginatedResults<PackageSummary>`.
5. **CI checks**: Run commands from `CONVENTIONS.md` if present; otherwise run `cargo check`,
   `cargo fmt --check`, `cargo clippy`, `cargo test -p fundamental`.
6. **Sensitive pattern check**: Scan staged diff for secrets/credentials.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
      modules/fundamental/src/package/service/mod.rs \
      tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX identifier filtering.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203"
```

Then create PR targeting `main` with description referencing TC-9203.
