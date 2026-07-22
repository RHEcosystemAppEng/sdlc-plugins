# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, enabling filtering by SPDX license identifier. Support both single-value and comma-separated multi-value filtering.

- **Jira Key**: TC-9203
- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

---

## Step 0 -- Validate Project Configuration

Project Configuration verified from `claude-md-mock.md`:

- **Repository Registry**: present, lists `trustify-backend` with Serena Instance `serena_backend` at path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present, `serena_backend` instance configured with `rust-analyzer`

All required sections are present. Proceed.

---

## Step 1 -- Parse Task Description

### Parsed sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add `license` query parameter to `GET /api/v2/package` for filtering by SPDX license identifier; support single and comma-separated multi-value |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` (add optional parameter), `GET /api/v2/package?license=MIT,Apache-2.0` (comma-separated) |
| Reuse Candidates | `common/src/db/query.rs::apply_filter`, `modules/fundamental/src/advisory/endpoints/list.rs`, `entity/src/package_license.rs` |
| Bookend Type | None |
| Target PR | None |

### Acceptance Criteria

1. `GET /api/v2/package?license=MIT` returns only packages with MIT license
2. `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license
3. `GET /api/v2/package` without `license` parameter returns all packages (no regression)
4. Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
5. Invalid license values return 400 Bad Request

### Test Requirements

1. Test single license filter returns only matching packages
2. Test comma-separated license filter returns packages matching any listed license
3. Test no license filter returns all packages unchanged
4. Test invalid license value returns 400

---

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

---

## Step 4 -- Understand the Code

### Files to inspect (via Serena `serena_backend` instance)

1. **`modules/fundamental/src/package/endpoints/list.rs`** -- Current package list endpoint handler. Use `get_symbols_overview` to identify the handler function, request extractor, and `Query` struct if present.

2. **`modules/fundamental/src/package/service/mod.rs`** -- `PackageService` with `list` method. Inspect its current signature and how it builds its database query.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Sibling endpoint that already implements a `severity` filter. This is the structural template for the license filter. Use `get_symbols_overview` and `find_symbol` to understand the Query struct, how the optional `severity` field is extracted, and how it flows to the service layer.

4. **`common/src/db/query.rs`** -- Shared query helpers. Find `apply_filter` to understand its signature (`fn apply_filter(query, field, value: Option<String>) -> Result<...>`) and how it handles comma-separated parsing and SQL `IN` clause generation.

5. **`entity/src/package_license.rs`** -- SeaORM entity for the package-license join table. Identify the `Column` enum (expected: `PackageId`, `LicenseId` or `License`), the `Relation` definitions, and how to join from the `package` table through this entity.

6. **`common/src/model/paginated.rs`** -- Confirm `PaginatedResults<T>` structure to ensure the response shape is not affected.

7. **`common/src/error.rs`** -- `AppError` enum, used for returning 400 Bad Request on invalid license values.

### Sibling analysis targets

- **`modules/fundamental/src/advisory/endpoints/list.rs`** -- primary sibling for endpoint filter pattern
- **`modules/fundamental/src/sbom/endpoints/list.rs`** -- secondary sibling for list endpoint structure
- **`tests/api/advisory.rs`** and **`tests/api/sbom.rs`** -- sibling test files for test convention analysis

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, extract CI verification commands and coding conventions. The repo structure shows `CONVENTIONS.md` exists at `trustify-backend/CONVENTIONS.md`.

### Documentation file identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new query parameter)
- `CONVENTIONS.md` -- coding conventions

### Expected discovered conventions (from repo structure and key conventions)

- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Module pattern**: `model/ + service/ + endpoints/` structure
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Expected test conventions (from sibling test analysis)

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List tests validate `total_count`, `items.len()`, and key fields
- **Error cases**: Tests include status code checks for error responses (e.g., `StatusCode::BAD_REQUEST`)
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_filtered_by_license`)

---

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the `Query` struct** (or equivalent request extractor):
   - Add `pub license: Option<String>` field to the query parameters struct, following the same pattern used for `severity` in the advisory list endpoint.
   - The field accepts an optional string that can be a single SPDX identifier or comma-separated list.

2. **Pass `license` to the service layer**:
   - In the handler function, extract `query.license` and pass it to `PackageService::list()`.
   - Follow the same pattern as advisory's handler passes `severity` to `AdvisoryService::list()`.

3. **Validation**:
   - Add validation for the license parameter value. If an invalid/empty license value is provided, return `AppError` that maps to 400 Bad Request.
   - Use `.context()` for error wrapping consistent with the codebase convention.

