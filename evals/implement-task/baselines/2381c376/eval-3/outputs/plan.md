# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena with `rust-analyzer`

Configuration is valid. Proceed.

## Step 1 -- Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira ID**: TC-9203
- **Linked Issues**: is incorporated by TC-9001
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none

### Files to Modify
1. `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method

### Files to Create
1. `tests/api/package_license_filter.rs` -- integration tests for the license filter

### API Changes
- `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
- `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated license values

### Acceptance Criteria
1. GET /api/v2/package?license=MIT returns only packages with MIT license
2. GET /api/v2/package?license=MIT,Apache-2.0 returns packages matching either license
3. GET /api/v2/package without license parameter returns all packages (no regression)
4. Response shape (PaginatedResults<PackageSummary>) remains unchanged
5. Invalid license values return 400 Bad Request

## Step 2 -- Verify Dependencies

No dependencies. Proceed.

## Step 4 -- Understand the Code

### Code inspection plan (using Serena instance `serena_backend`)

1. **Existing endpoint pattern**: Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` to understand the severity filter Query struct pattern. Use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function and the Query struct to read the exact implementation.

2. **Query helper**: Use `mcp__serena_backend__find_symbol` on `common/src/db/query.rs::apply_filter` with `include_body=true` to understand the signature, parameters, and how it handles comma-separated values and generates SQL IN clauses.

3. **Package endpoint current state**: Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/list.rs` to see the current Query struct and handler. Read the existing handler body to understand how query parameters are extracted and passed to the service.

4. **Package service current state**: Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/service/mod.rs` to see the PackageService list method signature and body.

5. **Package license entity**: Use `mcp__serena_backend__find_symbol` on `entity/src/package_license.rs` to understand the SeaORM entity -- columns, relations, and table name. This entity maps packages to licenses and will be used for the JOIN.

6. **Package entity**: Use `mcp__serena_backend__get_symbols_overview` on `entity/src/package.rs` to understand the Package entity and its relations to PackageLicense.

7. **Backward compatibility**: Use `mcp__serena_backend__find_referencing_symbols` on the PackageService list method to identify all callers and ensure adding an optional license filter parameter does not break them.

8. **Sibling convention analysis**: Examine `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` as sibling files to extract naming conventions, error handling, and Query struct patterns.

9. **Test convention analysis**: Examine `tests/api/advisory.rs` and `tests/api/sbom.rs` to understand integration test patterns -- setup, assertion style, response validation, naming.

10. **Documentation files**: Check for `CONVENTIONS.md` at repository root, `README.md`, and `docs/api.md` for documentation that may need updates.

### Expected conventions (from sibling analysis)

- **Query struct pattern**: Each list endpoint defines a `Query` struct with `#[derive(Deserialize)]` containing optional filter fields. The Axum handler extracts it with `Query<PackageQuery>`.
- **Error handling**: Handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Service method pattern**: Service methods accept optional filter parameters and build queries conditionally.
- **Response type**: List endpoints return `PaginatedResults<PackageSummary>`.
- **Filter application**: Uses `apply_filter` from `common/src/db/query.rs` for comma-separated multi-value filtering.
- **Test pattern**: Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` and validate response bodies against expected values.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the Query struct**: Following the advisory list endpoint's severity filter pattern, add an `Option<String>` field named `license` to the existing `Query` (or equivalent) struct used by the package list handler.

   ```rust
   /// Query parameters for the package list endpoint.
   #[derive(Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter. Supports single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter.

   ```rust
   let result = service.list(/* existing params */, query.license.as_deref()).await?;
   ```

3. **Validate license parameter**: Add validation for the license parameter -- if present but empty or containing only whitespace, return 400 Bad Request. This follows the defensive property access guidance and satisfies AC #5.

