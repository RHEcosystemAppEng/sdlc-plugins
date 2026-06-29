# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing
consumers to filter packages by their declared license (SPDX identifier). Support both
single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`)
filtering.

**Repository:** trustify-backend
**Target Branch:** main
**Jira Issue:** TC-9203
**Parent Feature:** TC-9001 (incorporated by)

---

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

All required sections are present:
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add license query parameter to GET /api/v2/package
- **Files to Modify:** 2 files listed
- **Files to Create:** 1 file listed
- **API Changes:** 2 modifications listed
- **Implementation Notes:** 4 notes with concrete code references
- **Acceptance Criteria:** 5 criteria
- **Test Requirements:** 4 test cases
- **Reuse Candidates:** 3 candidates identified
- **Dependencies:** None
- **Target PR:** Not present (default flow)
- **Bookend Type:** Not present (default flow)

No missing sections. No bookend or target PR -- this is the standard implementation flow.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress

Would assign to current user and transition TC-9203 to In Progress via Jira API.
(Skipped in eval mode.)

## Step 4 -- Understand the Code

### Files to inspect using Serena (`mcp__serena_backend__*`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** -- current GET /api/v2/package handler
   - Use `get_symbols_overview` to see the struct and handler function signatures
   - Use `find_symbol` with `include_body=true` on the handler function and the query params struct

2. **`modules/fundamental/src/package/service/mod.rs`** -- PackageService
   - Use `get_symbols_overview` to see the list method signature
   - Use `find_symbol` on the `list` method to understand its current parameters and query construction

3. **`common/src/db/query.rs`** (Reuse Candidate) -- shared query helpers
   - Use `find_symbol` on `apply_filter` to understand its signature and how it handles comma-separated values

4. **`modules/fundamental/src/advisory/endpoints/list.rs`** (Reuse Candidate / sibling) -- advisory list endpoint with severity filter
   - Use `get_symbols_overview` to understand the Query struct pattern
   - Use `find_symbol` on the severity filter field and how it is threaded through to the service

5. **`entity/src/package_license.rs`** (Reuse Candidate) -- package-license join entity
   - Use `get_symbols_overview` to see the SeaORM entity definition (columns, relations)

### Sibling convention analysis

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/list.rs` -- structurally identical list endpoint with filtering; primary pattern source
- `modules/fundamental/src/sbom/endpoints/list.rs` -- another list endpoint for convention confirmation
- `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService with filter support; pattern for PackageService changes

**Test file siblings:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests; pattern for assertion style, setup, naming
- `tests/api/sbom.rs` -- SBOM endpoint integration tests; secondary pattern source

### Discovered conventions (expected from sibling analysis)

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Filtering uses `apply_filter` from `common/src/db/query.rs` with comma-separated support
- **Query struct pattern:** Each list endpoint defines a Query struct with optional filter fields, deserialized from query parameters
- **Naming:** Service methods follow `verb_noun` pattern
- **Framework:** Axum for HTTP, SeaORM for database

### Discovered test conventions (expected from sibling analysis)

- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation:** List tests validate `total_count`, `items.len()`, and key fields of returned items
- **Error cases:** Include tests for invalid input returning appropriate error status codes
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Tests hit a real PostgreSQL test database

### Documentation files identified

- `docs/api.md` -- REST API reference; may need updating for the new query parameter
- `CONVENTIONS.md` -- repository root conventions file; read for CI checks and code standards

### CONVENTIONS.md

Would read `CONVENTIONS.md` at the repository root and extract any CI check commands
and code generation commands for use in Step 9.

---

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9203
```

---

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct:**
   - Add an `Option<String>` field named `license` to the existing query parameters struct
   - Follow the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`
   - This field will accept the raw query string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`)

2. **Pass the license filter to PackageService:**
   - In the list handler function, extract `query.license` and pass it to the `PackageService::list()` method
   - Follow the same threading pattern used by the advisory endpoint's severity filter

3. **Input validation:**
   - Add validation for the license parameter value; if present but empty or containing invalid characters, return 400 Bad Request
   - Reuse the validation pattern from the advisory severity filter

**Reuse:** Follows the exact Query struct + optional field pattern from
`modules/fundamental/src/advisory/endpoints/list.rs`.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add license filter parameter to the `list` method:**
   - Add an `Option<String>` parameter for the license filter to the `list` method signature
   - Or, if the method already accepts a query/filter struct, add the field to that struct

