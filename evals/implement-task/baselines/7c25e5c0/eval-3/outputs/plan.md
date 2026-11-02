# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` configured with rust-analyzer

Configuration validated. Proceeding.

## Step 1 — Fetch and Parse Jira Task

**Key:** TC-9203
**Summary:** Add package license filter to list endpoint
**Repository:** trustify-backend
**Target Branch:** main

### Parsed sections

- **Description:** Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier.
- **Files to Modify:**
  1. `modules/fundamental/src/package/endpoints/list.rs` — add license query parameter extraction and filtering
  2. `modules/fundamental/src/package/service/mod.rs` — add license filter to PackageService list method
- **Files to Create:**
  1. `tests/api/package_license_filter.rs` — integration tests for the license filter
- **API Changes:** `GET /api/v2/package?license=MIT` and `GET /api/v2/package?license=MIT,Apache-2.0`
- **Dependencies:** None

### Target Branch extraction
Target Branch is `main`.

### Description integrity (Step 1.5)
No digest comment found — skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 4 — Understand the Code

### Code inspection

Before modifying any files, I would inspect the following using Serena (`mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** — Use `get_symbols_overview` and `find_symbol` to study the severity filter implementation. This is the structural template for the license filter. I would examine:
   - The `Query` struct and its optional `severity` field
   - How `apply_filter` from `common/src/db/query.rs` is called
   - How the filter is passed from endpoint handler to service method

2. **`modules/fundamental/src/package/endpoints/list.rs`** — Use `get_symbols_overview` to understand the current endpoint handler structure, its Query struct, and how it calls PackageService.

3. **`modules/fundamental/src/package/service/mod.rs`** — Use `find_symbol` on the `list` method to understand its current signature, return type, and query building approach.

4. **`common/src/db/query.rs`** — Use `find_symbol(name_path_pattern="apply_filter", include_body=true)` to read the `apply_filter` function signature and understand how it handles comma-separated multi-value parameters and generates SQL IN clauses.

5. **`entity/src/package_license.rs`** — Use `get_symbols_overview` to understand the package-license join entity structure, its columns, and relation definitions.

6. **`common/src/error.rs`** — Use `get_symbols_overview` to understand the AppError enum for 400 Bad Request error handling.

### Convention conformance analysis

From sibling analysis of `advisory/endpoints/list.rs`, `advisory/service/advisory.rs`, and `sbom/endpoints/list.rs`:

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping for error context
- **Naming:** Endpoint handlers use `verb_noun` pattern (e.g., `list_advisories`)
- **Module structure:** Each domain follows `model/ + service/ + endpoints/` pattern
- **Query structs:** List endpoints define a `Query` struct with optional filter fields, deserialized from query parameters via `serde::Deserialize`
- **Filter application:** Optional filter fields are passed to the service layer, which calls `apply_filter` from `common/src/db/query.rs`
- **Response type:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Test patterns:** Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database

### Crate name resolution

I would run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the crate names for the affected packages. The files in `modules/fundamental/src/` belong to the `trustify-module-fundamental` crate (or similar), and `tests/api/` belongs to a separate test crate. The exact crate name would be resolved from cargo metadata rather than derived from the nearest `Cargo.toml`, which may be a virtual workspace manifest.

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**
1. Add an optional `license: Option<String>` field to the `Query` struct (following the same pattern as the `severity` field in `advisory/endpoints/list.rs`)
2. In the endpoint handler function, extract the `license` field from the query parameters
3. Pass the license filter value to `PackageService::list()` as a new parameter
4. Reuse `apply_filter` from `common/src/db/query.rs` to handle comma-separated values — do NOT write new parsing logic

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**
1. Add a `license: Option<String>` parameter to the `PackageService::list()` method signature
2. When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to generate the SQL IN clause for the license values
3. Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their declared license
4. Follow the same pattern used in `advisory/service/advisory.rs` for the severity filter — `apply_filter` handles splitting the comma-separated string and building the WHERE IN clause
5. Return 400 Bad Request (using `AppError`) for invalid license values

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**
1. Create integration tests following the patterns in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`)
2. Test cases:
   - Single license filter (`?license=MIT`) returns only matching packages
   - Comma-separated filter (`?license=MIT,Apache-2.0`) returns packages matching any listed license
   - No license filter returns all packages unchanged
   - Invalid license value returns 400 Bad Request
3. Register the test module in `tests/api/mod.rs` if a module registry exists

### Code reuse approach

**No new utility functions are created.** All filtering logic reuses existing code:
- `common/src/db/query.rs::apply_filter` — handles comma-separated parameter parsing and SQL IN clause generation
- `entity/src/package_license.rs` — provides the JOIN table entity for the database query
- The advisory severity filter pattern in `advisory/endpoints/list.rs` — provides the structural template

## Step 7 — Write Tests

Tests in `tests/api/package_license_filter.rs` following sibling conventions from `tests/api/advisory.rs`:

```rust
/// Verifies that filtering by a single license returns only matching packages.
#[test]
fn test_single_license_filter() {
    // Given packages with MIT and Apache-2.0 licenses in the database
    // When requesting GET /api/v2/package?license=MIT
    // Then only MIT-licensed packages are returned
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[test]
fn test_multi_license_filter() {
    // Given packages with MIT, Apache-2.0, and GPL-3.0 licenses
    // When requesting GET /api/v2/package?license=MIT,Apache-2.0
    // Then packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
}

/// Verifies that omitting the license filter returns all packages.
#[test]
fn test_no_license_filter_returns_all() {
    // Given packages with various licenses
    // When requesting GET /api/v2/package (no license parameter)
    // Then all packages are returned unchanged
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[test]
fn test_invalid_license_returns_400() {
    // Given an invalid license value
    // When requesting GET /api/v2/package?license=!!!
    // Then the response status is 400
}
```

## Step 9 — Self-Verification

### Scope containment
All modified/created files are within the task's Files to Modify and Files to Create sections:
- `modules/fundamental/src/package/endpoints/list.rs` — listed in Files to Modify
- `modules/fundamental/src/package/service/mod.rs` — listed in Files to Modify
- `tests/api/package_license_filter.rs` — listed in Files to Create

No out-of-scope files are modified.

### Duplication check
No new utility functions are created. All filtering logic reuses `apply_filter` from `common/src/db/query.rs`. No duplication of existing functionality.

### Module-level test (Rust)
Run `cargo metadata --no-deps --format-version 1` to resolve crate names, then:
```
cargo test -p <fundamental-crate-name>
cargo test -p <test-crate-name>
```

## Step 10 — Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to list endpoint

Add optional license query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203"
```

```
git push -u origin TC-9203
gh pr create --base main --title "feat(package): add license filter to list endpoint" --body "..."
```