**Reuse**: Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/list.rs` where the severity Query struct field is defined and passed to the service. No new code patterns needed -- mirror the advisory approach.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add license filter parameter to the list method**: Add an `Option<&str>` parameter `license` to the `list` (or equivalent) method signature of PackageService.

   ```rust
   /// Lists packages with optional filtering by license SPDX identifier.
   pub async fn list(
       &self,
       // ... existing parameters
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Build the license filter query**: When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and generate a SQL `IN` clause. Join through the `package_license` entity to filter packages by license.

   ```rust
   if let Some(license_filter) = license {
       let license_values = apply_filter(license_filter);
       // Join package_license table and add WHERE clause:
       // WHERE package_license.license IN (license_values)
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(package_license::Column::License.is_in(license_values));
   }
   ```

3. **Error handling for invalid values**: If `apply_filter` returns an empty list or the license values fail validation, return an `AppError` with a 400 status.

4. **Ensure deduplication**: Since the JOIN through `package_license` could produce duplicate packages (a package with multiple licenses matching the filter), add `.distinct()` to the query to ensure unique results.

**Reuse**:
- `common/src/db/query.rs::apply_filter` -- reused directly for comma-separated parsing and value extraction
- `entity/src/package_license.rs` -- reused as the SeaORM entity for the JOIN, using its Column and Relation definitions
- Advisory service list method pattern -- followed structurally for conditional filter application

### File 3 (new): `tests/api/package_license_filter.rs`

**Create integration tests following the patterns in `tests/api/advisory.rs`:**

```rust
/// Verifies that filtering by a single license returns only matching packages.
#[tokio::test]
async fn test_single_license_filter() {
    // Given a test database with packages having MIT and Apache-2.0 licenses
    let app = setup_test_app().await;
    seed_packages_with_licenses(&app, vec![
        ("pkg-a", "MIT"),
        ("pkg-b", "Apache-2.0"),
        ("pkg-c", "MIT"),
    ]).await;

    // When requesting packages filtered by MIT license
    let resp = app.get("/api/v2/package?license=MIT").await;

    // Then only MIT-licensed packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert!(body.items.iter().all(|p| p.license == "MIT"));
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[tokio::test]
async fn test_comma_separated_license_filter() {
    // Given a test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    let app = setup_test_app().await;
    seed_packages_with_licenses(&app, vec![
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

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_no_license_filter_returns_all() {
    // Given a test database with packages having various licenses
    let app = setup_test_app().await;
    seed_packages_with_licenses(&app, vec![
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
    // Given a test application
    let app = setup_test_app().await;

    // When requesting packages with an empty license filter
    let resp = app.get("/api/v2/package?license=").await;

    // Then a 400 Bad Request is returned
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

**Test module registration**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the appropriate test harness file) if the test module system requires explicit registration.

### Documentation Impact

- The API documentation (`docs/api.md`) should be updated to document the new `license` query parameter on the `GET /api/v2/package` endpoint, including examples for single-value and comma-separated usage.
- No changes needed to architecture docs -- this is an additive filter, not an architectural change.

## Step 8 -- Acceptance Criteria Verification

| # | Criterion | How verified |
|---|-----------|-------------|
| 1 | GET /api/v2/package?license=MIT returns only MIT packages | `test_single_license_filter` |
| 2 | GET /api/v2/package?license=MIT,Apache-2.0 returns either | `test_comma_separated_license_filter` |
| 3 | No license param returns all packages | `test_no_license_filter_returns_all` |
| 4 | Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` |
| 5 | Invalid license returns 400 | `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification Plan

1. **Scope containment**: `git diff --name-only` must show only the three files listed in Files to Modify and Files to Create, plus potentially `tests/api/mod.rs` for test module registration (flag for user approval if needed).
2. **Sensitive-pattern check**: Scan staged diff for secrets.
3. **Duplication check**: Grep for similar filter implementations to ensure no duplication with `apply_filter`.
4. **Dead parameter detection**: Verify no parameters became unused after changes.
5. **CI checks**: Run `CONVENTIONS.md` commands if present, or fallback to `cargo check`, `cargo fmt --check`, `cargo clippy`.
6. **Module-level Rust tests**: Run `cargo test -p <crate>` for each modified crate (fundamental, and the test crate).
7. **Data-flow trace**: Input (HTTP query param `license`) -> Extraction (Axum Query struct) -> Validation (empty check) -> Parsing (`apply_filter` splits commas) -> Query (JOIN + IN clause via SeaORM) -> Response (filtered `PaginatedResults<PackageSummary>`). Complete path.
8. **Contract & sibling parity**: Verify the PackageService list method signature change is backward-compatible with all callers by checking references. Confirm the filter pattern matches advisory endpoint sibling.

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated SPDX identifiers. Reuses apply_filter
from common/src/db/query.rs and joins through the existing package_license
entity rather than duplicating filter logic.

Implements TC-9203"
```

Then push and create PR:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Step 11 -- Update Jira

1. Set Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format.
2. Add comment with PR link, summary of changes, and confirmation of reuse approach.
3. Transition TC-9203 to In Review.
