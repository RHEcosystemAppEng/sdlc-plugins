# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint to allow
consumers to filter packages by their declared SPDX license identifier. Support both
single-value and comma-separated multi-value filtering.

## Target Repository

trustify-backend

## Target Branch

main

## Branch Name

TC-9203

## Step-by-Step Plan

### Step 1 — Understand the Code (Skill Step 4)

Before modifying any code, inspect the following:

1. **Read `modules/fundamental/src/advisory/endpoints/list.rs`** to understand the
   severity filter pattern (the structural reference for this task). Specifically:
   - Identify the `Query` struct (or equivalent) that extracts query parameters
   - See how the optional `severity` field is declared
   - See how it is passed to the service layer

2. **Read `common/src/db/query.rs`** to understand `apply_filter`:
   - How it parses comma-separated values
   - How it generates SQL `IN` clauses
   - What input type it expects (string, slice, etc.)

3. **Read `entity/src/package_license.rs`** to understand:
   - The SeaORM entity structure for the package-license join table
   - Column names and relationships
   - How to join through this table

4. **Read `modules/fundamental/src/package/endpoints/list.rs`** (current state):
   - Current `Query` struct fields
   - How the handler function is structured
   - How it calls the service layer

5. **Read `modules/fundamental/src/package/service/mod.rs`** (current state):
   - The `list` method signature on `PackageService`
   - How existing filtering and pagination work
   - How the database query is built

6. **Read sibling test files** (`tests/api/advisory.rs`, `tests/api/sbom.rs`):
   - Assertion patterns (likely `assert_eq!(resp.status(), StatusCode::OK)`)
   - Response body deserialization approach
   - Test naming conventions
   - Test setup and database seeding patterns

7. **Check for `CONVENTIONS.md`** at the repository root for CI commands and coding
   conventions.

8. **Identify documentation files** (README, API docs) that may need updating.

### Step 2 — Modify `modules/fundamental/src/package/endpoints/list.rs`

**Type of change:** Modify existing file

**Changes:**

1. **Add `license` field to the Query struct:**
   Following the pattern from the advisory list endpoint's severity filter, add an
   optional `license` field to the `Query` struct used for parameter extraction:

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional SPDX license identifier filter. Supports comma-separated values.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer:**
   In the handler function, extract `query.license` and pass it to
   `PackageService::list()` as an additional parameter. Follow the same pattern
   used by the advisory endpoint when passing the severity filter.

3. **Validate the license parameter:**
   Add validation for the license parameter to return 400 Bad Request for invalid
   values (e.g., empty strings after splitting, values with invalid characters for
   SPDX identifiers).

### Step 3 — Modify `modules/fundamental/src/package/service/mod.rs`

**Type of change:** Modify existing file

**Changes:**

1. **Add `license` parameter to the `list` method:**
   Extend the `PackageService::list()` method signature to accept an optional license
   filter parameter:

   ```rust
   pub async fn list(
       &self,
       // ... existing parameters
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Build the license filter query using `apply_filter`:**
   When the `license` parameter is `Some`, use `common::db::query::apply_filter` to:
   - Parse comma-separated license values
   - Generate an SQL `IN` clause

3. **Join through the `package_license` entity:**
   Use the SeaORM entity from `entity::package_license` to join the `package` table
   to the `package_license` table, then apply the license filter on the license column.
   This follows SeaORM's relation-based join pattern rather than raw SQL.

4. **Ensure no regression when license is None:**
   When no license filter is provided, skip the join and filter entirely, preserving
   the existing behavior and query performance.

### Step 4 — Create `tests/api/package_license_filter.rs`

**Type of change:** Create new file

**Changes:**

Create integration tests following the patterns observed in sibling test files
(`tests/api/advisory.rs`, `tests/api/sbom.rs`):

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only matching packages.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status is 200, response body contains only MIT-licensed packages,
     assert on specific package names/identifiers (not just count)

2. **`test_list_packages_filter_multi_license`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status is 200, response body contains MIT and Apache-2.0 packages
     but not GPL-3.0, assert on specific package identifiers

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license filter returns all packages unchanged.`
   - Given: seed database with packages having various licenses
   - When: `GET /api/v2/package`
   - Then: response status is 200, response body contains all seeded packages,
     response shape is `PaginatedResults<PackageSummary>` unchanged

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: standard test database state
   - When: `GET /api/v2/package?license=` (empty value)
   - Then: response status is 400

All tests will include given-when-then section comments for navigability.

### Step 5 — Register the test module

**Type of change:** Modify existing file (likely `tests/api/mod.rs` or `tests/Cargo.toml`)

Add `mod package_license_filter;` to the test module registration so the new test
file is compiled and run. Follow the pattern used by existing test registrations
(e.g., `mod sbom;`, `mod advisory;`, `mod search;`).

### Step 6 — Verify and Commit

1. Run `cargo test` to verify all tests pass (existing and new).
2. Run any CI check commands from `CONVENTIONS.md`.
3. Verify scope containment — only the files listed above should be modified.
4. Check for untracked files that need staging.
5. Run the sensitive-pattern check on the staged diff.
6. Commit with message:
   ```
   feat(api): add license filter to package list endpoint

   Add optional `license` query parameter to GET /api/v2/package.
   Supports single-value and comma-separated multi-value filtering
   using SPDX identifiers. Reuses apply_filter from common/db/query.rs
   and joins through the existing package_license entity.

   Implements TC-9203
   ```
7. Push branch and create PR targeting `main`.

## Files Summary

| File | Action | Description |
|---|---|---|
| `modules/fundamental/src/package/endpoints/list.rs` | Modify | Add `license` field to Query struct, pass to service, add validation |
| `modules/fundamental/src/package/service/mod.rs` | Modify | Add `license` parameter to list method, build filter with `apply_filter`, join through `package_license` entity |
| `tests/api/package_license_filter.rs` | Create | Integration tests for single, multi, absent, and invalid license filters |
| Test module registration file | Modify | Register `package_license_filter` test module |

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` request received
  -> Axum extracts `Query` struct with `license: Some("MIT")` ✓
  -> Handler passes `license` to `PackageService::list()` ✓
  -> Service calls `apply_filter` to parse comma-separated values ✓
  -> Service joins `package` with `package_license` via SeaORM relation ✓
  -> Service applies `WHERE license_id IN (...)` filter ✓
  -> Query returns filtered results ✓
  -> Handler wraps in `PaginatedResults<PackageSummary>` and returns 200 ✓
  -> **COMPLETE**

- `GET /api/v2/package` (no license param)
  -> `license: None` -> skip join and filter -> return all packages ✓
  -> **COMPLETE** (no regression)
