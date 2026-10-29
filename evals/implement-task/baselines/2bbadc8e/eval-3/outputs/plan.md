# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID present, Feature issue type ID `10142`, custom fields configured
- **Code Intelligence**: `serena_backend` instance with `rust-analyzer`

Validation passes. Proceed.

## Step 1 -- Parse Task Description

| Field               | Value |
|---------------------|-------|
| Key                 | TC-9203 |
| Repository          | trustify-backend |
| Target Branch       | main |
| Target PR           | (none -- default flow) |
| Bookend Type        | (none -- standard implementation) |
| Dependencies        | None |

Structured description is complete; all required sections present.

## Step 2 -- Verify Dependencies

No dependencies declared. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would call `jira.user_info()`, assign TC-9203 to current user, transition to In Progress.
(Skipped -- no external service interaction in this eval.)

## Step 4 -- Understand the Code

### Files to Modify

**`modules/fundamental/src/package/endpoints/list.rs`**
- Current state: handles `GET /api/v2/package` with pagination and sorting query parameters.
- Contains a `PackageQuery` struct (or similar) that deserializes query parameters from the request.
- Calls `PackageService::list()` with the current query/filter parameters.
- Would use `mcp__serena_backend__get_symbols_overview` on this file to see the `PackageQuery` struct and the handler function.

**`modules/fundamental/src/package/service/mod.rs`**
- Contains `PackageService` with a `list()` method that builds a SeaORM query against the package table.
- Currently applies pagination and sorting but has no license-based filter.
- Would use `mcp__serena_backend__find_symbol` to read the `list` method body.

### Sibling / Reference Files (Convention Conformance Analysis)

**`modules/fundamental/src/advisory/endpoints/list.rs`** (primary reuse reference)
- Already implements a `severity` query parameter filter using a `Query` struct with an `Option<String>` field.
- Uses `apply_filter` from `common/src/db/query.rs` to convert the comma-separated string into a SQL IN clause.
- This is the structural template for the license filter.

**`modules/fundamental/src/advisory/service/advisory.rs`**
- `AdvisoryService::list()` receives a filter parameter and applies it to the SeaORM query via a join.
- Pattern to follow: receive filter, build conditional join, apply filter condition.

**`common/src/db/query.rs`**
- Contains `apply_filter` function: parses comma-separated values, generates `column.is_in(values)` SeaORM condition.
- Already handles single-value and multi-value cases.
- No modification needed -- reuse as-is.

**`entity/src/package_license.rs`**
- SeaORM entity mapping the `package_license` table.
- Contains `Column` enum with fields like `PackageId` and `License` (or `SpdxIdentifier`).
- Used for the JOIN between `package` and `package_license` tables.

### Documentation Files Identified

- `docs/api.md` -- REST API reference; may need updating to document the new `license` parameter.
- `README.md` -- unlikely to need changes for a query parameter addition.

### CONVENTIONS.md Lookup

`CONVENTIONS.md` exists at repository root. Would read it for:
- CI check commands (formatting, linting, compilation) to run in Step 9.
- Code generation commands (e.g., OpenAPI spec generation).
- Naming and structural conventions.

### Convention Conformance Analysis (Discovered Conventions)

- **Error handling**: handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Naming**: `verb_noun` pattern for functions; query struct fields match URL parameter names.
- **Endpoint structure**: query parameters deserialized via `#[derive(Deserialize)]` struct, passed to service method.
- **Filter pattern**: optional filter fields are `Option<String>` in the query struct; `apply_filter` handles parsing.
- **Response types**: list endpoints return `PaginatedResults<T>`.
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern; integration tests hit a real PostgreSQL test database.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the query parameters struct** (e.g., `PackageQuery` or `PackageListQuery`):
   ```rust
   /// Optional license filter. Supports comma-separated SPDX identifiers.
   pub license: Option<String>,
   ```
   Follow the exact pattern used by the `severity` field in `advisory/endpoints/list.rs`.

2. **Pass the license filter to the service call**:
   In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter.

3. **Add validation**: If the `license` parameter is present but contains empty segments after splitting on comma, return a 400 Bad Request. Follow the validation pattern from the advisory severity filter if one exists, or use `AppError::BadRequest` with a descriptive message.

