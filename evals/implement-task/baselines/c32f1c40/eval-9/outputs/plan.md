# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md (`claude-md-mock.md`) contains all required sections:
- **Repository Registry**: trustify-backend with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Serena instance `serena_backend` with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed from the task description (TC-9207):

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Remove version-based filtering logic from the SBOM list endpoint |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | (none) |
| API Changes | `GET /api/v2/sbom` -- remove `version` query parameter support |
| Target PR | (none) |
| Bookend Type | (none) |
| Dependencies | None |

## Step 4 -- Understand the Code (simulated)

### Files to inspect

1. **`modules/fundamental/src/sbom/service/sbom.rs`** -- Contains `SbomService::list` with the `version_filter` parameter. Would use `mcp__serena_backend__get_symbols_overview` to view the method structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on `SbomService::list` to read the full method body and identify the `VersionMatches` filter logic.

2. **`modules/fundamental/src/sbom/endpoints/list.rs`** -- Contains the endpoint handler that extracts the `version` query parameter and passes it to `SbomService::list`. Would use `get_symbols_overview` to understand the handler structure and query parameter extraction.

3. **`tests/api/sbom.rs`** -- Integration tests including `test_list_sboms_version_filtered`. Would read the test file to understand which tests use the `version_filter` parameter and which are independent of it.

### Call site analysis

Would use `mcp__serena_backend__find_referencing_symbols` on `SbomService::list` to confirm all 3 call sites:
1. `modules/fundamental/src/sbom/endpoints/list.rs` -- passes the extracted `version` query param
2. `modules/search/src/service/mod.rs` -- passes an empty string `""` as `version_filter`
3. `tests/api/sbom.rs` -- passes various version filter values

### Convention conformance analysis

Would examine sibling files for patterns:
- `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint handler
- `modules/fundamental/src/advisory/service/advisory.rs` -- sibling service
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling list endpoint

Expected conventions:
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Naming: `verb_noun` pattern for functions
- Test assertions: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Framework: Axum for HTTP, SeaORM for database

### CONVENTIONS.md lookup

Would check for `trustify-backend/CONVENTIONS.md` and extract any CI check commands and code generation commands for use in Step 9.

### Documentation file identification

Would check for:
- `docs/api.md` -- REST API reference (may document the `version` query parameter)
- `docs/architecture.md` -- System architecture overview
- `README.md` at repo root

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**What to change:** Remove the version-based filtering logic from the `list` method.

**Current signature:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**Changes:**
1. Remove the `version_filter: &str` parameter from the method signature.
2. In the method body, remove the code that applies a `VersionMatches` filter to the query using `version_filter`. Keep all other query pipeline logic intact (search, pagination, transaction handling).

**Target signature:**
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**Implementation approach:** Use `mcp__serena_backend__replace_symbol_body` to rewrite the `list` method body with the version filter logic removed, or use `mcp__serena_backend__find_symbol` to read the current body, identify the exact lines applying `VersionMatches`, and then use Edit to remove them surgically.

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**What to change:** Remove the `version` query parameter extraction and stop passing it to `SbomService::list`.

**Changes:**
1. Remove the `version` field from the query parameter extraction struct (likely a struct implementing `Deserialize` for Axum's `Query` extractor).
2. Remove the line that passes the extracted version value to `SbomService::list`.
3. Update the call to `SbomService::list` to match the new 3-parameter signature (without `version_filter`).

**Before (conceptual):**
```rust
let result = sbom_service.list(search, paginated, &query.version, &tx).await?;
```

**After:**
```rust
let result = sbom_service.list(search, paginated, &tx).await?;
```

### File 3: `tests/api/sbom.rs`

**What to change:** Remove or update `test_list_sboms_version_filtered` and update remaining call sites.

**Changes:**
1. Remove the `test_list_sboms_version_filtered` test function entirely, since the feature it tests is being removed.
2. Update any remaining calls to `SbomService::list` in other test functions to remove the `version_filter` argument.

### Call site 4 (out-of-scope discovery): `modules/search/src/service/mod.rs`

**Note:** This file is NOT listed in the task's "Files to Modify" section but IS listed as a call site in the Implementation Notes. This is an intentional scope conflict. Per the skill's Step 9 scope containment check, this file would be flagged as out-of-scope, explained (it calls `SbomService::list` with an empty version filter and must be updated for compilation), and user approval would be requested.

**Required change:** Update the call from `sbom_service.list(search, paginated, "", &tx)` to `sbom_service.list(search, paginated, &tx)`.

This is a mechanical change required for compilation -- without it, the project will not build after removing the parameter from the service method.

## Step 7 -- Write Tests

- **Remove** `test_list_sboms_version_filtered` since the feature under test no longer exists.
- **Verify** all remaining SBOM list tests still compile and pass without the `version_filter` argument.
- Run `cargo test -p trustify-fundamental` (or equivalent crate name) to confirm.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| The `list` method in SbomService no longer filters by version | Confirmed by inspecting the modified method body -- no `VersionMatches` logic remains |
| The `version` query parameter is no longer extracted or accepted by the endpoint | Confirmed by inspecting the modified endpoint handler -- version field removed from query struct |
| All call sites compile and pass without the version_filter argument | All 3 call sites updated: endpoint handler, search service, integration tests |
| Existing tests that don't depend on version filtering still pass | Confirmed by `cargo test` run |

## Step 9 -- Self-Verification

### Scope containment
- `modules/fundamental/src/sbom/service/sbom.rs` -- in scope
- `modules/fundamental/src/sbom/endpoints/list.rs` -- in scope
- `tests/api/sbom.rs` -- in scope
- `modules/search/src/service/mod.rs` -- **OUT OF SCOPE** -- flagged to user with explanation: required for compilation after removing the `version_filter` parameter from `SbomService::list`

### Dead parameter detection
The `version_filter` parameter removal from `SbomService::list` IS the dead parameter detection outcome. The skill's Step 9 dead parameter detection confirms this was handled correctly: the parameter was removed from the signature and all call sites were updated.

### CI checks
Would run any CI check commands from `CONVENTIONS.md`, plus `cargo test -p <crate-name>` for each affected crate.

### Documentation currency
Would check `docs/api.md` for references to the `version` query parameter on `GET /api/v2/sbom` and remove or update them.

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/sbom/service/sbom.rs \
       modules/fundamental/src/sbom/endpoints/list.rs \
       modules/search/src/service/mod.rs \
       tests/api/sbom.rs
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version-based filter from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and the
version query parameter from the GET /api/v2/sbom endpoint. Version
filtering has been moved to the client side and is no longer needed
server-side.

Update all call sites: endpoint handler, search service, and
integration tests. Remove test_list_sboms_version_filtered test.

Implements TC-9207"
git push -u origin TC-9207
```

Then create a PR:
```
gh pr create --base main --title "refactor(sbom): remove version-based filter from SBOM list endpoint" --body "..."
```

## Step 11 -- Update Jira

1. Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format.
2. Add a comment summarizing the changes (with footnote per `shared/comment-footnote.md`).
3. Transition TC-9207 to In Review.
