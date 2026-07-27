# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared license (exact match on SPDX identifier). Support both single-value and comma-separated multi-value filtering.

- **Jira Issue**: TC-9203
- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new branch and PR)

---

## Step 0 — Project Configuration Validation

The project CLAUDE.md contains all required sections:
1. **Repository Registry** — `trustify-backend` mapped to Serena instance `serena_backend`
2. **Jira Configuration** — Project key `TC`, Cloud ID, Feature issue type ID present
3. **Code Intelligence** — Serena instance `serena_backend` with `rust-analyzer`

Validation passes. Proceed with implementation.

---

## Step 1 — Parsed Task Description

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Bookend Type | (none) |
| Target PR | (none) |

### Files to Modify

1. `modules/fundamental/src/package/endpoints/list.rs` — add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` — add license filter to PackageService list method

### Files to Create

1. `tests/api/package_license_filter.rs` — integration tests for the license filter

### API Changes

- `GET /api/v2/package?license=MIT` — add optional `license` query parameter for filtering
- `GET /api/v2/package?license=MIT,Apache-2.0` — support comma-separated license values

### Acceptance Criteria

1. `GET /api/v2/package?license=MIT` returns only packages with MIT license
2. `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license
3. `GET /api/v2/package` without license parameter returns all packages (no regression)
4. Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
5. Invalid license values return 400 Bad Request

---

## Step 4 — Code Understanding Plan

### Files to Inspect (via Serena `serena_backend`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current package list handler; use `get_symbols_overview` then `find_symbol` on the handler function and its `Query` struct to understand the existing parameter extraction pattern.

2. **`modules/fundamental/src/package/service/mod.rs`** — PackageService; use `get_symbols_overview` to find the `list` method signature and understand how filters are passed and applied.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (sibling/reuse reference) — advisory list handler with `severity` filter; use `get_symbols_overview` and `find_symbol` to extract the exact Query struct pattern and how the severity filter is wired to the service layer.

4. **`common/src/db/query.rs`** — shared query helpers; use `find_symbol` with `include_body=true` on `apply_filter` to understand its signature, how it parses comma-separated values, and how it generates SQL IN clauses.

5. **`entity/src/package_license.rs`** — package-license join entity; use `get_symbols_overview` to understand the SeaORM entity structure (columns, relations) for constructing the JOIN query.

6. **`common/src/model/paginated.rs`** — `PaginatedResults<T>` response wrapper; verify the response type is unchanged.

7. **`common/src/error.rs`** — `AppError` enum; verify how 400 Bad Request errors are returned for invalid input.

### Sibling Convention Analysis

- **Sibling endpoint file**: `modules/fundamental/src/advisory/endpoints/list.rs` — severity filter pattern
- **Sibling endpoint file**: `modules/fundamental/src/sbom/endpoints/list.rs` — SBOM list handler pattern
- **Sibling service file**: `modules/fundamental/src/advisory/service/advisory.rs` — advisory service filter handling
- **Sibling test files**: `tests/api/advisory.rs`, `tests/api/sbom.rs` — test patterns for endpoint integration tests

### Expected Discovered Conventions

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list_packages`)
- **Query struct**: Endpoint list handlers define a `Query` struct with optional filter fields, deserialized from query parameters via Axum extractors
- **Response type**: List endpoints return `PaginatedResults<T>`
- **Filter application**: Filters use `apply_filter` from `common/src/db/query.rs` for comma-separated multi-value support

### Test Convention Analysis

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and key fields
- **Error cases**: Include 400/404 status code tests
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_filtered_by_license`)

### Documentation Files

- `CONVENTIONS.md` at repository root — check for CI check commands
- `docs/api.md` — API reference; may need update for new query parameter

---

## Step 5 — Branch Creation

```
git checkout main
git pull
git checkout -b TC-9203
```

---

## Step 6 — Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the `Query` struct**: Add an `Option<String>` field named `license` to the existing `Query` struct used by the list handler. This follows the exact same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter — single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter. Follow the same propagation pattern used by the advisory endpoint's severity filter.

3. **Input validation**: Validate the license parameter values before passing to the service. If any value in the comma-separated list is empty or contains invalid characters, return a 400 Bad Request using `AppError`. Follow the existing validation pattern from the advisory severity filter.

