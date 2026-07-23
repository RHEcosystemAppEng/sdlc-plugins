# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: serena_backend with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from TC-9203:

| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR | (none) |
| Bookend Type | (none) |
| Dependencies | None |

**Description**: Add a `license` query parameter to `GET /api/v2/package` for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering.

**Files to Modify**:
1. `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method

**Files to Create**:
1. `tests/api/package_license_filter.rs` -- integration tests for the license filter

**API Changes**:
- `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
- `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values

**Reuse Candidates** (3 identified in task description):
1. `common/src/db/query.rs::apply_filter`
2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)
3. `entity/src/package_license.rs` (package-license join entity)

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9203)`, search for the `[sdlc-workflow] Description digest:` marker, and compare the stored digest against a freshly computed digest of the current description. Since this is a simulation, this step is noted but not executed.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would call `jira.user_info()` to get current user, `jira.edit_issue(TC-9203, assignee=...)` to assign, and `jira.transition_issue(TC-9203, "In Progress")`. Not executed in simulation.

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

**`modules/fundamental/src/package/endpoints/list.rs`** (current state):
- Would use `mcp__serena_backend__get_symbols_overview` to see the existing query struct and handler function
- Expected to find a `PackageQuery` or similar struct with pagination fields (page, limit) and possibly sorting
- The handler function extracts query params via Axum's `Query<T>` extractor and calls `PackageService::list()`

**`modules/fundamental/src/package/service/mod.rs`** (current state):
- Would use `mcp__serena_backend__get_symbols_overview` to see `PackageService` struct and its `list` method
- The `list` method likely queries the `package` table with pagination and returns `PaginatedResults<PackageSummary>`

### 4.2 Inspect reuse candidate files

**`common/src/db/query.rs`** -- the `apply_filter` function:
- Would use `mcp__serena_backend__find_symbol` with `include_body=true` on `apply_filter`
- Expected signature: takes a query builder (or `SelectStatement`), a column reference, and a filter string (potentially comma-separated), then applies an `IN` clause or equality filter
- Handles comma-splitting internally so callers just pass the raw query parameter value

**`modules/fundamental/src/advisory/endpoints/list.rs`** -- severity filter (sibling pattern):
- Would use `mcp__serena_backend__get_symbols_overview` then `find_symbol` on the query struct
- Expected to find an `AdvisoryQuery` struct with an `Option<String>` field for `severity`
- The handler extracts `severity` from query params, passes it to `AdvisoryService::list()`, which calls `apply_filter` with the severity column and filter value
- This is the structural pattern to replicate for the license filter

**`entity/src/package_license.rs`** -- join entity:
- Would use `mcp__serena_backend__get_symbols_overview` to see the SeaORM entity definition
- Expected to find `Entity`, `Model`, `Column`, and `Relation` definitions mapping packages to licenses
- The `Relation` will define the foreign key to the `package` table, which is needed for the JOIN

### 4.3 Check backward compatibility

- Would use `mcp__serena_backend__find_referencing_symbols` on `PackageService::list` to identify all callers
- The package list endpoint handler is the primary caller; need to ensure the new `license` parameter is optional so existing callers without it continue to work

### 4.4 Convention conformance analysis (sibling analysis)

**Sibling endpoints inspected**: `advisory/endpoints/list.rs`, `sbom/endpoints/list.rs`

**Discovered conventions**:
- **Query struct pattern**: Each list endpoint defines a query struct (e.g., `AdvisoryQuery`) with optional filter fields as `Option<String>`, pagination fields (`page: Option<u64>`, `limit: Option<u64>`), and optional sort fields. The struct derives `Deserialize` and is used with Axum's `Query<T>` extractor.
- **Error handling**: All handlers return `Result<Json<PaginatedResults<T>>, AppError>` with `.context()` wrapping on service calls.
- **Service method pattern**: Service `list` methods accept filter parameters as `Option<&str>` and return `Result<PaginatedResults<T>>`. Filters are applied conditionally when `Some`.
- **Filter application**: Filters use `apply_filter` from `common/src/db/query.rs` which handles comma-separated values and generates SQL `IN` clauses via SeaORM's `ColumnTrait::is_in()`.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list_packages`, `get_advisory`).
- **Response type**: All list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### 4.5 Test convention analysis

**Sibling test files inspected**: `tests/api/advisory.rs`, `tests/api/sbom.rs`

