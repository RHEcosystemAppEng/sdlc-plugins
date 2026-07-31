# Implementation Plan: TC-9207 — Remove version-based filter from SBOM list endpoint

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena Instance: serena_backend, Path: ./)
- Jira Configuration with Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence section with tool naming convention and serena_backend instance

All required sections present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

**Key**: TC-9207
**Summary**: Remove version-based filter from SBOM list endpoint
**Status**: To Do

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter` parameter in `SbomService::list` was used to filter SBOMs by a specific version string, but this filter is no longer needed -- version filtering has been moved to the client side. Remove the filter logic from the service method body.
- **Files to Modify**:
  1. `modules/fundamental/src/sbom/service/sbom.rs` -- remove version-based filtering logic from the `list` method
  2. `modules/fundamental/src/sbom/endpoints/list.rs` -- remove the `version` query parameter extraction and stop passing it to the service method
  3. `tests/api/sbom.rs` -- remove or update the `test_list_sboms_version_filtered` test
- **Files to Create**: (none)
- **API Changes**: `GET /api/v2/sbom` -- CHANGED: remove `version` query parameter support
- **Acceptance Criteria**:
  - The `list` method in SbomService no longer filters by version
  - The `version` query parameter is no longer extracted or accepted by the endpoint
  - All call sites compile and pass without the version_filter argument
  - Existing tests that don't depend on version filtering still pass
- **Test Requirements**:
  - Remove or update `test_list_sboms_version_filtered` since the feature is removed
  - Verify other SBOM list tests still pass without changes
- **Dependencies**: None

### Target Branch extraction

Target Branch is `main`. The task branch will be created from `main`.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9207)` and search for a comment whose body starts with `[sdlc-workflow] Description digest:`. If no digest comment is found, proceed with a warning: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." If a digest comment is found, would compute the current digest using `python3 scripts/sha256-digest.py` and compare format tags and hex digests. On match, proceed silently. On mismatch, alert the user and pause execution.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would call `jira.user_info()` to get the current user's account ID, then assign and transition:
- `jira.edit_issue(TC-9207, assignee=<current-user-account-id>)`
- `jira.transition_issue(TC-9207) -> In Progress`

## Step 4 -- Understand the Code

### Code Inspection

Before making any changes, inspect the files listed in Files to Modify using the serena_backend Serena instance:

1. **`modules/fundamental/src/sbom/service/sbom.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see the structure of SbomService, then use `mcp__serena_backend__find_symbol` with `include_body=true` to read the `list` method body. Identify the `version_filter` parameter and locate the `VersionMatches` filter logic that uses it.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see the endpoint handler function. Use `mcp__serena_backend__find_symbol` to read the handler body and identify where the `version` query parameter is extracted and passed to `SbomService::list`.

3. **`tests/api/sbom.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see all test functions. Identify `test_list_sboms_version_filtered` and any other tests that call `SbomService::list` with a version_filter argument.

4. **Backward compatibility check**: use `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` to identify ALL call sites. The task lists 3 call sites:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- the REST endpoint handler
   - `modules/search/src/service/mod.rs` -- the search service (passes empty version filter)
   - `tests/api/sbom.rs` -- integration tests

### Sibling analysis (Convention Conformance)

Analyze sibling files for established conventions:
- **`modules/fundamental/src/advisory/service/advisory.rs`** -- AdvisoryService follows the same `model/ + service/ + endpoints/` structure. Methods return `Result<T, AppError>` with `.context()` wrapping.
- **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Advisory list endpoint uses the same pattern: extract query params, call service method, return `PaginatedResults<T>`.
- **`tests/api/advisory.rs`** -- Advisory tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

