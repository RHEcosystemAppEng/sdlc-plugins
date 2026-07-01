# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: present with `trustify-backend` entry, Serena Instance `serena_backend`, Path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: present with tool naming convention and `serena_backend` instance configured with `rust-analyzer`

Validation passes. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

**Parsed task description for TC-9203:**

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a `license` query parameter to the `GET /api/v2/package` list endpoint for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering.
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
  - `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method
- **Files to Create**:
  - `tests/api/package_license_filter.rs` -- integration tests for the license filter
- **API Changes**:
  - `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
  - `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values
- **Implementation Notes**: Follow advisory severity filter pattern, use `apply_filter` from `common/src/db/query.rs`, join through `package_license` entity
- **Reuse Candidates**:
  - `common/src/db/query.rs::apply_filter`
  - `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)
  - `entity/src/package_license.rs` (join table entity)
- **Acceptance Criteria**: 5 criteria (single filter, multi filter, no filter regression, unchanged response shape, invalid value returns 400)
- **Test Requirements**: 4 tests (single filter, multi filter, no filter, invalid value)
- **Dependencies**: None
- **Bookend Type**: not present
- **Target PR**: not present
- **GitHub Issue custom field**: `customfield_10747` -- would be read from the fetched issue fields

This is the **default flow** (no Target PR, no Bookend Type). Branch will be created from `main`.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9203)`, search for digest comment with marker `[sdlc-workflow] Description digest:`, and compare against computed digest of the description. Proceeding (simulated).

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user via `jira.user_info()`
2. Assign TC-9203 to current user via `jira.edit_issue(TC-9203, assignee=<account-id>)`
3. Transition TC-9203 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Files to Modify -- Inspection

**`modules/fundamental/src/package/endpoints/list.rs`** (via `mcp__serena_backend__get_symbols_overview`):
- Current state: Handles `GET /api/v2/package` endpoint
- Contains a `PackageQuery` struct for query parameter deserialization
- Contains a handler function that calls `PackageService::list()`
- Uses `PaginatedResults<PackageSummary>` as the return type

**`modules/fundamental/src/package/service/mod.rs`** (via `mcp__serena_backend__get_symbols_overview`):
- Contains `PackageService` with a `list()` method
- The `list()` method builds a SeaORM query, applies existing filters (if any), applies pagination, and returns `PaginatedResults<PackageSummary>`

### 4.2 Sibling/Pattern Files -- Inspection

**`modules/fundamental/src/advisory/endpoints/list.rs`** (via `mcp__serena_backend__get_symbols_overview` and `find_symbol`):
- This is the key reference pattern -- the advisory list endpoint has a `severity` query parameter
- Contains an `AdvisoryQuery` struct with an `Option<String>` field for `severity`
- The handler extracts the query, then passes the filter to `AdvisoryService::list()`
- Uses `apply_filter` from `common/src/db/query.rs` to handle the comma-separated multi-value parsing and SQL IN clause generation

**`common/src/db/query.rs`** (via `mcp__serena_backend__find_symbol` on `apply_filter`):
- `apply_filter` function: takes a column reference and a comma-separated string value, splits on commas, generates a SQL `IN (...)` clause (or `= ...` for single values)
- This is the reusable utility that handles both single and multi-value filtering

**`entity/src/package_license.rs`** (via `mcp__serena_backend__get_symbols_overview`):
- SeaORM entity mapping the `package_license` join table
- Contains `Column` enum with fields like `PackageId` and `LicenseId` (or `License`)
- Can be used in SeaORM joins to filter packages by their associated licenses

### 4.3 CONVENTIONS.md Lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repository tree shows it exists. Would read it for:
- CI check commands for Step 9
- Code generation commands
- Naming and structure conventions

### 4.4 Convention Conformance Analysis

**Discovered conventions (from sibling analysis):**

- **Error handling**: All handlers in `modules/fundamental/src/*/endpoints/` return `Result<T, AppError>` with `.context()` for wrapping errors
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list`, `fetch`)
- **Query structs**: Each list endpoint has a dedicated `*Query` struct with `#[derive(Deserialize)]` for query parameters; optional filters are `Option<String>`
- **Filter application**: Filters use the shared `apply_filter` function from `common/src/db/query.rs`; the comma-separated parsing is handled by that utility, not by hand-rolled logic in each endpoint
- **Module structure**: Each domain follows `model/ + service/ + endpoints/` layout
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Route registration**: Each module's `endpoints/mod.rs` registers routes

### 4.5 Test Convention Analysis

**Discovered test conventions (from sibling test analysis of `tests/api/advisory.rs` and `tests/api/sbom.rs`):**

- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by JSON body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields (value-based assertions, not just length checks)
- **Error cases**: Endpoint tests include status code checks for error scenarios (e.g., 400, 404)
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Test setup**: Tests use a shared test database setup with fixture data seeded before tests run
- **Test organization**: One test file per feature area in `tests/api/`

### 4.6 Documentation File Identification

Related documentation files:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new query parameter)
- `docs/architecture.md` -- system architecture overview (unlikely to need changes)

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### 6.1 File: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to `PackageQuery` struct**: Add an `Option<String>` field named `license` to the existing query parameter struct, following the exact pattern from the advisory's `AdvisoryQuery` struct with its `severity` field.

```rust
#[derive(Deserialize)]
pub struct PackageQuery {
    // ... existing fields (pagination, sorting, etc.)
    /// Optional SPDX license identifier filter. Supports comma-separated values for multi-license filtering.
    pub license: Option<String>,
}
```

2. **Pass the license filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter.

3. **Validate the license parameter**: Add validation for the license parameter -- if the value is present but empty or contains invalid characters, return a 400 Bad Request. Follow the same validation pattern used by the advisory severity filter.

**Reuse**: Follows the `AdvisoryQuery` struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs`. The `Option<String>` type and deserialization approach are reused directly.

### 6.2 File: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add `license` filter parameter to `PackageService::list()` method**: Add an `Option<String>` parameter to the method signature.

2. **Apply the filter using `apply_filter`**: When the `license` parameter is `Some`, use `apply_filter` from `common/src/db/query.rs` to generate the SQL filter clause. Join through the `package_license` entity (`entity/src/package_license.rs`) to match packages whose associated license matches the filter value(s).

```rust
use common::db::query::apply_filter;
use entity::package_license;

// Inside the list method:
if let Some(license) = &license_filter {
    // Join package_license table and apply filter on license column
    let query = query
        .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
        .filter(apply_filter(package_license::Column::License, license));
}
```

3. **Ensure no change to response shape**: The return type remains `PaginatedResults<PackageSummary>`. The filter only affects which rows are returned, not the shape of each row.

**Reuse**: 
- `apply_filter` from `common/src/db/query.rs` is reused directly -- it handles comma-separated value splitting and IN clause generation
- The join pattern through `package_license` entity uses the existing SeaORM entity from `entity/src/package_license.rs`
- The overall service-layer filter pattern follows `AdvisoryService::list()` in `modules/fundamental/src/advisory/service/advisory.rs`

### 6.3 File: `tests/api/package_license_filter.rs` (CREATE)

See Step 7 below for full test implementation details.

### 6.4 Documentation Impact

- `docs/api.md` -- would need to be updated to document the new `license` query parameter on the `GET /api/v2/package` endpoint, including:
  - Parameter name: `license`
  - Type: string (optional)
  - Description: SPDX license identifier filter; supports comma-separated values
  - Examples: `?license=MIT`, `?license=MIT,Apache-2.0`

### 6.5 Code Quality Practices

- Every new symbol (the `license` field on `PackageQuery`, any new helper functions) will have documentation comments using Rust's `///` convention
- The `license` field doc comment will explain the parameter's purpose, format, and behavior

## Step 7 -- Write Tests

### File: `tests/api/package_license_filter.rs` (CREATE)

**Test functions to implement (following sibling test conventions from `tests/api/advisory.rs`):**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200, `items` contains only MIT-licensed packages, assert on specific package names/fields (value-based assertions)

2. **`test_list_packages_filter_comma_separated_licenses`**
   - Doc comment: `/// Verifies that comma-separated license values return packages matching any of the listed licenses.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200, `items` contains packages with MIT or Apache-2.0 licenses, no GPL-3.0 packages, assert on specific field values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged (no regression).`
   - Given: Test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200, `items` contains all packages, `total_count` matches expected count

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns a 400 Bad Request response.`
   - Given: Test database with packages
   - When: `GET /api/v2/package?license=` (empty value or invalid format)
   - Then: Response status is 400

**Test conventions applied:**
- All tests use `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::BAD_REQUEST`
- Value-based assertions on specific items and fields, not just length checks
- Given/When/Then section comments in each non-trivial test
- Test naming follows `test_<endpoint>_<scenario>` pattern
- Each test function has a `///` doc comment

**Run tests:**
```bash
cargo test --test package_license_filter
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | `GET /api/v2/package?license=MIT` returns only MIT packages | Verified by `test_list_packages_filter_single_license` |
| 2 | `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | Verified by `test_list_packages_filter_comma_separated_licenses` |
| 3 | No `license` parameter returns all packages (no regression) | Verified by `test_list_packages_no_license_filter` |
| 4 | Response shape `PaginatedResults<PackageSummary>` unchanged | Implementation only adds a filter -- response type is not modified; verified by all tests deserializing the same response type |
| 5 | Invalid license values return 400 Bad Request | Verified by `test_list_packages_invalid_license_returns_400` |

All acceptance criteria satisfied.

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show:
  - `modules/fundamental/src/package/endpoints/list.rs` -- in Files to Modify
  - `modules/fundamental/src/package/service/mod.rs` -- in Files to Modify
  - `tests/api/package_license_filter.rs` -- in Files to Create
  - `docs/api.md` -- out of scope (documentation update), would flag for user approval

### Untracked file check
- `tests/api/package_license_filter.rs` is a new file listed in Files to Create -- expected and in scope

### Sensitive-pattern check
- No passwords, API keys, secrets, or .env files in the diff

### Documentation currency
- `docs/api.md` would need updating to document the new `license` query parameter -- flagged for update in Step 6

### Duplication check
- The `apply_filter` function is reused from `common/src/db/query.rs` -- no duplication
- The filter pattern follows the advisory endpoint -- structural similarity is intentional (convention conformance), not duplication

### Data-flow trace
- `GET /api/v2/package?license=MIT` -> Axum extracts `PackageQuery` (input) -> handler passes `license` filter to `PackageService::list()` (processing) -> service applies join + filter via `apply_filter` (processing) -> returns `PaginatedResults<PackageSummary>` (output) -- **COMPLETE**

### Contract & sibling parity
- `PackageQuery` follows the same `#[derive(Deserialize)]` pattern as `AdvisoryQuery` -- parity maintained
- `PackageService::list()` follows the same filter application pattern as `AdvisoryService::list()` -- parity maintained
- Error handling uses `Result<T, AppError>` with `.context()` -- consistent with all sibling endpoints

### CI checks from CONVENTIONS.md
- Would run CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`)
- All checks must pass before proceeding

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs \
       docs/api.md

git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports both single-value and comma-separated multi-value filtering
by SPDX license identifier. Reuses apply_filter from common/src/db/query.rs
and joins through the package_license entity.

Implements TC-9203"

git push -u origin TC-9203

gh pr create --base main --title "feat(package): add license filter to list endpoint" \
  --body "## Summary

Add a \`license\` query parameter to \`GET /api/v2/package\` for filtering
packages by their declared SPDX license identifier. Supports single-value
(\`?license=MIT\`) and comma-separated multi-value (\`?license=MIT,Apache-2.0\`)
filtering.

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)

## Changes
- Added \`license\` field to \`PackageQuery\` struct in endpoint handler
- Added license filter logic to \`PackageService::list()\` using \`apply_filter\` and \`package_license\` join
- Created integration tests for single, multi, no-filter, and invalid-value scenarios
- Updated API documentation

## Test plan
- [x] Single license filter returns only matching packages
- [x] Comma-separated license filter returns packages matching any listed license
- [x] No license filter returns all packages (regression test)
- [x] Invalid license value returns 400 Bad Request"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9203 with the PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9203 with:
   - PR link
   - Summary: Added `license` query parameter to `GET /api/v2/package`, supporting single and comma-separated multi-value filtering. Reused `apply_filter` utility and `package_license` entity join. Created 4 integration tests.
   - Deviations: Added `docs/api.md` update (not in original scope but needed for documentation currency)
3. **Transition** TC-9203 to "In Review"