**Reuse**: Follows the `advisory/endpoints/list.rs` severity filter struct pattern exactly. No new patterns introduced.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Update `PackageService::list()` method signature** to accept an optional license filter parameter:
   ```rust
   pub async fn list(
       &self,
       // ... existing params (pagination, sorting, etc.)
       license_filter: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter to the query**:
   - When `license_filter` is `Some(value)`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string into individual values.
   - Add a LEFT JOIN (or INNER JOIN for filtering) to the `package_license` entity from `entity/src/package_license.rs`.
   - Apply the filter condition: `package_license::Column::License.is_in(parsed_values)`.
   - Ensure distinct results (a package with multiple license matches should appear only once).

3. **No change when filter is absent**: When `license_filter` is `None`, the query runs unchanged -- no JOIN added, no filter applied. This preserves backward compatibility.

**Reuse**:
- `apply_filter` from `common/src/db/query.rs` for comma-separated parsing and SQL IN clause generation.
- `entity::package_license` entity for the JOIN -- no raw SQL needed.
- Follow the same join-and-filter pattern used in `AdvisoryService::list()` for severity filtering.

### File 3 (new): `tests/api/package_license_filter.rs`

**Changes:**

Create an integration test file with the following test functions:

1. **`test_filter_packages_by_single_license`**
   ```rust
   /// Verifies that filtering by a single license returns only packages with that license.
   ```
   - Given: seed test DB with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status is 200; response body contains only packages with MIT license; assert on specific package names/identifiers, not just count.

2. **`test_filter_packages_by_multiple_licenses`**
   ```rust
   /// Verifies that comma-separated license values return packages matching any listed license.
   ```
   - Given: seed test DB with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status is 200; response body contains packages with MIT or Apache-2.0 licenses but not GPL-3.0; assert on specific package identifiers.

3. **`test_no_license_filter_returns_all_packages`**
   ```rust
   /// Verifies that omitting the license parameter returns all packages unchanged.
   ```
   - Given: seed test DB with packages having various licenses.
   - When: `GET /api/v2/package`
   - Then: response status is 200; all seeded packages are present in the response.

4. **`test_invalid_license_returns_400`**
   ```rust
   /// Verifies that an invalid license value returns a 400 Bad Request response.
   ```
   - Given: standard test DB.
   - When: `GET /api/v2/package?license=` (empty value) or other invalid input.
   - Then: response status is 400.

**Test conventions followed:**
- Integration tests hit a real PostgreSQL test database (per project convention).
- `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks.
- Value-based assertions on response body (per skill guidance, overriding any length-only sibling patterns).
- Doc comments on every test function (per skill guidance).
- Given/When/Then section comments in test bodies (per skill guidance for non-trivial tests).

### Module Registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) to register the new test file.
- This is an out-of-scope file modification that would be flagged in Step 9 scope containment and requires user approval.

### Documentation Impact

- `docs/api.md`: update the `GET /api/v2/package` endpoint documentation to include the new `license` query parameter, its type (`string`), optionality (`optional`), and behavior (comma-separated SPDX identifiers, exact match).
- This is a lightweight documentation update scoped to the modified endpoint.

## Step 7 -- Write Tests

Tests described above in File 3. Would run:
```
cargo test -p trustify-tests  # or whichever crate contains tests/api/
```
Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|-----------|-------------|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_filter_packages_by_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Covered by `test_filter_packages_by_multiple_licenses` |
| `GET /api/v2/package` without license returns all packages | Covered by `test_no_license_filter_returns_all_packages` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | Service method return type unchanged; no model modifications |
| Invalid license values return 400 | Covered by `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment
- `modules/fundamental/src/package/endpoints/list.rs` -- in scope (Files to Modify)
- `modules/fundamental/src/package/service/mod.rs` -- in scope (Files to Modify)
- `tests/api/package_license_filter.rs` -- in scope (Files to Create)
- `tests/api/mod.rs` -- out-of-scope (module registration); flag for user approval
- `docs/api.md` -- out-of-scope (documentation update); flag for user approval

### Duplication check
- License filter logic reuses `apply_filter` from `common/src/db/query.rs`; no new filtering utilities created.
- No duplication of existing code detected.

### Dead parameter detection
- No parameters removed from existing functions.

### Sensitive-pattern check
- No secrets, credentials, or `.env` patterns in the diff.

### Data-flow trace
- Input: HTTP request with `?license=MIT` query parameter
- Parsing: Axum deserializes into `PackageQuery` struct; `license` field populated as `Option<String>`
- Processing: handler passes to `PackageService::list()`; service calls `apply_filter` to parse comma-separated values; SeaORM query joins `package_license` table and applies `.is_in()` filter
- Output: `PaginatedResults<PackageSummary>` returned as JSON response
- All stages connected. Data flow is complete.

### CI checks
- Would run commands from `CONVENTIONS.md` (formatting, linting, clippy, compilation).
- Would run `cargo test -p <crate-name>` for each modified crate.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and the package_license
entity join table.

Implements TC-9203"
git push -u origin TC-9203
gh pr create --base main --title "feat(package): add license filter to list endpoint" --body "$(cat <<'EOF'
## Summary

- Add `license` query parameter to `GET /api/v2/package` for filtering packages by SPDX license identifier
- Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering
- Reuse `apply_filter` from `common/src/db/query.rs` and join through `entity/src/package_license.rs`

## Test plan

- [ ] `test_filter_packages_by_single_license` -- verify single license filter returns only matching packages
- [ ] `test_filter_packages_by_multiple_licenses` -- verify comma-separated filter returns union of matches
- [ ] `test_no_license_filter_returns_all_packages` -- verify no regression when parameter is omitted
- [ ] `test_invalid_license_returns_400` -- verify invalid input returns 400

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)
EOF
)"
```

## Step 11 -- Update Jira

Would update:
- `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment with PR link, summary of changes, no deviations from plan
- Transition TC-9203 to In Review
