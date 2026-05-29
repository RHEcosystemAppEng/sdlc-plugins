# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting
both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Target Repository

trustify-backend (Serena instance: `serena_backend`)

## Target Branch

main

## Branch Name

TC-9203

## Step 0 — Project Configuration Validation

The project CLAUDE.md contains all required sections:
- Repository Registry: present, lists `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present, includes Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention and configured `serena_backend` instance

Validation passes. Proceed with implementation.

## Step 1 — Task Parsing

Parsed sections from the Jira task description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add `license` query parameter to `GET /api/v2/package` for filtering by SPDX identifier; support single and comma-separated multi-value filtering
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs`
  - `modules/fundamental/src/package/service/mod.rs`
- **Files to Create**:
  - `tests/api/package_license_filter.rs`
- **API Changes**: `GET /api/v2/package?license=MIT` and `GET /api/v2/package?license=MIT,Apache-2.0`
- **Implementation Notes**: Follow advisory severity filter pattern, reuse `apply_filter`, use `package_license` entity
- **Acceptance Criteria**: 5 criteria (see task)
- **Test Requirements**: 4 test cases (see task)
- **Target PR**: none (default flow — new branch and PR)
- **Bookend Type**: none (standard implementation)
- **Dependencies**: none

No missing sections. Proceed.

## Step 2 — Dependency Verification

No dependencies listed. Proceed.

## Step 3 — Transition and Assign

Would transition TC-9203 to In Progress and assign to current user via Jira API.

## Step 4 — Understand the Code

### Code inspection plan

Using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reference pattern):
   - `get_symbols_overview` to see the Query struct and handler function structure
   - `find_symbol` on the Query struct to see how the `severity` optional field is declared
   - `find_symbol` on the list handler to see how it calls `apply_filter` with the severity field

2. **`common/src/db/query.rs`** (reuse target):
   - `get_symbols_overview` to see all exported functions
   - `find_symbol` with `include_body=true` on `apply_filter` to understand its signature and behavior (comma-separated parsing, SQL IN clause generation)

3. **`entity/src/package_license.rs`** (reuse target):
   - `get_symbols_overview` to see the entity struct and its fields/relations
   - Understand the join relationship between `package` and `package_license` tables

4. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify):
   - `get_symbols_overview` to see the current Query struct and handler
   - `find_symbol` on the list handler to understand current filter logic

5. **`modules/fundamental/src/package/service/mod.rs`** (file to modify):
   - `get_symbols_overview` to see PackageService methods
   - `find_symbol` on the `list` method to understand current query building

6. **Sibling analysis** for convention conformance:
   - Compare `modules/fundamental/src/advisory/endpoints/list.rs` (advisory list endpoint) and `modules/fundamental/src/sbom/endpoints/list.rs` (SBOM list endpoint) to confirm consistent patterns for query structs, filter application, and handler signatures

7. **Test sibling analysis**:
   - `get_symbols_overview` on `tests/api/advisory.rs` and `tests/api/sbom.rs` to identify test patterns, assertion styles, naming conventions, and test setup/teardown

8. **Backward compatibility**:
   - `find_referencing_symbols` on the PackageService `list` method to identify all callers and ensure the new optional parameter does not break them

9. **Documentation files**:
   - Check for `CONVENTIONS.md` at repository root
   - Check `docs/api.md` for API documentation that may need updating

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root and extract CI check commands if present.

### Discovered conventions (expected from sibling analysis)

