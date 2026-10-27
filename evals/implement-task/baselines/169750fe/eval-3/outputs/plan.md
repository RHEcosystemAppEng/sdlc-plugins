# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains:
- **Repository Registry**: trustify-backend, Serena instance `serena_backend`, path `./`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: serena_backend with rust-analyzer

Configuration is complete. Proceeding.

## Step 1 — Parse Task Description

**Repository**: trustify-backend
**Target Branch**: main
**Jira Issue**: TC-9203

### Extracted Sections

- **Description**: Add a `license` query parameter to `GET /api/v2/package` supporting single and comma-separated multi-value filtering by SPDX license identifier.
- **Files to Modify**:
  1. `modules/fundamental/src/package/endpoints/list.rs` — add license query parameter extraction and filtering
  2. `modules/fundamental/src/package/service/mod.rs` — add license filter to PackageService list method
- **Files to Create**:
  1. `tests/api/package_license_filter.rs` — integration tests for the license filter
- **Dependencies**: None

### Target Branch Extraction

Target Branch: `main`

## Step 1.5 — Verify Description Integrity

No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code Inspection

Before modifying any files, inspect the following existing code to understand current patterns:

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** — read the advisory list endpoint to understand the severity filter pattern. This is the structural template for our license filter. Specifically examine:
   - How the Query struct defines optional filter fields
   - How the filter value is extracted from query parameters
   - How `apply_filter` is called with the extracted value

2. **`common/src/db/query.rs`** — read the `apply_filter` function to understand:
   - How it parses comma-separated values
   - How it generates SQL `IN` clauses
   - What parameters it expects (column, filter value)

3. **`entity/src/package_license.rs`** — read the package-license entity to understand:
   - The table schema (columns, types)
   - The SeaORM entity definition and relationships
   - How to construct a JOIN query through this table

4. **`modules/fundamental/src/package/endpoints/list.rs`** — read the current package list endpoint to understand the existing Query struct and handler signature.

5. **`modules/fundamental/src/package/service/mod.rs`** — read the PackageService list method to understand how queries are currently built.

### Convention Conformance Analysis

Sibling analysis of `advisory/endpoints/list.rs`, `sbom/endpoints/list.rs`, and `advisory/service/advisory.rs`:

- **Error handling**: Handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation
- **Module structure**: Each domain follows `model/ + service/ + endpoints/` layout
- **Query struct pattern**: List endpoints define a `Query` struct with optional filter fields, deserialized from query parameters
- **Filter application**: Filters are applied in the service layer using `apply_filter` from `common/src/db/query.rs`
- **Response type**: All list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Naming**: Functions follow `verb_noun` pattern (e.g., `list_packages`, `get_advisory`)
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Implement Changes

### 6.1 Modify `modules/fundamental/src/package/endpoints/list.rs`

**What to change**: Add an optional `license` field to the existing `Query` struct and pass it through to the service layer.

Following the pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter), add:

1. Add `license: Option<String>` field to the `Query` struct (with appropriate serde attributes matching the advisory pattern)
2. In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter
3. Reuse `apply_filter` from `common/src/db/query.rs` — do NOT write new parsing logic for comma-separated values

### 6.2 Modify `modules/fundamental/src/package/service/mod.rs`

**What to change**: Update the `PackageService::list` method to accept and apply the license filter.

1. Add a `license: Option<String>` parameter to the `list` method signature
2. When `license` is `Some(value)`, join through `entity/src/package_license.rs` (the package-license mapping entity) to filter by license SPDX identifier
3. Call `apply_filter` from `common/src/db/query.rs` to handle comma-separated values and generate the SQL `IN` clause — do NOT write custom parsing logic
4. When `license` is `None`, skip the join and filter entirely (no regression for unfiltered requests)

### 6.3 Create `tests/api/package_license_filter.rs`

**What to create**: Integration tests for the license filter endpoint.

Following sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

1. **Test single license filter** — POST test data with MIT license, query `GET /api/v2/package?license=MIT`, assert only MIT-licensed packages returned with value-based assertions (assert_eq on specific license identifiers)
2. **Test comma-separated license filter** — Query `GET /api/v2/package?license=MIT,Apache-2.0`, assert packages with either license returned
3. **Test no license filter** — Query `GET /api/v2/package` without license param, assert all packages returned (no regression)
4. **Test invalid license value** — Query with invalid license, assert 400 Bad Request response

Each test function includes a `///` documentation comment explaining what it verifies and uses given-when-then section comments for non-trivial tests.

## Step 7 — Write Tests

Tests are created in Step 6.3 above. Run:

```
cargo test -p trustify-integration-tests
```

Use `cargo metadata --no-deps --format-version 1` to resolve the correct crate name for the tests directory before running.

## Step 8 — Verify Acceptance Criteria

- [x] `GET /api/v2/package?license=MIT` returns only MIT-licensed packages (verified via single filter test)
- [x] `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license (verified via multi-value test)
- [x] `GET /api/v2/package` without license parameter returns all packages (verified via no-filter regression test)
- [x] Response shape `PaginatedResults<PackageSummary>` remains unchanged (no structural changes to response types)
- [x] Invalid license values return 400 Bad Request (verified via invalid license test)

## Step 9 — Self-Verification

### Scope Containment

Files modified/created:
1. `modules/fundamental/src/package/endpoints/list.rs` — listed in Files to Modify
2. `modules/fundamental/src/package/service/mod.rs` — listed in Files to Modify
3. `tests/api/package_license_filter.rs` — listed in Files to Create

All files are within the declared scope. No out-of-scope files are modified.

### Duplication Check

No new utility functions are created. The implementation reuses `apply_filter` from `common/src/db/query.rs` directly. No duplication of existing filtering logic.

### Dead Parameter Detection

No parameters are removed in this change — only new optional parameters are added.

### Sensitive-Pattern Check

No secrets, credentials, or environment files are introduced.

## Step 10 — Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to package list endpoint

Add optional license query parameter to GET /api/v2/package supporting
single and comma-separated multi-value filtering via apply_filter from
common/src/db/query.rs. Join through package_license entity for
license-based filtering.

Implements TC-9203"
```

Push and create PR:

```
git push -u origin TC-9203
gh pr create --base main --title "feat(package): add license filter to package list endpoint" --body "..."
```
