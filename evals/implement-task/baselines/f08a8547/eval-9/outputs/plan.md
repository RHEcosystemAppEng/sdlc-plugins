# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Task Summary

Remove the `version_filter` parameter and its associated filtering logic from the
`SbomService::list` method, propagating the removal through all call sites (endpoint
handler, search service, and integration tests).

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

Validation passes. Proceed.

## Step 1 -- Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira Key**: TC-9207
- **Bookend Type**: none
- **Target PR**: none (standard flow)
- **Dependencies**: none

### Files to Modify

1. `modules/fundamental/src/sbom/service/sbom.rs`
2. `modules/fundamental/src/sbom/endpoints/list.rs`
3. `tests/api/sbom.rs`

### Files to Create

None.

### API Changes

- `GET /api/v2/sbom` -- CHANGED: remove `version` query parameter support

## Step 4 -- Understand the Code

### Symbols to inspect (via serena_backend)

1. **`SbomService::list`** in `modules/fundamental/src/sbom/service/sbom.rs`
   - Current signature:
     ```rust
     pub async fn list(
         &self,
         search: Query,
         paginated: Paginated,
         version_filter: &str,
         tx: &Transactional<'_>,
     ) -> Result<PaginatedResults<SbomSummary>, AppError>
     ```
   - The `version_filter` parameter is used inside the body to apply a `VersionMatches`
     filter to the query. All other query pipeline stages (search, pagination, tx) remain.

2. **Endpoint handler** in `modules/fundamental/src/sbom/endpoints/list.rs`
   - Extracts a `version` query parameter from the HTTP request.
   - Passes the extracted value to `SbomService::list` as the `version_filter` argument.

3. **SearchService** in `modules/search/src/service/mod.rs`
   - Calls `SbomService::list` with an empty string `""` for `version_filter`.

4. **Integration tests** in `tests/api/sbom.rs`
   - `test_list_sboms_version_filtered` -- exercises the version filter with specific values.
   - Other SBOM list tests pass version filter values (likely empty strings).

### Sibling / convention analysis

Based on the repository structure:
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping (consistent across advisory, package services)
- **Naming**: `verb_noun` pattern for methods (`fetch`, `list`, `ingest`)
- **Endpoint pattern**: each domain uses `model/ + service/ + endpoints/` structure
- **Test assertions**: `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Documentation files identified

- `docs/api.md` -- REST API reference, may document the `version` query parameter
- `docs/architecture.md` -- unlikely to be affected
- `CONVENTIONS.md` -- present at repo root, would be read for CI commands

## Step 5 -- Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/sbom/service/sbom.rs`

**What changes**: Remove the `version_filter` parameter from the `list` method signature
and remove all filtering logic that references it.

**Before** (conceptual):
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let mut query = /* ... build base query from search ... */;

    // Version filter logic to REMOVE:
    if !version_filter.is_empty() {
        query = query.filter(VersionMatches::new(version_filter));
    }

    // Remaining pipeline (pagination, execution, mapping) stays intact
    let results = query.paginate(paginated).fetch(tx).await?;
    Ok(results)
}
```

**After** (conceptual):
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError> {
    let query = /* ... build base query from search ... */;

    // Version filter removed -- filtering now done client-side
    let results = query.paginate(paginated).fetch(tx).await?;
    Ok(results)
}
```

**Key decisions**:
- The `version_filter` parameter is **removed entirely** from the signature, not renamed
  to `_version_filter`. Per SKILL.md Step 9 dead parameter detection: "The correct fix
  is removal, not renaming."
- The `VersionMatches` filter application block is removed.
- All other query pipeline stages (search application, pagination, tx propagation) are
  preserved exactly.
- If `VersionMatches` is imported solely for this use, remove the import as well.

### File 2: `modules/fundamental/src/sbom/endpoints/list.rs`

**What changes**: Remove extraction of the `version` query parameter and stop passing
it to `SbomService::list`.

**Before** (conceptual):
```rust
pub async fn list_sboms(
    Query(params): Query<ListParams>,
    service: Data<SbomService>,
    // ...
) -> Result<Json<PaginatedResults<SbomSummary>>, AppError> {
    let version = params.version.unwrap_or_default();
    let results = service.list(params.search, params.paginated, &version, &tx).await?;
    Ok(Json(results))
}
```

**After** (conceptual):
```rust
pub async fn list_sboms(
    Query(params): Query<ListParams>,
    service: Data<SbomService>,
    // ...
) -> Result<Json<PaginatedResults<SbomSummary>>, AppError> {
    let results = service.list(params.search, params.paginated, &tx).await?;
    Ok(Json(results))
}
```