- **Query struct pattern**: List endpoints define a `Query` struct with `#[derive(Deserialize)]` containing optional filter fields; Axum extracts this from query parameters automatically
- **Filter application**: Handlers call `apply_filter(&query.field_name, &mut condition)` for each optional filter field; `apply_filter` handles None (skip), single value, and comma-separated multi-value cases
- **Error handling**: All handlers return `Result<Json<PaginatedResults<T>>, AppError>` with `.context()` wrapping on service calls
- **Service method pattern**: Service list methods accept a query/filter struct parameter and build a SeaORM `Select` with optional conditions
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list_packages`, `fetch_advisory`)

### Discovered test conventions (expected from sibling test analysis)

- **Assertion style**: Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by JSON body deserialization into the response type
- **Response validation**: List tests validate `total_count`, `items.len()`, and assert on specific item field values (not just counts)
- **Error cases**: Tests include 400/404 status code assertions for invalid input
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests seed the database with known test data before making requests

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing `Query` struct, following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.

   ```rust
   #[derive(Deserialize)]
   pub struct Query {
       // ... existing fields ...
       /// Optional SPDX license identifier filter. Supports comma-separated values.
       pub license: Option<String>,
   }
   ```

2. **Apply the license filter in the handler**: In the list handler function, add a call to `apply_filter` from `common/src/db/query.rs`, passing `&query.license` and the filter condition builder. This reuses the existing `apply_filter` function which already handles:
   - `None` values (skip filter entirely)
   - Single values (SQL `= ?` clause)
   - Comma-separated values (SQL `IN (?, ?, ...)` clause)

   **Reuse**: Call `apply_filter(&query.license, &mut select, package_license::Column::License)` following the exact same pattern used for the severity filter in the advisory list endpoint.

3. **Add the JOIN**: Add a `.join()` call to join the `package` table with the `package_license` table using the `package_license` entity from `entity/src/package_license.rs`. This join is only needed when the license filter is present, so wrap it in an `if query.license.is_some()` conditional to avoid unnecessary joins on unfiltered queries.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Extend the list method signature**: Add an optional `license: Option<String>` parameter to the PackageService `list` method (or incorporate it into the existing filter/query struct if one is used).

2. **Build the filter condition**: Use `apply_filter` from `common/src/db/query.rs` to build the SQL condition for the license filter. The `apply_filter` function handles comma parsing and IN clause generation, so no custom parsing logic is needed.

3. **Add the entity JOIN**: When the license filter is present, join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their declared license. Use SeaORM's `.join()` method with the relation defined in the `package_license` entity.

4. **Apply DISTINCT**: Since the join through `package_license` can produce duplicate package rows (a package may have multiple licenses matching the filter), apply `.distinct()` to the query to ensure each package appears only once in the results.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create a new integration test file following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Test functions:**

1. **`test_list_packages_filter_single_license`**: Seed packages with known licenses (MIT, Apache-2.0, GPL-3.0). Request `GET /api/v2/package?license=MIT`. Assert response status is 200, assert that all returned items have license MIT, assert specific package names/identifiers in the results.

2. **`test_list_packages_filter_multi_license`**: Seed packages with known licenses. Request `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response status is 200, assert returned items have either MIT or Apache-2.0 license, assert correct count and specific items.

3. **`test_list_packages_no_license_filter`**: Seed packages with various licenses. Request `GET /api/v2/package` (no license param). Assert response status is 200, assert all seeded packages are returned (no regression from adding the filter capability).

4. **`test_list_packages_invalid_license`**: Request `GET /api/v2/package?license=NOT-A-VALID-SPDX`. Assert response status is 400 Bad Request.

Each test function will have:
- A `///` doc comment explaining what it verifies
- Given/When/Then section comments inside the test body
- Value-based assertions on specific package fields, not just length checks

### Additional integration points

- **Module registration**: If `tests/api/` uses a `mod.rs` or the test binary's `main.rs`/`lib.rs` to register test modules, add `mod package_license_filter;` to that file.
- **Import `apply_filter`**: Add `use common::db::query::apply_filter;` (or equivalent path) in the endpoint and service files.
- **Import `package_license` entity**: Add `use entity::package_license;` in the service file for the JOIN.

### Documentation impact

- If `docs/api.md` documents the `GET /api/v2/package` endpoint, add the new `license` query parameter to that documentation.
- The response shape (`PaginatedResults<PackageSummary>`) does not change, so no response documentation updates are needed.

## Step 7 — Write Tests

Implement the four test functions described above in `tests/api/package_license_filter.rs`. Run `cargo test` to verify all pass.

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | Verified by `test_list_packages_filter_single_license` |
| GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | Verified by `test_list_packages_filter_multi_license` |
| GET /api/v2/package without license returns all packages | Verified by `test_list_packages_no_license_filter` |
| Response shape PaginatedResults<PackageSummary> unchanged | No structural changes to response type; verified by all tests deserializing successfully |
| Invalid license values return 400 | Verified by `test_list_packages_invalid_license` |

## Step 9 — Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `modules/fundamental/src/package/endpoints/list.rs` (in Files to Modify)
  - `modules/fundamental/src/package/service/mod.rs` (in Files to Modify)
  - `tests/api/package_license_filter.rs` (in Files to Create)
  - Possibly `tests/api/mod.rs` or equivalent for module registration (out-of-scope — would ask user to approve)

### Data-flow trace
- `GET /api/v2/package?license=MIT` -> Axum extracts Query struct with `license: Some("MIT")` -> handler calls `apply_filter` -> service builds SeaORM query with JOIN on `package_license` and WHERE condition -> database returns filtered rows -> service maps to `PackageSummary` -> handler wraps in `PaginatedResults` -> JSON response. **COMPLETE**.

### Duplication check
- No new parsing or filtering logic written; `apply_filter` from `common/src/db/query.rs` handles all comma-separated multi-value parsing. No duplication.

## Step 10 — Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" \
  -m "feat(api): add license filter to GET /api/v2/package

Add optional 'license' query parameter supporting single and
comma-separated SPDX identifiers. Reuses apply_filter from
common/src/db/query.rs and joins through the package_license entity.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary
- Add \`license\` query parameter to \`GET /api/v2/package\`
- Support single-value and comma-separated multi-value SPDX filtering
- Reuse \`apply_filter\` and \`package_license\` entity — no new filtering logic

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)"
```

## Step 11 — Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL using ADF inlineCard format
- Add comment summarizing changes and linking PR
- Transition TC-9203 to In Review
