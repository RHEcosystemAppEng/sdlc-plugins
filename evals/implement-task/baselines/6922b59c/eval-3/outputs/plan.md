# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` with `rust-analyzer`

Configuration is valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

**Parsed sections from TC-9203:**

| Section | Value |
|---------|-------|
| Repository | trustify-backend |
| Target Branch | main |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |

**Description**: Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering on SPDX license identifiers.

**Files to Modify:**
1. `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method

**Files to Create:**
1. `tests/api/package_license_filter.rs` -- integration tests for the license filter

**API Changes:**
- `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
- `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values

**Acceptance Criteria:**
1. `GET /api/v2/package?license=MIT` returns only packages with MIT license
2. `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license
3. `GET /api/v2/package` without license parameter returns all packages (no regression)
4. Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
5. Invalid license values return 400 Bad Request

**GitHub Issue custom field**: `customfield_10747` -- would check issue fields for a GitHub issue URL.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9203, assignee=<account-id>)`
3. `jira.transition_issue(TC-9203)` to In Progress

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

**`modules/fundamental/src/package/endpoints/list.rs`**
- Use `mcp__serena_backend__get_symbols_overview` on this file to see its current structure (the Query struct, handler function, route registration).
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function and the Query struct to read their implementations.

**`modules/fundamental/src/package/service/mod.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see PackageService methods.
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to understand current query construction.

### 4.2 Inspect reuse candidates

**`common/src/db/query.rs`**
- Use `mcp__serena_backend__find_symbol` on `apply_filter` with `include_body=true` to understand its signature and how it handles comma-separated values and SQL IN clauses.

**`modules/fundamental/src/advisory/endpoints/list.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see the advisory Query struct and handler.
- Use `mcp__serena_backend__find_symbol` on the advisory Query struct to see how the `severity` optional field is declared and used.

**`entity/src/package_license.rs`**
- Use `mcp__serena_backend__get_symbols_overview` to see the SeaORM entity definition, columns, relations.

### 4.3 Check backward compatibility

- Use `mcp__serena_backend__find_referencing_symbols` on `PackageService::list` to identify all callers and ensure the added optional parameter does not break them.

### 4.4 Convention conformance analysis (sibling analysis)

**Production siblings:**
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling list endpoint with severity filter (primary pattern source)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- sibling list endpoint for SBOMs

**Test siblings:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests (pattern source for test structure)
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Examine these for:
- Naming conventions: expect `verb_noun` pattern for functions, `Query` struct per endpoint
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Import organization and module structure
- Test patterns: `assert_eq!(resp.status(), StatusCode::OK)`, real PostgreSQL test database

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. The repo structure shows `CONVENTIONS.md` exists. Would read it for:
- CI check commands (extract for Step 9)
- Code generation commands
- Naming rules, directory structure, code patterns

### 4.6 Documentation file identification

- `docs/api.md` -- REST API reference, may need updating for the new query parameter
- `docs/architecture.md` -- unlikely to need changes
- `README.md` at repository root

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### 6.1 Modify `modules/fundamental/src/package/endpoints/list.rs`

**What to change:**

1. **Add `license` field to the `Query` struct**: Following the advisory `list.rs` pattern where the `severity` field is an `Option<String>`, add:
   ```rust
   /// Optional license SPDX identifier filter. Supports comma-separated values.
   pub license: Option<String>,
   ```

2. **Update the handler function**: After extracting the Query parameters, add license filter logic:
   - Check if `query.license` is `Some`
   - Call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value and generate the SQL IN clause
   - Join through the `package_license` entity table when filtering
   - Pass the filter condition to the PackageService `list` method

3. **Add validation**: Validate that license values are non-empty strings. Return `AppError` (400 Bad Request) for invalid values.

**Reuse:**
- Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/list.rs` for the Query struct field and handler filter extraction
- Use `apply_filter` from `common/src/db/query.rs` for comma-separated parsing

### 6.2 Modify `modules/fundamental/src/package/service/mod.rs`

**What to change:**

1. **Add license filter parameter to the `list` method signature**: Add an optional parameter `license_filter: Option<Vec<String>>` (or equivalent after `apply_filter` parsing).

2. **Implement the filter in the query builder**: When `license_filter` is `Some`:
   - Join the `package_license` entity table (`entity::package_license`) to the package query
   - Add a WHERE clause: `package_license.license IN (<values>)` using SeaORM's `column.is_in()` method
   - Ensure the join does not produce duplicates (use DISTINCT or group by package ID)

3. **Preserve backward compatibility**: When `license_filter` is `None`, the query behaves exactly as before -- no join, no filter, all packages returned.

**Reuse:**
- Use `entity::package_license` (from `entity/src/package_license.rs`) for the join -- this is the existing SeaORM entity, no raw SQL needed
- Follow the same query-building pattern used in the advisory service for severity filtering

### 6.3 Create `tests/api/package_license_filter.rs`

**What to create:**

