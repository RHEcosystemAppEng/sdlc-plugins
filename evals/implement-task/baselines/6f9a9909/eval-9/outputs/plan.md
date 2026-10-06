# Implementation Plan: TC-9207

## Task Summary

Remove version-based filtering logic from the SBOM list endpoint. The `version_filter` parameter in `SbomService::list` is no longer needed because version filtering has been moved to the client side.

## Step-by-step Plan (following implement-task skill)

### Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: Serena with rust-analyzer

Configuration is valid -- proceed.

### Step 1 -- Parse Jira Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Remove version-based filtering from SBOM list endpoint
- **Files to Modify**:
  1. `modules/fundamental/src/sbom/service/sbom.rs`
  2. `modules/fundamental/src/sbom/endpoints/list.rs`
  3. `tests/api/sbom.rs`
- **Files to Create**: none
- **API Changes**: `GET /api/v2/sbom` -- remove `version` query parameter
- **Dependencies**: none
- **Bookend Type**: none
- **Target PR**: none

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress

Would assign task to current user and transition TC-9207 to "In Progress" via Jira API.

### Step 4 -- Understand the Code

#### Files to inspect

1. **`modules/fundamental/src/sbom/service/sbom.rs`** -- Contains `SbomService::list` with current signature:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       version_filter: &str,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
   The `version_filter` parameter is used inside the body to apply a `VersionMatches` filter. Need to identify the exact filter application code and understand the surrounding query pipeline.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** -- Endpoint handler for `GET /api/v2/sbom`. Extracts `version` query parameter and passes it to `SbomService::list`. Need to understand the query parameter struct and handler function.

3. **`tests/api/sbom.rs`** -- Contains `test_list_sboms_version_filtered` test and other SBOM list tests. Need to identify which tests call `SbomService::list` with version filter values.

#### Additional files to inspect (call sites)

4. **`modules/search/src/service/mod.rs`** -- SearchService calls `SbomService::list` with an empty version filter (`""`). Must be updated after removing the parameter.

#### Convention conformance

Would inspect sibling service files (e.g., `advisory.rs`, `package/service/mod.rs`) for patterns:
- Error handling: `Result<T, AppError>` with `.context()`
- List method signatures: `(&self, search, paginated, tx) -> Result<PaginatedResults<T>>`
- Test patterns: `assert_eq!(resp.status(), StatusCode::OK)`

#### Documentation files

- `CONVENTIONS.md` at repository root -- check for CI commands
- `docs/api.md` -- may document the `version` query parameter

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

### Step 6 -- Implement Changes

#### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**What to change:**

1. **Remove `version_filter` parameter from `list` method signature.** The signature changes from:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       version_filter: &str,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
   To:
   ```rust
   pub async fn list(
       &self,
       search: Query,
       paginated: Paginated,
       tx: &Transactional<'_>,
   ) -> Result<PaginatedResults<SbomSummary>, AppError>
   ```

2. **Remove the `VersionMatches` filter application inside the method body.** The body currently applies a filter like:
   ```rust
   if !version_filter.is_empty() {
       query = query.filter(VersionMatches(version_filter));
   }
   ```
   (or equivalent). Remove this block entirely. Keep the rest of the query pipeline intact -- the `search`, `paginated`, and `tx` parameters continue to be used as before.

3. **Remove any `use` import for `VersionMatches`** if it is only used in this method. Check with `search_for_pattern` or Grep to confirm no other code in the file references it.

**Rationale for removing the parameter, not just the body logic:** Per the implement-task skill's Step 9 "Dead parameter detection", after removing the filter logic from the body, the `version_filter` parameter has zero references in the function body. The correct fix is removal, not underscore-prefixing. This is detailed further in `parameter-cleanup.md`.

#### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**What to change:**

1. **Remove `version` from the query parameter extraction struct.** The endpoint likely has a struct like:
   ```rust
   #[derive(Deserialize)]
   struct ListParams {
       // ... other fields
       version: Option<String>,
   }
   ```
   Remove the `version` field.