**Discovered test conventions**:
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into `PaginatedResults<T>`.
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields (not just length checks).
- **Error cases**: Tests include status code assertions for error cases (e.g., `StatusCode::BAD_REQUEST`).
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered_by_severity`).
- **Setup**: Tests seed the database with known test data before assertions, using helper functions or direct inserts.
- **Parameterized tests**: Need to check if the project uses `rstest` -- if sibling tests do not use it, individual test functions will be written instead.

### 4.6 Documentation file identification

- `CONVENTIONS.md` at repository root -- would check for CI commands
- `docs/api.md` -- may need updating if it documents the package list endpoint query parameters
- `README.md` -- unlikely to need changes for a filter addition

### 4.7 CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at the repository root and extract any CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). These would be run in Step 9.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

Standard flow: no Target PR, no Bookend Type.

## Step 6 -- Implement Changes

### 6.1 Modify `modules/fundamental/src/package/endpoints/list.rs`

**What to change**: Add a `license` field to the query parameter struct and pass it to the service layer.

**Detailed changes**:

1. **Add `license` field to query struct** (e.g., `PackageQuery` or `PackageListQuery`):
   ```rust
   /// Query parameters for the package list endpoint.
   #[derive(Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (page, limit, sort, etc.) ...

       /// Optional license filter. Accepts a single SPDX identifier or
       /// comma-separated list (e.g., "MIT" or "MIT,Apache-2.0").
       pub license: Option<String>,
   }
   ```

2. **Pass `license` to service call** in the handler function:
   ```rust
   // In the handler function:
   let result = package_service
       .list(/* existing params */, query.license.as_deref())
       .await
       .context("Failed to list packages")?;
   ```

3. **Add import** for `apply_filter` if not already imported (from `common::db::query`).

### 6.2 Modify `modules/fundamental/src/package/service/mod.rs`

**What to change**: Accept the license filter parameter in the `list` method and apply it via a JOIN to the `package_license` table using `apply_filter`.

**Detailed changes**:

1. **Update `list` method signature** to accept an optional license filter:
   ```rust
   /// Lists packages with optional filtering by license.
   pub async fn list(
       &self,
       /* existing params */
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>> {
   ```

2. **Apply the license filter** using a JOIN through `package_license` entity and `apply_filter`:
   ```rust
   use entity::package_license;
   use common::db::query::apply_filter;

   // Build the base query
   let mut query = /* existing query builder */;

   // Apply license filter if provided
   if let Some(license_filter) = license {
       // JOIN package_license table
       query = query.join(
           JoinType::InnerJoin,
           package_license::Relation::Package.def().rev(),
       );
       // Apply filter using the shared apply_filter helper
       // This handles comma-separated values (e.g., "MIT,Apache-2.0")
       // and generates a SQL IN clause
       query = apply_filter(query, package_license::Column::License, license_filter)?;
   }
   ```

3. **Validate the license parameter**: If `apply_filter` does not already handle invalid values with a 400 response, add validation that returns `AppError` with a 400 status for empty or malformed license values. Follow the pattern from the advisory severity filter for error handling.

4. **Ensure DISTINCT results**: Since the JOIN through `package_license` may produce duplicate packages (if a package has multiple licenses matching the filter), apply `.distinct()` to the query or use a subquery/EXISTS approach matching what sibling filters do.

### 6.3 No additional files to modify

- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration should not need changes since the endpoint path stays the same; only the query parameters change
- `entity/src/package_license.rs` -- reused as-is, no modifications needed
- `common/src/db/query.rs` -- reused as-is via `apply_filter`, no modifications needed

## Step 7 -- Write Tests

### Create `tests/api/package_license_filter.rs`

**Test structure** following sibling conventions from `tests/api/advisory.rs`:

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response is 200 OK, `PaginatedResults<PackageSummary>` contains only MIT-licensed packages, assert on specific package names/IDs (not just count)

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response is 200 OK, result contains packages with MIT or Apache-2.0 (but not GPL-3.0), assert on specific values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged (no regression).`
   - Given: Seed database with packages having various licenses
   - When: `GET /api/v2/package` (no license param)
   - Then: Response is 200 OK, all packages returned, count matches total seeded

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Database with valid packages
   - When: `GET /api/v2/package?license=` (empty value or invalid characters)
   - Then: Response is 400 Bad Request

Each test will include `// Given`, `// When`, `// Then` section comments for non-trivial tests.

**Registration**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the appropriate test module file) if the test directory uses module declarations.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | Covered by test 1 and code review of filter logic |
| GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | Covered by test 2 and apply_filter's comma handling |
| GET /api/v2/package without license returns all packages | Covered by test 3 and Optional parameter (None = no filter) |
| Response shape PaginatedResults<PackageSummary> unchanged | No changes to response types or serialization |
| Invalid license values return 400 | Covered by test 4 and validation logic |

## Step 9 -- Self-Verification Plan

1. **Scope containment**: `git diff --name-only` should show only the 2 modified files and 1 created file listed in the task
2. **Untracked file check**: Verify `tests/api/package_license_filter.rs` appears as untracked and should be staged
3. **Sensitive-pattern check**: Scan staged diff for secrets/credentials
4. **Documentation currency**: Check if `docs/api.md` documents package list endpoint query params -- if so, add `license` parameter documentation
5. **CI checks**: Run commands from CONVENTIONS.md (likely `cargo fmt --check`, `cargo clippy`, `cargo test`)
6. **Duplication check**: Search for any existing license filtering logic elsewhere in the codebase
7. **Data-flow trace**: `GET request` -> extract license query param -> pass to PackageService::list() -> apply_filter with JOIN -> SQL query -> PaginatedResults response -- **COMPLETE**
8. **Contract & sibling parity**: Verify PackageService::list() follows same pattern as AdvisoryService::list() for filter parameters
9. **Cross-section reference consistency**: Files to Modify and Implementation Notes reference consistent paths

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs
git add modules/fundamental/src/package/service/mod.rs
git add tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports single SPDX identifier and comma-separated multi-value
filtering. Reuses the existing apply_filter helper and joins through
the package_license entity.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Step 11 -- Update Jira

- Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment summarizing changes and linking to PR
- Transition TC-9203 to "In Review"