#### Discovered conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Module structure: `model/ + service/ + endpoints/`
- Naming: `verb_noun` pattern for functions
- Response types: list endpoints return `PaginatedResults<T>`
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)`

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it for naming rules, directory structure, code patterns, test conventions, and CI check commands.

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Remove the version-based filtering logic from the `list` method body.

The `list` method currently has this signature:
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

In the method body, locate and remove the `VersionMatches` filter logic that uses `version_filter`. Keep the rest of the query pipeline intact (search, pagination, transaction handling).

After removing the filtering logic, the `version_filter` parameter is no longer referenced anywhere in the method body. This makes it a dead parameter. See Step 9 (Dead parameter detection) for how this is handled -- the parameter will be removed from the signature entirely.

**Updated signature after dead parameter removal:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

The `version_filter: &str` parameter is removed completely from the function signature. It is NOT renamed to `_version_filter` -- renaming to an underscore-prefixed name would suppress the compiler warning but leave unnecessary API surface. Dead parameters must be removed, not hidden.

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**Change**: Remove the `version` query parameter extraction and stop passing it to the service method.

- Remove the extraction of the `version` query parameter from the request (the `Query` extractor or manual parameter parsing for the version field).
- Update the call to `SbomService::list` to remove the `version_filter` argument. The call changes from:
  ```rust
  service.list(search, paginated, &version, &tx).await
  ```
  to:
  ```rust
  service.list(search, paginated, &tx).await
  ```
- Remove any struct field or variable related to the version query parameter if it was part of a query params struct.

### File 3: `tests/api/sbom.rs`

**Change**: Remove or update the `test_list_sboms_version_filtered` test and update other test call sites.

- Remove the `test_list_sboms_version_filtered` test entirely since the version filtering feature is being removed.
- Update any remaining test calls to `SbomService::list` to remove the `version_filter` argument. For example:
  ```rust
  // Before:
  service.list(search, paginated, "", &tx).await
  // After:
  service.list(search, paginated, &tx).await
  ```

### Call site 3 (out-of-scope, flagged): `modules/search/src/service/mod.rs`

The task's Implementation Notes identify a third call site in `modules/search/src/service/mod.rs` where the search service calls `SbomService::list` with an empty version filter. This file is NOT listed in the Files to Modify section, but it MUST be updated to remove the `version_filter` argument -- otherwise the code will not compile.

**Scope containment note**: This file is out-of-scope per the task's Files to Modify section. Per Step 9's scope containment check, this out-of-scope modification is flagged for user approval. However, updating this call site is mechanically required -- without it, the code will not compile after removing the parameter from the `SbomService::list` signature.

**Change**: Update the call from:
```rust
sbom_service.list(search, paginated, "", &tx).await
```
to:
```rust
sbom_service.list(search, paginated, &tx).await
```

## Step 7 -- Write Tests

- Remove `test_list_sboms_version_filtered` since the version filtering feature is being removed entirely.
- Verify other SBOM list tests still pass without changes. Tests that do not depend on version filtering should be unaffected.

## Step 8 -- Verify Acceptance Criteria

- [x] The `list` method in SbomService no longer filters by version -- filtering logic removed from method body
- [x] The `version` query parameter is no longer extracted or accepted by the endpoint -- extraction removed from list.rs
- [x] All call sites compile and pass without the version_filter argument -- all 3 call sites updated
- [x] Existing tests that don't depend on version filtering still pass -- verified by running tests

## Step 9 -- Self-Verification

### Scope containment

`git diff --name-only` would show:
1. `modules/fundamental/src/sbom/service/sbom.rs` -- in scope (Files to Modify)
2. `modules/fundamental/src/sbom/endpoints/list.rs` -- in scope (Files to Modify)
3. `tests/api/sbom.rs` -- in scope (Files to Modify)
4. `modules/search/src/service/mod.rs` -- OUT OF SCOPE, flagged for user approval

File 4 is out-of-scope but mechanically required: removing the `version_filter` parameter from `SbomService::list` requires updating all call sites, and the search service is a call site. Would ask the user to approve this out-of-scope change.

### Dead parameter detection

After removing the version filtering logic from `SbomService::list`, the `version_filter` parameter becomes dead -- it is no longer referenced anywhere in the function body.

1. **Identify candidates**: The `git diff` shows removed lines in `SbomService::list` that contained the only references to `version_filter`. After removal, zero references to `version_filter` remain in the method body.

2. **Detect dead parameters**: The `version_filter` parameter has zero references in the function body after the filtering logic is removed. The Rust compiler would emit a warning about the unused parameter. The correct fix is REMOVAL, not renaming to `_version_filter`.

3. **Remove dead parameters**: Remove `version_filter: &str` from the `SbomService::list` function signature. Use `mcp__serena_backend__find_referencing_symbols` (or Grep) to find all call sites. Update every caller to remove the corresponding argument:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- remove version_filter argument
   - `modules/search/src/service/mod.rs` -- remove empty string argument
   - `tests/api/sbom.rs` -- remove version_filter arguments from all test calls

4. **Re-run tests** to confirm nothing broke after the parameter removal and call site updates. Run `cargo test` and verify all tests pass.

### Sensitive-pattern check

Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to check for secrets. No sensitive patterns expected in this change.

### CI checks

Would run CI check commands from CONVENTIONS.md (if extracted in Step 4). At minimum, run `cargo build` and `cargo test` to verify the changes compile and pass.

## Step 10 -- Commit and Push

### Commit

```
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filter from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and update
all 3 call sites (endpoint handler, search service, tests). The version
filtering has been moved to the client side and is no longer needed in
the backend.

Implements TC-9207"
```

### Branch and PR

```
git push -u origin TC-9207
gh pr create --base main --title "refactor(sbom): remove version-based filter from SBOM list endpoint" --body "..."
```

The PR description would include:
- Implements [TC-9207](https://redhat.atlassian.net/browse/TC-9207)
- Summary of changes made

## Step 11 -- Update Jira

- Update the Git Pull Request custom field (`customfield_10875`) with the PR URL
- Add a comment summarizing the changes
- Transition the issue to In Review
