# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: present with `trustify-backend` entry, Serena instance `serena_backend`, path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: present with tool naming convention and `serena_backend` instance configured

Validation passes. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from TC-9203:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a `license` query parameter to `GET /api/v2/package` list endpoint for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering.
- **Files to Modify**: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs`
- **Files to Create**: `tests/api/package_license_filter.rs`
- **API Changes**: `GET /api/v2/package?license=MIT` (add optional param), `GET /api/v2/package?license=MIT,Apache-2.0` (comma-separated)
- **Bookend Type**: none
- **Target PR**: none
- **Dependencies**: none

No missing sections. Proceeding.

## Step 4 -- Understand the Code

### Code inspection plan

Using Serena instance `serena_backend` (from Repository Registry), the following inspections would be performed:

1. **`modules/fundamental/src/package/endpoints/list.rs`** -- `get_symbols_overview` to understand current Query struct and handler function structure. `find_symbol` on the handler function and the Query struct to read their bodies.

2. **`modules/fundamental/src/package/service/mod.rs`** -- `get_symbols_overview` to see PackageService methods. `find_symbol` on the `list` method to understand its current signature and query-building logic.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (sibling reference) -- `get_symbols_overview` to examine the advisory list endpoint's Query struct and handler. `find_symbol` on the advisory Query struct to see how the `severity` field is defined and how the filter is applied. This is the primary reuse reference.

4. **`common/src/db/query.rs`** -- `find_symbol` on `apply_filter` with `include_body=true` to understand its signature, parameter types, and how it handles comma-separated values and SQL IN clause generation.

5. **`entity/src/package_license.rs`** -- `get_symbols_overview` to see the SeaORM entity definition, its columns, and relation definitions for the package-license join table.

6. **`modules/fundamental/src/package/model/summary.rs`** -- `get_symbols_overview` to confirm the PackageSummary struct has a `license` field and verify its type.

7. **Backward compatibility**: `find_referencing_symbols` on the package list handler and the PackageService `list` method to identify all callers and ensure new optional parameters do not break them.

### Sibling convention analysis

**Sibling files identified** (same structural role):
- `modules/fundamental/src/advisory/endpoints/list.rs` -- advisory list endpoint (filter pattern reference)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- SBOM list endpoint (structural sibling)

**Discovered conventions (from repo structure and conventions)**:
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list_packages`)
- **Query struct**: Each list endpoint defines a Query struct with optional filter fields, deserialized from query parameters

### Test convention analysis

**Sibling test files identified**:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Discovered test conventions**:
- **Testing approach**: Integration tests hit a real PostgreSQL test database
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and key fields of items
- **Error cases**: Tests include status code assertions for error responses (e.g., `StatusCode::BAD_REQUEST`)

### Documentation files identified

- `docs/api.md` -- REST API reference (may need updating to document the new `license` parameter)
- `README.md` -- general project documentation (unlikely to need changes)

### CONVENTIONS.md

Would check for `CONVENTIONS.md` at repository root. Per the repo structure, it exists. Would read it for CI check commands and code generation commands.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes**:

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing Query struct used for deserializing query parameters. Follow the exact same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter. Supports single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass `license` filter to the service layer**: In the handler function, pass `query.license` to the `PackageService::list` method. This follows the same pattern as how the advisory handler passes `query.severity` to `AdvisoryService::list`.

   ```rust
   let result = service
       .list(
           // ... existing parameters
           query.license.as_deref(),
       )
       .await?;
   ```

**Reuse applied**: The Query struct pattern is reused from the advisory endpoint's Query struct. No new filtering logic is written in the endpoint layer -- the handler simply extracts the parameter and delegates to the service.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes**:

