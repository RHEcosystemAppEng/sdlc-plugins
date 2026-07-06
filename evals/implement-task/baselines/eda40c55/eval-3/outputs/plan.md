# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint to allow filtering packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 4 -- Understand the Code

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. The repo structure shows a `CONVENTIONS.md` file exists -- read it and extract any CI check commands and code generation commands for use during verification (Step 9).

### Convention Conformance Analysis

Inspect sibling files to establish patterns before implementing:

1. **Sibling endpoint file:** `modules/fundamental/src/advisory/endpoints/list.rs` -- the advisory list endpoint already implements a `severity` query parameter filter. This is the primary pattern to follow. Use `get_symbols_overview` (via `mcp__serena_backend__get_symbols_overview`) to inspect the file structure, then `find_symbol` with `include_body=true` on the query struct and handler function.

2. **Sibling endpoint file:** `modules/fundamental/src/sbom/endpoints/list.rs` -- the SBOM list endpoint for a second reference on how list endpoints are structured in this codebase.

3. **Query helpers:** `common/src/db/query.rs` -- inspect `apply_filter` function signature and usage to understand how it handles comma-separated values and generates SQL IN clauses.

4. **Entity file:** `entity/src/package_license.rs` -- inspect the SeaORM entity definition for the package-license join table to understand column names and relations.

5. **Current package endpoint:** `modules/fundamental/src/package/endpoints/list.rs` -- inspect the existing query struct and handler to understand the current parameter set.

6. **Package service:** `modules/fundamental/src/package/service/mod.rs` -- inspect `PackageService::list` method signature and implementation.

**Expected discovered conventions (based on repo structure and key conventions):**
- **Framework:** Axum for HTTP, SeaORM for database
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Naming:** Service methods follow `verb_noun` pattern
- **Module pattern:** Each domain follows `model/ + service/ + endpoints/` structure

### Test Convention Analysis

Inspect sibling test files to establish test patterns:

1. **Sibling test file:** `tests/api/advisory.rs` -- advisory endpoint integration tests; inspect assertion style, response validation, error case coverage, test naming, and test setup.
2. **Sibling test file:** `tests/api/sbom.rs` -- SBOM endpoint integration tests for a second reference.

**Expected discovered test conventions:**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and key fields on items
- **Error cases:** Endpoint tests include status code assertions for error conditions (e.g., `StatusCode::BAD_REQUEST`)
- **Test naming:** `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Setup:** Tests hit a real PostgreSQL test database

### Documentation File Identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (likely documents `GET /api/v2/package`)
- `CONVENTIONS.md` at repository root

### Referencing Symbols Check

Use `find_referencing_symbols` on `PackageService::list` to identify all callers and ensure that adding an optional `license` filter parameter with a default of `None` will not break existing call sites.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add `license` query parameter extraction and pass it to the service layer.

**Changes:**

a. **Add `license` field to the Query struct:**
   Follow the pattern from `advisory/endpoints/list.rs` where the `severity` field is defined as an optional query parameter. Add:
   ```rust
   /// Optional license filter. Supports comma-separated SPDX identifiers.
   pub license: Option<String>,
   ```

b. **Extract and pass `license` to the service layer:**
   In the handler function, extract `query.license` and pass it to `PackageService::list()`. This follows the same pattern as how `severity` is extracted and passed in the advisory list handler.

c. **Add input validation:**
   Validate the license parameter before passing to the service layer. If the value is present but empty (e.g., `?license=`), return a `400 Bad Request` using `AppError`. This satisfies the acceptance criterion for invalid license values.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering logic to the `PackageService::list` method.

**Changes:**

a. **Add `license` parameter to the `list` method signature:**
   Add an `Option<String>` parameter for the license filter. Use a default of `None` so existing callers (identified via `find_referencing_symbols`) are not broken -- update all existing callers to pass `None` for the new parameter if needed, or restructure as an options struct if the advisory service uses that pattern.

b. **Implement the license filter using `apply_filter` from `common/src/db/query.rs`:**
   When `license` is `Some(value)`:
   1. Call `apply_filter` with the license string -- this handles parsing comma-separated values and generating the appropriate SQL `IN` clause.
   2. Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers.
   3. The join uses SeaORM's `JoinType::InnerJoin` on the `package_license` table, matching `package.id = package_license.package_id` and filtering on `package_license.license` using the values parsed by `apply_filter`.

c. **When `license` is `None`:**
   Skip the join and filter entirely -- return all packages as before (no regression).

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Changes:**

a. **Register the test module:** Add `mod package_license_filter;` to `tests/api/mod.rs` (if a mod.rs exists) or ensure the test is picked up by the test harness via `Cargo.toml` configuration.

b. **Test functions to implement** (following sibling test conventions from `tests/api/advisory.rs`):

   - `test_list_packages_filter_single_license`:
     ```
     /// Verifies that filtering by a single license returns only packages with that license.
     ```
     - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
     - When: `GET /api/v2/package?license=MIT`
     - Then: assert status 200, assert all returned items have `license == "MIT"`, assert specific expected package names are present (value-based assertions, not just count)

   - `test_list_packages_filter_comma_separated_licenses`:
     ```
     /// Verifies that filtering by comma-separated licenses returns packages matching any listed license.
     ```
     - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
     - When: `GET /api/v2/package?license=MIT,Apache-2.0`
     - Then: assert status 200, assert returned items have license in {"MIT", "Apache-2.0"}, assert GPL-3.0 packages are excluded, assert specific expected packages are present

   - `test_list_packages_no_license_filter`:
     ```
     /// Verifies that omitting the license parameter returns all packages (no regression).
     ```
     - Given: seed database with packages having various licenses
     - When: `GET /api/v2/package` (no license parameter)
     - Then: assert status 200, assert all seeded packages are returned, assert response shape is `PaginatedResults<PackageSummary>`

   - `test_list_packages_invalid_license`:
     ```
     /// Verifies that an invalid license value returns 400 Bad Request.
     ```
     - Given: standard database state
     - When: `GET /api/v2/package?license=` (empty value)
     - Then: assert status 400 (Bad Request)

c. **Test patterns to follow:**
   - Use `assert_eq!(resp.status(), StatusCode::OK)` / `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` per sibling convention
   - Deserialize response body as `PaginatedResults<PackageSummary>` for validation
   - Assert on specific field values (license, package name) not just collection lengths
   - Add `// Given`, `// When`, `// Then` section comments in each test body
   - Add `///` doc comments on every test function

