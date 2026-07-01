# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Parse Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **No Target PR** (standard flow -- create new branch)
- **No Bookend Type** (standard implementation)
- **Dependencies**: None

## Step 4 -- Code Understanding Plan

### Files to Inspect (using Serena `serena_backend`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - Use `get_symbols_overview` to understand current query struct and handler function
   - Use `find_symbol` with `include_body=true` to read the handler and any Query/Filter structs

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - Use `get_symbols_overview` to see PackageService methods
   - Use `find_symbol` on the `list` method to understand its current signature and query construction

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- sibling pattern)
   - Use `get_symbols_overview` to see how the severity filter Query struct is defined
   - Use `find_symbol` on the Query struct and handler to understand the pattern for optional filter fields

4. **`common/src/db/query.rs`** (reuse candidate -- shared utility)
   - Use `find_symbol` on `apply_filter` to understand its signature, how it parses comma-separated values, and how it generates SQL IN clauses

5. **`entity/src/package_license.rs`** (reuse candidate -- entity)
   - Use `get_symbols_overview` to understand the SeaORM entity structure: columns, relations, primary key

6. **`modules/fundamental/src/package/model/summary.rs`** (context -- response type)
   - Use `get_symbols_overview` to confirm PackageSummary already includes a `license` field (per repo description)

### Sibling Convention Analysis

- Examine `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` as siblings to identify:
  - Query struct pattern (how optional filter fields are declared)
  - Handler function signature and return type
  - How filters are passed from endpoint to service layer
  - Error handling approach (`Result<T, AppError>` with `.context()`)

### Test Convention Analysis

- Examine `tests/api/advisory.rs` and `tests/api/sbom.rs` as sibling test files to identify:
  - Assertion patterns (e.g., `assert_eq!(resp.status(), StatusCode::OK)`)
  - Response body deserialization approach
  - Test setup/database seeding patterns
  - Test naming conventions
  - Error case testing (400, 404 patterns)

### Documentation Files

- `docs/api.md` -- may need updating if it documents the package list endpoint parameters
- `CONVENTIONS.md` -- check for CI verification commands

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing query parameter struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).

2. **Extract and pass filter to service**: In the handler function, extract `query.license` and pass it to the `PackageService::list` method call. If `license` is `Some`, pass it through; if `None`, no filter is applied.

3. **Input validation**: Add validation for the license parameter before passing to the service. If the license string contains invalid characters (not valid for SPDX identifiers), return a 400 Bad Request using the existing `AppError` pattern from `common/src/error.rs`.

**Reuse:**
- Follow the exact Query struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter). The license field will be structurally identical: `pub license: Option<String>`.
- Use `AppError` from `common/src/error.rs` for error responses.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Update the `list` method signature**: Add an optional `license: Option<String>` parameter to the `list` method of `PackageService`.

2. **Build the filter query**: When `license` is `Some`:
   - Call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated license string into individual values and generate the appropriate SQL `IN` clause.
   - Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license records.
   - The join uses the SeaORM relation between the `package` and `package_license` entities.

3. **When `license` is `None`**: No filter is applied; the existing query runs unchanged (no regression).

**Reuse:**
- `common/src/db/query.rs::apply_filter` -- call directly to handle comma-separated parsing and SQL IN clause generation. Do NOT reimplement this logic.
- `entity/src/package_license.rs` -- use the existing SeaORM entity for the JOIN rather than writing raw SQL. Use its `Column` and `Relation` definitions to construct the filter query.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create a new integration test file with the following test functions. All tests follow the patterns discovered from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: seed the test database with packages having different licenses (e.g., MIT, Apache-2.0, GPL-3.0)
   - When: `GET /api/v2/package?license=MIT`
   - Then: assert status 200, deserialize `PaginatedResults<PackageSummary>`, assert all returned items have `license == "MIT"`, assert specific expected packages are present by name/identifier

2. **`test_list_packages_filter_multi_license`**
   - Doc comment: `/// Verifies that comma-separated license filtering returns packages matching any listed license.`
   - Given: seed the test database with packages having different licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert status 200, deserialize response, assert returned items have license matching either "MIT" or "Apache-2.0", assert specific expected packages are present

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages (no regression).`
   - Given: seed the test database with packages having different licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: assert status 200, assert total_count includes all seeded packages, assert response shape is `PaginatedResults<PackageSummary>`

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: no special setup needed
   - When: `GET /api/v2/package?license=!!!invalid!!!`
   - Then: assert status 400 (Bad Request)

**Conventions applied:**
- Test naming: `test_list_packages_<scenario>` (matches `test_<endpoint>_<scenario>` pattern)
- Assertions: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Value-based assertions on specific items, not just length checks
- Given-when-then section comments in non-trivial tests
- All test functions have `///` doc comments

### Documentation Impact

- Check `docs/api.md` for package endpoint documentation. If the `GET /api/v2/package` endpoint is documented there, add the `license` query parameter to its parameter list with description: "Optional. Filter by SPDX license identifier. Supports comma-separated values for OR filtering (e.g., `MIT,Apache-2.0`)."

## Step 8 -- Acceptance Criteria Verification

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Verified by `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Verified by `test_list_packages_filter_multi_license` |
| `GET /api/v2/package` without license returns all packages | Verified by `test_list_packages_no_license_filter` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | Verified in all tests -- deserialization succeeds with same type |
| Invalid license values return 400 | Verified by `test_list_packages_invalid_license` |

## Step 9 -- Self-Verification Checklist

- **Scope containment**: Only `list.rs`, `service/mod.rs`, and `package_license_filter.rs` are modified/created -- all within Files to Modify / Files to Create
- **Sensitive-pattern check**: No secrets or env files involved
- **Documentation currency**: Update `docs/api.md` if it documents the package endpoint
- **Duplication check**: Grep for any existing license filter logic to ensure we are not duplicating; confirm `apply_filter` is being reused, not reimplemented
- **Data-flow trace**: Request (`license` query param) -> endpoint extraction -> service layer filter construction (via `apply_filter`) -> SeaORM JOIN query through `package_license` entity -> filtered results returned as `PaginatedResults<PackageSummary>` -- COMPLETE path
- **Contract & sibling parity**: PackageService `list` method maintains same return type; handler follows same `Result<T, AppError>` pattern as advisory/sbom siblings

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that filters
packages by SPDX license identifier. Supports single-value and comma-separated
multi-value filtering using the existing apply_filter utility.

Implements TC-9203"
```

Then push and create PR:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```