**Additional changes**:
- Remove the `version` field from the `ListParams` query parameter struct (if defined
  in this file or its module).
- Remove any deserialization or default logic for the version field.

### File 3: `tests/api/sbom.rs`

**What changes**: Remove or update the version-filter-specific test, and update any
remaining call sites that pass a `version_filter` argument.

- **Remove** `test_list_sboms_version_filtered` entirely -- the feature it tests no
  longer exists.
- **Update** all remaining calls to `SbomService::list` in test helper code to remove
  the `version_filter` argument.
- **Update** any HTTP request builders that include a `version` query parameter in tests
  for the `GET /api/v2/sbom` endpoint -- remove the parameter.
- Verify other SBOM list tests still pass without changes to their assertions.

### Additional call site: `modules/search/src/service/mod.rs`

**What changes**: This file calls `SbomService::list` with an empty `version_filter`.
Remove the empty string argument from the call.

**Before**:
```rust
let sbom_results = sbom_service.list(search, paginated, "", &tx).await?;
```

**After**:
```rust
let sbom_results = sbom_service.list(search, paginated, &tx).await?;
```

**Scope note**: This file is NOT listed in "Files to Modify" in the task description.
However, removing the `version_filter` parameter from `SbomService::list` will cause a
compilation failure here. Per SKILL.md Step 9 scope containment: this out-of-scope
modification would be flagged for user approval, with the explanation that it is a
mechanically required call site update (the code will not compile otherwise). This is a
direct consequence of the dead parameter removal mandated by Step 9.

## Step 7 -- Tests

- Remove `test_list_sboms_version_filtered` from `tests/api/sbom.rs`.
- Run `cargo test -p trustify-fundamental` (or appropriate crate name resolved via
  `cargo metadata`) to verify all remaining SBOM tests pass.
- Run the full test suite for any crate containing modified files.

## Step 8 -- Acceptance Criteria Verification

| Criterion | How verified |
|-----------|-------------|
| `list` method no longer filters by version | version_filter parameter and VersionMatches logic removed from sbom.rs |
| `version` query parameter no longer extracted | version field removed from ListParams, not passed to service |
| All call sites compile without version_filter | endpoint handler, search service, and tests updated |
| Non-version-filtering tests still pass | cargo test confirms no regressions |

## Step 9 -- Self-Verification Checklist

### Dead parameter detection

This is the central concern for this task. After removing the `VersionMatches` filter
logic from the `list` method body:

1. **Identify candidates**: The `version_filter` parameter's only references are in the
   removed filter logic. It becomes a dead parameter.
2. **Detect**: After removing the body logic, `version_filter` would have zero references
   in the function body. The Rust compiler would emit an `unused variable` warning if
   it were renamed to `_version_filter`, but per SKILL.md the correct fix is **removal,
   not renaming**.
3. **Remove**: Remove `version_filter: &str` from the method signature entirely.
4. **Update call sites**: Use `find_referencing_symbols` or Grep to locate all 3 callers:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- remove the argument
   - `modules/search/src/service/mod.rs` -- remove the empty string argument
   - `tests/api/sbom.rs` -- remove the argument from all test calls
5. **Re-run tests** to confirm nothing broke.

### Scope containment

Modified files vs task scope:
- `modules/fundamental/src/sbom/service/sbom.rs` -- in scope
- `modules/fundamental/src/sbom/endpoints/list.rs` -- in scope
- `tests/api/sbom.rs` -- in scope
- `modules/search/src/service/mod.rs` -- **out of scope** but required for compilation;
  flag for user approval

### Documentation currency

Check `docs/api.md` for documentation of the `version` query parameter on
`GET /api/v2/sbom`. If documented, remove the parameter from the API reference.

### Sensitive-pattern check

No secrets, credentials, or environment file changes expected.

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "fix(sbom): remove version-based filter from SBOM list endpoint

Remove the version_filter parameter from SbomService::list and all call
sites. Version filtering has been moved to the client side, making this
server-side parameter dead code.

Call sites updated:
- endpoint handler (list.rs): stop extracting version query param
- search service (mod.rs): remove empty-string version argument
- integration tests (sbom.rs): remove version-filter-specific test

Implements TC-9207"
```

Then push and create PR targeting `main`.

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment summarizing: removed version_filter parameter and VersionMatches logic
  from SbomService::list, updated 3 call sites, removed version-filter test
- Transition TC-9207 to In Review