---

## Step 8 -- Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | `test_list_packages_filter_comma_separated_licenses` |
| `GET /api/v2/package` without license returns all packages | `test_list_packages_no_license_filter` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | All tests deserialize to `PaginatedResults<PackageSummary>` |
| Invalid license values return 400 | `test_list_packages_invalid_license` |

---

## Step 9 -- Self-Verification Plan

### Scope Containment
- Run `git diff --name-only` and confirm only these files are modified/created:
  - `modules/fundamental/src/package/endpoints/list.rs` (modified)
  - `modules/fundamental/src/package/service/mod.rs` (modified)
  - `tests/api/package_license_filter.rs` (created)
- If any additional files were modified (e.g., updating existing callers of `PackageService::list` to pass the new `None` parameter), flag them as out-of-scope modifications requiring approval -- though these would be necessary cascading changes.

### Untracked File Check
- Run `git status --short` and check for `??` entries in directories containing modified files.
- Flag `tests/api/package_license_filter.rs` as a new file to stage.

### Sensitive-Pattern Check
- Search staged diff for secrets/credentials patterns -- none expected.

### Documentation Currency
- Check `docs/api.md` for documentation of the `GET /api/v2/package` endpoint -- if it exists and documents query parameters, add the `license` parameter to the documentation.
- Check `README.md` for any API parameter documentation that needs updating.

### Duplication Check
- Search the codebase for any existing license filtering logic to ensure we are not duplicating code.
- Confirm that `apply_filter` is being reused rather than reimplemented.

### Data-Flow Trace
- `GET /api/v2/package?license=MIT` -> extract `license` from query params (endpoint list.rs) -> pass to `PackageService::list` (service/mod.rs) -> `apply_filter` parses comma values (query.rs) -> JOIN on `package_license` table (entity) -> filter by license column -> return `PaginatedResults<PackageSummary>` -- **COMPLETE**

### Contract & Sibling Parity
- Verify the handler returns `Result<T, AppError>` matching sibling handlers.
- Verify `PackageService::list` error handling matches `AdvisoryService::list` patterns.
- Verify the new filter follows the same `apply_filter` pattern as the severity filter in advisory.

### CI Checks
- Run all CI check commands extracted from `CONVENTIONS.md` (formatting, linting, compilation, tests).
- Run `cargo test` to verify all tests pass.
- Hard stop on any non-zero exit.

---

## Step 10 -- Commit and Push Plan

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that supports
single-value and comma-separated SPDX identifier filtering. Reuses the
apply_filter helper from common/src/db/query.rs and joins through the existing
package_license entity.

Implements TC-9203"
```

Then:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

---

## Step 11 -- Jira Update Plan

1. Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format.
2. Add a Jira comment with: PR link, summary of changes, confirmation that all acceptance criteria are met, note that existing code was reused (apply_filter, advisory pattern, package_license entity).
3. Transition TC-9203 to **In Review**.