**Reuse**: Follow the exact structural pattern from `modules/fundamental/src/advisory/endpoints/list.rs` -- the Query struct with an optional field, the extraction, and the pass-through to the service.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Update `PackageService::list()` signature**:
   - Add a `license: Option<String>` parameter (or incorporate it into an existing options/filter struct if the service uses one).

2. **Build the filter query**:
   - When `license` is `Some(value)`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value and generate a SQL `IN` clause.
   - Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license records.
   - Use SeaORM's query builder to add the JOIN and WHERE clause:
     ```rust
     // Pseudocode structure:
     use entity::package_license;
     
     if let Some(license_filter) = license {
         let query = query
             .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
             .filter(apply_filter(package_license::Column::License, &license_filter)?);
     }
     ```

3. **Preserve existing behavior**:
   - When `license` is `None`, the query is unchanged -- all packages returned.
   - The return type `PaginatedResults<PackageSummary>` is unchanged.

**Reuse**:
- `common/src/db/query.rs::apply_filter` -- directly reuse for comma-separated parsing and SQL IN clause generation
- `entity/src/package_license.rs` -- use existing SeaORM entity for the JOIN rather than writing raw SQL

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create a new integration test file with the following test functions:

1. **`test_list_packages_filter_single_license`**:
   - Doc comment: `/// Verifies that filtering by a single license returns only matching packages.`
   - Given: seed test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status is 200, response body contains only MIT-licensed packages, assert on specific package names/identifiers (value-based assertions, not just count)

2. **`test_list_packages_filter_multiple_licenses`**:
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: seed test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status is 200, body contains packages with MIT or Apache-2.0 licenses but not GPL-3.0, assert on specific values

3. **`test_list_packages_no_license_filter`**:
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: seed test database with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: response status is 200, all packages returned, count matches total seeded

4. **`test_list_packages_invalid_license`**:
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: standard test database
   - When: `GET /api/v2/package?license=` (empty value or invalid format)
   - Then: response status is 400 Bad Request

Each test will use given-when-then section comments (`// Given`, `// When`, `// Then`) for navigability. Tests follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling test files. Value-based assertions on specific package fields rather than count-only checks.

### Module registration

The new test file `tests/api/package_license_filter.rs` must be registered in `tests/Cargo.toml` as a test target (or auto-discovered if the test framework uses `mod` declarations). Verify how existing test files like `tests/api/sbom.rs` and `tests/api/advisory.rs` are registered and follow the same approach.

### Documentation impact

- **`docs/api.md`**: Update the `GET /api/v2/package` endpoint documentation to include the new optional `license` query parameter, with examples of single-value and comma-separated usage.
- No other documentation changes needed -- the response shape is unchanged.

---

## Step 8 -- Acceptance Criteria Verification

| # | Criterion | How verified |
|---|---|---|
| 1 | `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| 2 | `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | `test_list_packages_filter_multiple_licenses` |
| 3 | No license parameter returns all packages | `test_list_packages_no_license_filter` |
| 4 | Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` without error |
| 5 | Invalid license returns 400 | `test_list_packages_invalid_license` |

---

## Step 9 -- Self-Verification Checklist

### Scope containment
- Modified files: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` -- both in Files to Modify
- Created files: `tests/api/package_license_filter.rs` -- in Files to Create
- Possible out-of-scope: `docs/api.md` if updated for documentation impact -- would flag to user for approval

### Data-flow trace
- `GET /api/v2/package?license=MIT` -> Axum extracts Query struct with `license: Some("MIT")` -> handler passes to `PackageService::list(license)` -> service calls `apply_filter` to parse value -> SeaORM query joins `package_license` table and adds WHERE clause -> filtered results returned as `PaginatedResults<PackageSummary>` -> JSON response -- **COMPLETE**

### Duplication check
- The `apply_filter` function in `common/src/db/query.rs` already handles comma-separated parsing and SQL IN clauses -- the implementation reuses it directly rather than duplicating that logic.

### Contract and sibling parity
- The package list handler follows the same `Result<T, AppError>` contract as all other handlers
- The Query struct pattern with optional filter field matches the advisory endpoint sibling
- The service method follows the same pattern as `AdvisoryService::list()`

---

## Step 10 -- Commit Plan

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package
supporting single-value and comma-separated multi-value filtering
by SPDX license identifier. Reuses apply_filter from common query
helpers and joins through the existing package_license entity.

Implements TC-9203
```

Branch: `TC-9203` off `main`
PR base: `main`
PR description includes: `Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)`
