# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Step 0 -- Validate Project Configuration

CLAUDE.md contains:
- Repository Registry: trustify-backend with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer

All required sections present. Proceed.

## Step 1 -- Fetch and Parse Jira Task

**Key**: TC-9207
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: (none)
**Target PR**: (none)
**Dependencies**: None

### Parsed sections

- **Description**: Remove the version-based filtering logic from `SbomService::list`. The `version_filter` parameter was used to filter SBOMs by version string; this is no longer needed since filtering moved client-side.
- **Files to Modify**:
  1. `modules/fundamental/src/sbom/service/sbom.rs` -- remove version filtering logic from `list`
  2. `modules/fundamental/src/sbom/endpoints/list.rs` -- remove `version` query param extraction, stop passing it
  3. `tests/api/sbom.rs` -- remove or update `test_list_sboms_version_filtered`
- **Files to Create**: (none)
- **API Changes**: `GET /api/v2/sbom` -- remove `version` query parameter support
- **Acceptance Criteria**:
  - The `list` method in SbomService no longer filters by version
  - The `version` query parameter is no longer extracted or accepted by the endpoint
  - All call sites compile and pass without the version_filter argument
  - Existing tests that do not depend on version filtering still pass
- **Test Requirements**:
  - Remove or update `test_list_sboms_version_filtered`
  - Verify other SBOM list tests still pass

## Step 2 -- Verify Dependencies

No dependencies declared. Proceed.

## Step 3 -- Transition to In Progress

1. Fetch current user via `jira.user_info()`
2. Assign TC-9207 to current user via `jira.edit_issue`
3. Transition TC-9207 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Files to inspect

1. **`modules/fundamental/src/sbom/service/sbom.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the structure. Then use `mcp__serena_backend__find_symbol(name_path_pattern="SbomService::list", include_body=true)` to read the full method body and understand how `version_filter` is used in the query pipeline.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the endpoint handler. Then read the handler function to understand how `version` is extracted from the query string and passed to `SbomService::list`.

3. **`modules/search/src/service/mod.rs`** -- Use `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` to confirm this file calls `list` with an empty version filter string.

4. **`tests/api/sbom.rs`** -- Read test functions that call `SbomService::list` or hit `GET /api/v2/sbom?version=...` to understand how tests exercise the version filter.

### Sibling / convention analysis

- Examine `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService::list`) and `modules/fundamental/src/advisory/endpoints/list.rs` as siblings. These follow the same `model/ + service/ + endpoints/` pattern.
- Error handling: `Result<T, AppError>` with `.context()` wrapping.
- Response types: list endpoints return `PaginatedResults<T>`.
- Test patterns: `assert_eq!(resp.status(), StatusCode::OK)` in `tests/api/`.

### CONVENTIONS.md

Check `./CONVENTIONS.md` for CI check commands. Extract and record any `cargo fmt`, `cargo clippy`, `cargo test` commands for Step 9.

### Documentation files

- `docs/api.md` -- may reference the `version` query parameter on `GET /api/v2/sbom`; will need to check and update if so.
- `README.md` -- unlikely to reference endpoint details at this granularity.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Remove the version-based filtering logic from the `list` method body.

Current signature:
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

Actions:
1. Remove the `version_filter: &str` parameter from the signature entirely (dead parameter -- see parameter-cleanup.md).
2. Remove the lines in the method body that use `version_filter` to construct and apply a `VersionMatches` filter to the query.
3. Keep all other query pipeline logic intact (search, pagination, transaction).

New signature:
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**Change**: Remove the `version` query parameter extraction and stop passing it to `SbomService::list`.

Actions:
1. Remove the `version` field from the query parameters struct (or remove the extraction of `version` from the query string).
2. Update the call to `SbomService::list(...)` to no longer pass the `version` argument. The call changes from 4 arguments (`search, paginated, version_filter, tx`) to 3 arguments (`search, paginated, tx`).

### File 3: `tests/api/sbom.rs`

**Change**: Remove or update the `test_list_sboms_version_filtered` test.

Actions:
1. Remove the `test_list_sboms_version_filtered` test function entirely, since the feature it tests no longer exists.
2. Update any remaining test calls to `SbomService::list` to remove the `version_filter` argument. If tests call the service directly, update from `service.list(search, paginated, "", &tx)` to `service.list(search, paginated, &tx)`.
3. Verify tests that call the endpoint via HTTP no longer pass `?version=...` query parameters (or if they do and the parameter is simply ignored, confirm they still pass).

## Step 7 -- Write Tests

- The `test_list_sboms_version_filtered` test is removed since the feature is deleted.
- No new tests are needed -- the change is a removal.
- Run `cargo test -p <crate>` for each affected crate to verify existing tests still pass without the version_filter argument.

## Step 8 -- Verify Acceptance Criteria

| Criterion | How verified |
|---|---|
| `list` method no longer filters by version | Inspect method body -- `VersionMatches` filter logic removed |
| `version` query param no longer extracted | Inspect endpoint handler -- `version` field removed from query struct |
| All call sites compile without version_filter | `cargo check` passes; all 3 call sites updated |
| Existing non-version tests pass | `cargo test` passes |

## Step 9 -- Self-Verification

### Scope containment

Expected modified files:
- `modules/fundamental/src/sbom/service/sbom.rs`
- `modules/fundamental/src/sbom/endpoints/list.rs`
- `modules/search/src/service/mod.rs` (call site update -- flagged as out-of-scope, see below)
- `tests/api/sbom.rs`

**Out-of-scope file**: `modules/search/src/service/mod.rs` is not listed in Files to Modify but must be changed because it is a call site of `SbomService::list`. This is a necessary consequence of the dead parameter removal (Step 9 dead parameter detection). Would flag for user approval before proceeding.

### Dead parameter detection

After removing the version filtering logic from the `list` method body, the `version_filter: &str` parameter has zero references in the function body. This is a dead parameter.

**Action**: Remove `version_filter` from the signature entirely. Do NOT prefix with underscore. Update all 3 call sites. See `parameter-cleanup.md` for the full approach.

### CI checks

Run CI commands from CONVENTIONS.md:
1. `cargo fmt --check`
2. `cargo clippy -- -D warnings`
3. `cargo test -p trustify-fundamental`
4. `cargo test -p trustify-search` (if search module was modified)
5. `cargo test` for integration test crate

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency

Check `docs/api.md` for references to the `version` query parameter on `GET /api/v2/sbom`. If documented, remove the parameter from the API reference.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/sbom/service/sbom.rs \
      modules/fundamental/src/sbom/endpoints/list.rs \
      modules/search/src/service/mod.rs \
      tests/api/sbom.rs
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filter from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and all call
sites. Version filtering has been moved to the client side and is no
longer needed in the backend service layer.

Implements TC-9207"
```

Push and create PR:
```
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filter from SBOM list endpoint" --body "..."
```

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format.
2. Add comment with PR link and summary of changes.
3. Transition TC-9207 to In Review.