1. **Add `license` parameter to the `list` method signature**: Add an `Option<&str>` parameter for the license filter.

   ```rust
   pub async fn list(
       &self,
       // ... existing parameters
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter using `apply_filter` from `common/src/db/query.rs`**: When the `license` parameter is `Some`, use the existing `apply_filter` function to build the SQL WHERE clause. This function already handles:
   - Parsing comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
   - Generating a SQL `IN` clause for multi-value filters
   - Single-value equality for single values

   ```rust
   use common::db::query::apply_filter;
   use entity::package_license;

   // In the list method body:
   let mut query = package::Entity::find();

   if let Some(license) = license {
       // Join through the package_license entity
       query = query
           .join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
       // Apply the filter using the shared helper
       query = apply_filter(query, package_license::Column::License, license)?;
   }
   ```

3. **Validate license parameter**: If `apply_filter` does not already handle validation of empty or malformed values, add validation that returns `AppError` (400 Bad Request) for invalid license values (e.g., empty string, only commas).

**Reuse applied**: 
- `apply_filter` from `common/src/db/query.rs` is called directly -- no duplication of comma-separated parsing or SQL IN clause generation.
- `entity::package_license` entity is used for the JOIN, leveraging SeaORM's relation definitions rather than writing raw SQL.
- The overall pattern mirrors the advisory service's severity filter implementation.

### File 3 (new): `tests/api/package_license_filter.rs`

**Changes**:

Create integration tests following the patterns in `tests/api/advisory.rs`:

1. **`test_filter_single_license`**: Seed packages with different licenses (MIT, Apache-2.0, GPL-3.0). Query `GET /api/v2/package?license=MIT`. Assert response status is 200, assert all returned items have license `MIT`, assert specific item values (not just count).

2. **`test_filter_comma_separated_licenses`**: Using the same seed data, query `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response status is 200, assert returned items include both MIT and Apache-2.0 licensed packages, assert GPL-3.0 packages are excluded.

3. **`test_no_license_filter_returns_all`**: Query `GET /api/v2/package` without a license parameter. Assert response status is 200, assert all seeded packages are returned (regression guard).

4. **`test_invalid_license_returns_400`**: Query `GET /api/v2/package?license=` (empty value). Assert response status is 400 Bad Request.

Each test function will have:
- A `///` doc comment explaining what it verifies
- Given/When/Then section comments inside the test body
- Value-based assertions on specific package fields, not just length checks

**Test file registration**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) so the test module is compiled and run.

### Documentation impact

- **`docs/api.md`**: Would update the `GET /api/v2/package` section to document the new optional `license` query parameter, its accepted format (single SPDX identifier or comma-separated list), and example usage.

## Step 7 -- Tests

Run `cargo test` targeting the new test module. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Covered by `test_filter_comma_separated_licenses` |
| `GET /api/v2/package` without license returns all | Covered by `test_no_license_filter_returns_all` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | Service method return type is unchanged; existing deserialization tests would catch shape changes |
| Invalid license values return 400 | Covered by `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment
Expected modified/created files:
- `modules/fundamental/src/package/endpoints/list.rs` (in scope)
- `modules/fundamental/src/package/service/mod.rs` (in scope)
- `tests/api/package_license_filter.rs` (in scope)
- `docs/api.md` (documentation impact -- would flag as out-of-scope and ask user for approval)

### Duplication check
Search for any existing license filtering logic in the codebase using `search_for_pattern` on terms like `license_filter`, `filter_by_license`. Confirm no duplication with the `apply_filter`-based approach.

### Data-flow trace
`GET /api/v2/package?license=MIT` -> endpoint extracts `license` from Query struct -> passes to `PackageService::list` -> `apply_filter` builds SQL IN clause -> SeaORM joins `package_license` table -> filtered results returned as `PaginatedResults<PackageSummary>` -> serialized as JSON response. **COMPLETE**.

### Contract and sibling parity
- The Query struct gains an optional field -- backward compatible with existing callers since `license` defaults to `None`
- PackageService `list` method gains an optional parameter -- all callers must be updated to pass the new argument (or use a default). `find_referencing_symbols` on the `list` method would identify all callers.
- Sibling parity: advisory list endpoint supports `severity` filter with same approach; package list endpoint now supports `license` filter with identical pattern.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to list endpoint

Add optional license query parameter to GET /api/v2/package that supports
single-value and comma-separated multi-value SPDX license filtering. Reuses
apply_filter from common/src/db/query.rs and the package_license entity for
JOIN queries, following the same pattern as the advisory severity filter.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --base main --title "feat(package): add license filter to list endpoint" --body "..."
```

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL using ADF format
- Add comment summarizing changes and PR link
- Transition TC-9203 to In Review