2. **Build the filter query using `apply_filter`:**
   - Import `apply_filter` from `common/src/db/query.rs`
   - When `license` is `Some(value)`, call `apply_filter` with the value -- this handles both single values and comma-separated multi-values automatically
   - Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers
   - Use SeaORM's join capabilities to perform the JOIN between the package table and the package_license table

3. **Preserve existing behavior:**
   - When `license` is `None`, the query remains unchanged -- all packages are returned
   - The response type `PaginatedResults<PackageSummary>` is not modified

**Reuse:**
- `common/src/db/query.rs::apply_filter` for comma-separated parsing and SQL IN clause generation
- `entity/src/package_license.rs` for the JOIN entity rather than raw SQL
- Pattern from `modules/fundamental/src/advisory/service/advisory.rs` for how the advisory service integrates its severity filter

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

1. **Test: single license filter returns only matching packages**
   - Seed test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0)
   - Send `GET /api/v2/package?license=MIT`
   - Assert response status is 200
   - Assert returned packages all have MIT license
   - Assert on specific package identifiers, not just count

2. **Test: comma-separated license filter returns packages matching any listed license**
   - Seed test database with packages having different licenses
   - Send `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert response status is 200
   - Assert returned packages have either MIT or Apache-2.0 license
   - Assert specific expected packages are present

3. **Test: no license filter returns all packages unchanged**
   - Seed test database with packages having different licenses
   - Send `GET /api/v2/package` (no license parameter)
   - Assert response status is 200
   - Assert all seeded packages are returned (no regression)

4. **Test: invalid license value returns 400**
   - Send `GET /api/v2/package?license=` (empty value) or other invalid input
   - Assert response status is 400 Bad Request

**Conventions applied:**
- Follow `test_<endpoint>_<scenario>` naming pattern (e.g., `test_list_packages_filtered_by_single_license`)
- Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Validate `total_count`, `items.len()`, and key fields of returned items
- Add `///` doc comments to every test function explaining what it verifies
- Add `// Given`, `// When`, `// Then` section comments for non-trivial tests
- Use `PaginatedResults<PackageSummary>` for response deserialization

### Module registration

- Ensure `tests/api/package_license_filter.rs` is registered in `tests/Cargo.toml` or `tests/api/mod.rs` if applicable (check sibling test registration pattern)

### API documentation

- If `docs/api.md` documents the `GET /api/v2/package` endpoint, add the optional `license` query parameter with its description (single value or comma-separated SPDX identifiers)

---

## Step 7 -- Write Tests

Tests are described above in File 3. After writing, run:

```
cargo test
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | Covered by single license filter test |
| GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | Covered by comma-separated filter test |
| GET /api/v2/package without license returns all packages | Covered by no-filter regression test |
| Response shape PaginatedResults<PackageSummary> unchanged | Response type is not modified; deserialization in tests confirms |
| Invalid license values return 400 | Covered by invalid license test |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show exactly:
  - `modules/fundamental/src/package/endpoints/list.rs` (in Files to Modify)
  - `modules/fundamental/src/package/service/mod.rs` (in Files to Modify)
  - `tests/api/package_license_filter.rs` (in Files to Create)
  - Possibly `docs/api.md` (documentation update -- would flag as out-of-scope for user approval)
  - Possibly test module registration file (would flag for user approval)

### Sensitive-pattern check
- Scan staged diff for secrets/credentials. None expected.

### Duplication check
- Verify no duplicate filter logic exists; `apply_filter` is the canonical implementation being reused.

### Data-flow trace
- Input: `license` query parameter in HTTP request
- Processing: extracted into Query struct -> passed to PackageService::list() -> apply_filter builds SQL IN clause -> JOIN through package_license entity
- Output: filtered PaginatedResults<PackageSummary> returned in HTTP response
- All stages connected. **COMPLETE.**

### Contract & sibling parity
- PackageService::list() maintains same return type
- New handler follows same Result<T, AppError> pattern as siblings
- Error handling follows .context() wrapping convention

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that supports
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
package_license entity.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" \
  --body "..."
```

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link and summary of changes
- Transition TC-9203 to In Review
