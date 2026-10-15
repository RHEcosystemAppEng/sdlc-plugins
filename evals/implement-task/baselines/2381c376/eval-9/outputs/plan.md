# Implementation Plan for TC-9207

## Task Summary

Remove version-based filtering logic from the SBOM list endpoint. The `version_filter`
parameter in `SbomService::list` is used to apply a `VersionMatches` filter to the query,
but this filtering has been moved client-side and the server-side logic must be removed.

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Parse Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira Issue**: TC-9207 (child of TC-9001)
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None
- **Files to Modify**:
  1. `modules/fundamental/src/sbom/service/sbom.rs`
  2. `modules/fundamental/src/sbom/endpoints/list.rs`
  3. `tests/api/sbom.rs`
- **Files to Create**: None
- **API Changes**: `GET /api/v2/sbom` -- remove `version` query parameter support

## Step 4 -- Understand the Code

### Inspection plan (using Serena instance `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs`
   to see the `SbomService` struct and `list` method signature.
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `SbomService::list` to read
   the full method body and identify the `VersionMatches` filtering logic.
3. `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` to confirm all 3
   call sites documented in the task:
   - `modules/fundamental/src/sbom/endpoints/list.rs` (REST handler)
   - `modules/search/src/service/mod.rs` (search service)
   - `tests/api/sbom.rs` (integration tests)
4. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/list.rs`
   to understand how `version` is extracted from the query string.
5. `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` to identify
   `test_list_sboms_version_filtered` and any other tests calling `SbomService::list`.

### Convention conformance analysis

Examine sibling files for patterns:
- `modules/fundamental/src/advisory/service/advisory.rs` -- sibling service, check `list` signature
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
- `tests/api/advisory.rs` -- sibling test file

Expected conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern (e.g., `list`, `fetch`)
- Response types: list endpoints return `PaginatedResults<T>`
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Documentation file identification

- `README.md` at repo root
- `CONVENTIONS.md` at repo root (extract CI check commands)
- `docs/api.md` -- REST API reference (may document the `version` query parameter)

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**What to change:**
- Remove the `version_filter: &str` parameter from the `list` method signature.
- Remove the `VersionMatches` filter logic from the method body that uses `version_filter`.
  This likely involves removing a conditional block or filter chain step such as:
  ```rust
  if !version_filter.is_empty() {
      query = query.filter(VersionMatches(version_filter));
  }
  ```
  or a similar `.filter()` call in the query pipeline.
- Keep the rest of the query pipeline intact (search, pagination, sorting, transaction).

**After the change, the signature becomes:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**What to change:**
- Remove the extraction of the `version` query parameter from the request. This likely
  involves removing a field from a query parameter struct or removing a
  `Query<VersionFilter>` extractor parameter from the handler function signature.
- Update the call to `SbomService::list` to no longer pass the `version_filter` argument.

**Before (conceptual):**
```rust
let results = service.list(search, paginated, &version_param, &tx).await?;
```

**After:**
```rust
let results = service.list(search, paginated, &tx).await?;
```

### File 3: `tests/api/sbom.rs`

**What to change:**
- Remove or delete `test_list_sboms_version_filtered` entirely, since the feature it tests
  no longer exists.
- Update any remaining test functions that call `SbomService::list` to remove the
  `version_filter` argument. These tests should pass an updated argument list without
  the version string.

**Before (conceptual):**
```rust
let results = service.list(search, paginated, "", &tx).await.unwrap();
```

**After:**
```rust
let results = service.list(search, paginated, &tx).await.unwrap();
```

## Step 7 -- Tests

- Remove `test_list_sboms_version_filtered` entirely.
- Verify remaining SBOM list tests compile and pass with the updated `list` signature.
- Run: `cargo test -p trustify-fundamental` and `cargo test -p trustify-tests` (or the
  appropriate crate names resolved via `cargo metadata`).

## Step 8 -- Acceptance Criteria Verification

| Criterion | How verified |
|---|---|
| The `list` method no longer filters by version | Inspect method body -- `VersionMatches` logic removed |
| The `version` query parameter is no longer accepted | Inspect endpoint handler -- extraction removed |
| All call sites compile and pass without `version_filter` | All 3 call sites updated; `cargo test` passes |
| Existing tests that don't depend on version filtering still pass | `cargo test` confirms |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show exactly the 3 files listed in Files to Modify.
- No out-of-scope files.

### Dead parameter detection
- This is the core of the task. After removing the `VersionMatches` filter logic from
  `SbomService::list`, the `version_filter` parameter becomes dead (zero references in
  the method body). Per Step 9 guidance: **remove the parameter entirely** (do not
  rename with underscore prefix). Then update all 3 call sites. See
  `outputs/parameter-cleanup.md` for the detailed approach.

### Sensitive-pattern check
- No secrets or credentials involved.

### Documentation currency
- If `docs/api.md` documents the `version` query parameter on `GET /api/v2/sbom`, remove
  that documentation entry.

### CI checks
- Run CI commands from `CONVENTIONS.md` (formatting, linting, clippy, compilation).
- Run `cargo test -p <crate>` for each modified crate.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/sbom/service/sbom.rs \
      modules/fundamental/src/sbom/endpoints/list.rs \
      tests/api/sbom.rs

git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filter from list endpoint

Remove the version_filter parameter from SbomService::list and the version
query parameter from the GET /api/v2/sbom endpoint. Version filtering has
been moved to the client side.

Update all 3 call sites (endpoint handler, search service, tests) to remove
the version_filter argument. Remove test_list_sboms_version_filtered test.

Implements TC-9207"
```

Then push and create PR:
```
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filter from list endpoint" --body "..."
```

## Step 11 -- Update Jira

- Update `customfield_10875` with PR URL (ADF format).
- Add comment with PR link and summary of changes.
- Transition TC-9207 to In Review.