2. **Update the handler function call to `SbomService::list`.** Remove the `version_filter` argument:
   ```rust
   // Before:
   let result = service.list(search, paginated, &params.version.unwrap_or_default(), &tx).await?;
   
   // After:
   let result = service.list(search, paginated, &tx).await?;
   ```

3. **Remove any version-specific imports or helper logic** that was only used for extracting or processing the version parameter.

#### File 3: `tests/api/sbom.rs`

**What to change:**

1. **Remove or update `test_list_sboms_version_filtered`** -- this test verifies behavior that no longer exists. The entire test function should be removed.

2. **Update any other test that calls `SbomService::list` directly.** If tests call `list()` with a version argument (e.g., `service.list(query, paginated, "", &tx)`), remove the version argument from those calls (e.g., `service.list(query, paginated, &tx)`).

3. **Verify tests that hit `GET /api/v2/sbom?version=...`** via HTTP -- these should be removed or updated to not pass the `version` query parameter. The endpoint should still work; it just ignores (or rejects) the `version` param now.

#### Call site 3: `modules/search/src/service/mod.rs`

**What to change:**

1. **Remove the empty version filter argument.** The search service currently calls:
   ```rust
   sbom_service.list(search, paginated, "", &tx)
   ```
   Change to:
   ```rust
   sbom_service.list(search, paginated, &tx)
   ```

### Step 7 -- Write Tests

- The `test_list_sboms_version_filtered` test should be **removed entirely** since it tests removed functionality.
- All other existing SBOM list tests should continue to pass without modification (apart from removing the `version_filter` argument at direct call sites).
- No new tests are needed -- we are removing functionality, not adding it.

### Step 8 -- Verify Acceptance Criteria

| Criterion | How to verify |
|-----------|--------------|
| `list` method no longer filters by version | Inspect method body -- no `VersionMatches` or version-related filter logic |
| `version` query parameter no longer accepted | Inspect endpoint handler -- no `version` field in params struct |
| All call sites compile without `version_filter` | `cargo check` passes across all crates |
| Existing non-version tests still pass | `cargo test` passes |

### Step 9 -- Self-Verification

#### Scope containment
Expected modified files:
- `modules/fundamental/src/sbom/service/sbom.rs` (in scope)
- `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)
- `tests/api/sbom.rs` (in scope)
- `modules/search/src/service/mod.rs` (out of scope -- but required for compilation; flag for user approval)

#### Dead parameter detection
After removing the `VersionMatches` filter logic from the `list` method body, the `version_filter` parameter becomes dead (zero references in the body). Per the skill's dead parameter detection protocol:
1. Remove the parameter from the signature
2. Use `find_referencing_symbols` or Grep to find all 3 call sites
3. Update every caller to remove the corresponding argument
4. Re-run tests

See `parameter-cleanup.md` for the full approach.

#### CI checks
Run `CONVENTIONS.md` CI commands if present. At minimum:
```
cargo fmt --check
cargo clippy -- -D warnings
cargo check
cargo test -p trustify-fundamental
cargo test -p trustify-search
```

#### Documentation currency
If `docs/api.md` documents the `version` query parameter on `GET /api/v2/sbom`, update it to reflect the parameter's removal.

### Step 10 -- Commit and Push

```
git add modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/list.rs \
       modules/search/src/service/mod.rs \
       tests/api/sbom.rs

git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filtering from list endpoint

Remove the version_filter parameter from SbomService::list and the
version query parameter from GET /api/v2/sbom. Version filtering has
been moved to the client side and is no longer needed server-side.

Update all three call sites (endpoint handler, search service, tests)
to remove the version_filter argument. Remove the
test_list_sboms_version_filtered integration test.

Implements TC-9207"
```

Then push and create PR:
```
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filtering from list endpoint" --body "..."
```

### Step 11 -- Update Jira

- Set Git Pull Request custom field (`customfield_10875`) to the PR URL
- Add comment summarizing the changes
- Transition TC-9207 to "In Review"
