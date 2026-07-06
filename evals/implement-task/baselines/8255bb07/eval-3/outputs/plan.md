# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint
that filters packages by their declared SPDX license identifier. Support both
single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`)
filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID, and custom fields
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured for rust-analyzer

Validation passes. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9203:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a `license` query parameter to `GET /api/v2/package` for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering (exact match).
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
  - `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method
- **Files to Create**:
  - `tests/api/package_license_filter.rs` -- integration tests for the license filter
- **API Changes**:
  - `GET /api/v2/package?license=MIT` -- MODIFY: add optional `license` query parameter
  - `GET /api/v2/package?license=MIT,Apache-2.0` -- MODIFY: support comma-separated license values
- **Implementation Notes**: Follow advisory severity filter pattern; use `apply_filter` from `common/src/db/query.rs`; join through `package_license` entity
- **Reuse Candidates**: 3 candidates (detailed in reuse-analysis.md)
- **Acceptance Criteria**: 5 items (single filter, multi filter, no filter regression, unchanged response shape, invalid license 400)
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Target PR**: None (default flow)
- **Bookend Type**: None (default flow)

GitHub Issue custom field: `customfield_10747` -- would check the fetched issue for a GitHub issue URL. Skipped in this eval (no Jira access).

Issue webUrl: `https://redhat.atlassian.net/browse/TC-9203` (would be extracted from Jira API response).

## Step 1.5 -- Verify Description Integrity

Would fetch comments via `jira.get_issue_comments(TC-9203)`, locate the most recent comment starting with `[sdlc-workflow] Description digest:`, extract the tagged digest, compute the current digest with `python3 scripts/sha256-digest.py`, and compare. Skipped in this eval (no Jira access).

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9203, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9203)` to "In Progress"

Skipped in this eval (no Jira access).

## Step 4 -- Understand the Code

### Code inspection plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **Inspect files to modify:**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/list.rs` -- understand the current list handler: its Query struct, route registration, and handler function signature
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/service/mod.rs` -- understand `PackageService::list()` method signature and return type

2. **Read reuse candidates:**
   - `mcp__serena_backend__find_symbol` on `apply_filter` in `common/src/db/query.rs` with `include_body=true` -- understand the filter helper's signature, how it parses comma-separated values, and how it generates the SQL IN clause
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- understand the advisory Query struct with the `severity` optional field as a structural template
   - `mcp__serena_backend__get_symbols_overview` on `entity/src/package_license.rs` -- understand the SeaORM entity structure, its columns, and its relations

3. **Check backward compatibility:**
   - `mcp__serena_backend__find_referencing_symbols` on the package Query struct to identify all callers
   - `mcp__serena_backend__find_referencing_symbols` on `PackageService::list()` to ensure the added parameter is optional and backward-compatible

4. **Convention conformance analysis (siblings):**
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/list.rs` -- sibling list endpoint
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling list endpoint with filter (primary template)
   - Compare: Query struct pattern, handler return types, error handling, pagination usage

5. **Test convention analysis:**
   - `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` -- sibling endpoint test file
   - `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` -- sibling endpoint test file
   - Examine assertion patterns, test naming, setup/teardown, fixture creation

6. **Documentation file identification:**
   - Check for `CONVENTIONS.md` at repository root
   - Check `docs/api.md` for API documentation that might reference `/api/v2/package`
   - Check `README.md` for any endpoint references

### CONVENTIONS.md lookup

Would check `./CONVENTIONS.md` in the trustify-backend repo root. If present, read it and extract CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`) for use in Step 9.

### Discovered conventions (expected from sibling analysis)

Based on the repository structure and conventions:

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query pattern:** List endpoints use a `Query` struct with `#[derive(Deserialize)]` for query parameters, with optional fields for filters
- **Filter pattern:** Filters use `common/src/db/query.rs::apply_filter` for comma-separated multi-value handling
- **Service layer:** Service methods take filter parameters as `Option<String>` and pass them to query builders
- **Entity joins:** SeaORM entities provide relation definitions used for `.join()` in query builders
- **Route registration:** Each endpoint module's `mod.rs` registers routes; `server/main.rs` mounts all modules
- **Framework:** Axum for HTTP, SeaORM for database

### Discovered test conventions (expected from sibling analysis)

- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into `PaginatedResults<T>`
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases:** Include tests for invalid input returning `StatusCode::BAD_REQUEST`
- **Test naming:** `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_by_license`)
- **Test database:** Integration tests hit a real PostgreSQL test database
- **No parameterized tests observed** in sibling files -- use individual test functions

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the Query struct:**
   Add an optional `license` field to the existing query parameter struct, following the same pattern as the advisory endpoint's `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`:
   ```rust
   /// Query parameters for listing packages.
   #[derive(Debug, Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (pagination, sorting, search) ...

       /// Optional license filter. Supports single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer:**
   In the handler function, pass `query.license` to `PackageService::list()`:
   ```rust
   let result = service
       .list(
           &db,
           // ... existing parameters ...
           query.license.as_deref(),
       )
       .await
       .context("Failed to list packages")?;
   ```

   The response type `PaginatedResults<PackageSummary>` remains unchanged -- only the input accepts a new optional parameter.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add `license` parameter to the `list` method signature:**
   ```rust
   pub async fn list(
       &self,
       db: &DatabaseConnection,
       // ... existing parameters ...
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Add license filter logic using `apply_filter` and the `package_license` entity:**
   - Import `apply_filter` from `common/src/db/query.rs` -- reuse this existing function directly for comma-separated multi-value query parameter parsing and SQL IN clause generation. Do NOT create a new parsing or filtering utility.
   - Import the `package_license` entity from `entity/src/package_license.rs` -- use this existing entity for the JOIN query rather than writing raw SQL.
   - When `license` is `Some`, join the `package_license` table and apply the filter:

   ```rust
   use common::db::query::apply_filter;
   use entity::package_license;

   // Inside the list method, after building the base query:
   if let Some(license_filter) = license {
       // Join through the package_license entity (reusing entity/src/package_license.rs)
       query = query.join(
           JoinType::InnerJoin,
           package::Relation::PackageLicense.def(),
       );
       // Apply the comma-separated filter using the shared helper
       // (reusing common/src/db/query.rs::apply_filter)
       query = apply_filter(query, package_license::Column::License, license_filter)?;
   }
   ```

   The `apply_filter` function handles:
   - Splitting comma-separated values (e.g., "MIT,Apache-2.0" becomes ["MIT", "Apache-2.0"])
   - Generating the SQL IN clause (e.g., `WHERE license IN ('MIT', 'Apache-2.0')`)
   - Returning a 400 Bad Request error via AppError for invalid values

### File 3 (new): `tests/api/package_license_filter.rs`

**Create integration tests following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:**

Test cases:
1. `test_list_packages_single_license_filter` -- verify `?license=MIT` returns only MIT-licensed packages (assert on specific package identifiers, not just count)
2. `test_list_packages_multi_license_filter` -- verify `?license=MIT,Apache-2.0` returns packages matching either license
3. `test_list_packages_no_license_filter` -- verify omitting the parameter returns all packages (regression check)
4. `test_list_packages_invalid_license_returns_400` -- verify invalid license value returns `StatusCode::BAD_REQUEST`

Each test function gets a `///` doc comment explaining what it verifies. Non-trivial tests use `// Given`, `// When`, `// Then` section comments.

Register the test module in `tests/api/mod.rs` (or equivalent).

## Step 7 -- Write Tests

Tests are defined in Step 6, File 3. Would run:
```
cargo test --test package_license_filter
```
Fix any compilation or assertion failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/package?license=MIT returns only MIT packages | Verified by `test_list_packages_single_license_filter` |
| 2 | GET /api/v2/package?license=MIT,Apache-2.0 returns packages matching either | Verified by `test_list_packages_multi_license_filter` |
| 3 | GET /api/v2/package without license returns all packages | Verified by `test_list_packages_no_license_filter` |
| 4 | Response shape PaginatedResults<PackageSummary> unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` -- any shape change would break deserialization |
| 5 | Invalid license values return 400 Bad Request | Verified by `test_list_packages_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment

Expected `git diff --name-only` output:
- `modules/fundamental/src/package/endpoints/list.rs` -- in Files to Modify
- `modules/fundamental/src/package/service/mod.rs` -- in Files to Modify
- `tests/api/package_license_filter.rs` -- in Files to Create

Potential out-of-scope file (requires user approval):
- `tests/api/mod.rs` (or equivalent) -- may need module declaration for the new test file

### Duplication check

Search for existing license-filtering logic in the codebase to ensure no duplication:
- Verify that `apply_filter` from `common/src/db/query.rs` is reused directly -- no new parsing or filtering utility functions created
- Confirm no other module already implements license filtering

### Data-flow trace

```
GET /api/v2/package?license=MIT,Apache-2.0
  -> list.rs: extract `license` from Query struct
  -> service/mod.rs: receive license Option<&str>
  -> apply_filter (query.rs): parse "MIT,Apache-2.0" -> ["MIT", "Apache-2.0"], generate IN clause
  -> SeaORM JOIN via package_license entity: filter packages by license match
  -> Return filtered PaginatedResults<PackageSummary>
  -> HTTP response (unchanged shape)
```

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/package/endpoints/list.rs \
      modules/fundamental/src/package/service/mod.rs \
      tests/api/package_license_filter.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
filters packages by SPDX license identifier. Supports single-value
and comma-separated multi-value filtering using the existing
apply_filter helper. Joins through the package_license entity for
filtering while keeping the response shape unchanged.

Implements TC-9203"
```

```bash
git push -u origin TC-9203

gh pr create --base main \
  --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary

- Add optional \`license\` query parameter to \`GET /api/v2/package\`
- Support single-value (\`?license=MIT\`) and comma-separated (\`?license=MIT,Apache-2.0\`) filtering
- Reuse \`apply_filter\` from \`common/src/db/query.rs\` and join through \`package_license\` entity
- Add integration tests for single filter, multi filter, no filter, and invalid input cases

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)

## Test Plan

- [x] Single license filter returns only matching packages
- [x] Comma-separated license filter returns packages matching any listed license
- [x] No license filter returns all packages (no regression)
- [x] Invalid license value returns 400 Bad Request
- [x] Response shape PaginatedResults<PackageSummary> remains unchanged"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format
2. **Add comment** to TC-9203 with PR link, summary of changes, and note that no deviations from plan occurred
3. **Transition** TC-9203 to "In Review"