**Reuse**: The `Query` struct pattern is directly copied from the advisory list endpoint's Query struct — add one `Option<String>` field.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add `license` parameter to the `list` method signature**: Add an `Option<String>` parameter for the license filter.

   ```rust
   pub async fn list(
       &self,
       // ... existing params
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Build the license filter query**: When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and generate a SQL IN clause. Join through `entity/src/package_license.rs` (the `package_license` table) to filter packages by their associated license SPDX identifiers.

   ```rust
   if let Some(license_filter) = license {
       let license_values = apply_filter(&license_filter);
       // JOIN package_license ON package.id = package_license.package_id
       // WHERE package_license.license IN (license_values)
       query = query
           .join(/* PackageLicense entity */)
           .filter(package_license::Column::License.is_in(license_values));
   }
   ```

3. **Preserve existing behavior**: When `license` is `None`, the query runs without the license join/filter, returning all packages as before.

**Reuse**: 
- `apply_filter` from `common/src/db/query.rs` — directly reused for comma-separated value parsing
- `package_license` entity from `entity/src/package_license.rs` — used for the JOIN query via SeaORM relations
- The filter application pattern mirrors the advisory service's severity filter implementation

### File 3 (new): `tests/api/package_license_filter.rs`

**Create integration tests following the sibling test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:**

1. **`test_list_packages_filter_single_license`**: 
   - Seed test DB with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - `GET /api/v2/package?license=MIT`
   - Assert response status is 200
   - Assert all returned packages have MIT license
   - Assert correct `total_count`

2. **`test_list_packages_filter_multiple_licenses`**:
   - Seed test DB with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert response status is 200
   - Assert returned packages have either MIT or Apache-2.0 license
   - Assert GPL-3.0 packages are excluded
   - Assert correct `total_count`

3. **`test_list_packages_no_license_filter`**:
   - Seed test DB with packages having various licenses
   - `GET /api/v2/package` (no license parameter)
   - Assert response status is 200
   - Assert all packages are returned (no regression)
   - Assert `total_count` matches total seeded packages

4. **`test_list_packages_invalid_license`**:
   - `GET /api/v2/package?license=` (empty value) or with invalid characters
   - Assert response status is 400 Bad Request

5. **`test_list_packages_license_filter_no_matches`**:
   - `GET /api/v2/package?license=NONEXISTENT-LICENSE`
   - Assert response status is 200
   - Assert empty results with `total_count: 0`

Each test will include:
- A `///` doc comment describing what it verifies
- Given/When/Then section comments for non-trivial tests
- Value-based assertions (checking specific license values, not just counts)

### Module Registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness root) so the new test file is compiled and run.

### Documentation Impact

- Check `docs/api.md` for the `GET /api/v2/package` endpoint documentation and add the `license` query parameter description.
- No changes to `CONVENTIONS.md` or architecture docs needed.

---

## Step 7 — Test Execution

```
cargo test --test package_license_filter
```

Run the full test suite to verify no regressions:

```
cargo test
```

---

## Step 8 — Acceptance Criteria Verification

| Criterion | Verified By |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | `test_list_packages_filter_multiple_licenses` |
| No license param returns all packages | `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests deserialize `PaginatedResults<PackageSummary>` |
| Invalid license returns 400 | `test_list_packages_invalid_license` |

---

## Step 9 — Self-Verification Checks

### Scope Containment
Expected modified/created files:
- `modules/fundamental/src/package/endpoints/list.rs` (modified) — in scope
- `modules/fundamental/src/package/service/mod.rs` (modified) — in scope
- `tests/api/package_license_filter.rs` (created) — in scope
- `tests/api/mod.rs` (modified, if needed for module registration) — minor out-of-scope but necessary for test compilation; flag for user approval

### Data-Flow Trace
- `GET /api/v2/package?license=MIT` -> Axum query param extraction (list.rs) -> `PackageService::list()` with license filter (service/mod.rs) -> `apply_filter` parses comma values (query.rs) -> SeaORM query with JOIN on `package_license` and IN clause -> `PaginatedResults<PackageSummary>` response — **COMPLETE**

### Contract & Sibling Parity
- Package list handler follows same `Result<T, AppError>` return type as advisory list handler
- Filter application uses same `apply_filter` + SeaORM pattern as advisory severity filter
- Response type `PaginatedResults<PackageSummary>` unchanged

### Duplication Check
- No new filter parsing logic written — reuses `apply_filter` from `common/src/db/query.rs`
- No new entity code — reuses existing `package_license` entity

---

## Step 10 — Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
      modules/fundamental/src/package/service/mod.rs \
      tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203"
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

---

## Step 11 — Jira Update

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add implementation comment summarizing changes
- Transition TC-9203 to In Review