Integration tests hitting the real PostgreSQL test database, following the patterns from `tests/api/advisory.rs`.

```rust
/// Verifies that filtering by a single license returns only matching packages.
#[tokio::test]
async fn test_single_license_filter() {
    // Given: packages with MIT and Apache-2.0 licenses in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only MIT-licensed packages are returned
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[tokio::test]
async fn test_comma_separated_license_filter() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_no_license_filter_returns_all() {
    // Given: packages with various licenses
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned (no regression)
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_invalid_license_returns_400() {
    // Given: a request with an empty/invalid license value
    // When: GET /api/v2/package?license=
    // Then: 400 Bad Request is returned
}
```

**Conventions applied:**
- Doc comment on every test function (skill requirement, overrides sibling pattern if siblings lack them)
- Given-When-Then section comments inside each test body
- Value-based assertions: assert on specific package names/licenses, not just counts
- `assert_eq!(resp.status(), StatusCode::OK)` pattern from siblings
- Same test database setup/teardown pattern as `tests/api/advisory.rs`

### 6.4 Register the test module

Add `mod package_license_filter;` to `tests/api/mod.rs` (or the appropriate test runner file) so the new test file is compiled and executed.

### 6.5 Documentation impact

- Update `docs/api.md` to document the new `license` query parameter on `GET /api/v2/package`, including both single-value and comma-separated usage examples.

### 6.6 Code quality checks

- Every new public symbol (struct fields, functions) gets a doc comment
- Defensive property access on license values from the query parameter
- No raw SQL -- use SeaORM entities and `apply_filter` throughout

## Step 7 -- Write Tests

Implement the four tests described in 6.3 above. Run:

```bash
cargo test -p trustify-tests  # or whatever crate contains tests/api/
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|-----------|-------------|
| `?license=MIT` returns only MIT packages | Covered by `test_single_license_filter` |
| `?license=MIT,Apache-2.0` returns either | Covered by `test_comma_separated_license_filter` |
| No parameter returns all packages | Covered by `test_no_license_filter_returns_all` |
| Response shape unchanged | Tests validate `PaginatedResults<PackageSummary>` deserialization |
| Invalid license returns 400 | Covered by `test_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify only these files are modified/created:
- `modules/fundamental/src/package/endpoints/list.rs` (modify)
- `modules/fundamental/src/package/service/mod.rs` (modify)
- `tests/api/package_license_filter.rs` (create)

If `docs/api.md` is also modified, flag as out-of-scope documentation update and request user approval (since it was not in the task's Files to Modify).

### Dead parameter detection
The `list` method signature is being extended (adding a parameter), not removing references. No dead parameters expected.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no secrets expected in this change.

### Duplication check
Search for any existing license filtering logic in the codebase to avoid duplication. The `apply_filter` reuse should prevent this.

### Data-flow trace
- **Input**: HTTP query parameter `license` extracted from `GET /api/v2/package?license=MIT`
- **Processing**: `apply_filter` parses comma-separated values into `Vec<String>`, passed to `PackageService::list`, which builds a SeaORM query joining `package_license` with IN clause
- **Output**: Filtered `PaginatedResults<PackageSummary>` returned as JSON response
- All stages connected. Complete path.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

### Module-level test requirement (Rust)
Run `cargo test -p <package-name>` for each crate containing modified files:
- The `fundamental` crate (contains the endpoint and service)
- The test crate (contains integration tests)

### Contract and sibling parity
- **Contract**: Verify the Query struct matches Axum's deserialization requirements
- **Sibling parity**: Compare with advisory list endpoint for consistent error handling, logging, filter application
- **Cross-module entity**: `package_license` entity usage -- check other modules for consistent join/query patterns
- **Caller-site**: Check all callers of `PackageService::list` to update them with the new parameter (passing `None` to preserve existing behavior)

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/package/endpoints/list.rs \
      modules/fundamental/src/package/service/mod.rs \
      tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX identifier filtering.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203
EOF
)"
git push -u origin TC-9203
```

Then create PR:

```bash
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "$(cat <<'EOF'
## Summary

- Add optional `license` query parameter to `GET /api/v2/package` for filtering by SPDX license identifier
- Support comma-separated values for multi-license filtering (e.g., `?license=MIT,Apache-2.0`)
- Reuse `apply_filter` from `common/src/db/query.rs` and join through existing `package_license` entity

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)

## Test plan

- [ ] `test_single_license_filter` -- verify single license returns only matching packages
- [ ] `test_comma_separated_license_filter` -- verify multi-value returns packages matching any listed license
- [ ] `test_no_license_filter_returns_all` -- verify no regression when parameter is omitted
- [ ] `test_invalid_license_returns_400` -- verify invalid values return 400 Bad Request
EOF
)"
```

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request) with the PR URL in ADF format
2. Add comment to TC-9203 with PR link, summary of changes, and note about reusing `apply_filter` and the advisory severity filter pattern
3. Transition TC-9203 to In Review
