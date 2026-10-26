# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Task Summary

Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter` parameter in `SbomService::list` was used to filter SBOMs by a specific version string, but this filter is no longer needed -- version filtering has been moved to the client side. After removing the filter logic from the method body, the `version_filter` parameter itself becomes dead and must be removed from the signature and all call sites.

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- Service method

**Current state:** The `SbomService::list` method has the signature:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

The method body uses `version_filter` to apply a `VersionMatches` filter to the query pipeline.

**Changes:**

1. **Remove the version filtering logic from the method body.** Delete the code that applies the `VersionMatches` filter using `version_filter`. Keep the rest of the query pipeline intact (search, pagination, transaction handling).

2. **Remove the `version_filter` parameter from the function signature.** After removing the filtering logic, the `version_filter` parameter has zero references in the method body. Per Step 9 dead parameter detection, the correct fix is removal -- not renaming to `_version_filter`. The updated signature becomes:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

3. **Remove any unused imports** related to the `VersionMatches` filter type, if they become unused after the filtering logic is removed.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- REST endpoint handler

**Current state:** The handler extracts a `version` query parameter from the HTTP request and passes it to `SbomService::list` as the `version_filter` argument.

**Changes:**

1. **Remove the `version` query parameter extraction.** Delete the code that extracts the `version` field from the query parameters struct or request.

2. **Update the call to `SbomService::list`** to remove the `version_filter` argument. Change from:

```rust
sbom_service.list(search, paginated, &version, tx).await
```

to:

```rust
sbom_service.list(search, paginated, tx).await
```

3. **Remove the `version` field from the query parameters struct** (if the endpoint defines a typed query params struct that includes a `version` field). Also remove any `#[serde]` attributes related to that field.

4. **Remove any unused imports** that were only needed for the version query parameter handling.

### 3. `tests/api/sbom.rs` -- Integration tests

**Current state:** Contains `test_list_sboms_version_filtered` and other tests that pass various `version_filter` values to `SbomService::list`.

**Changes:**

1. **Remove the `test_list_sboms_version_filtered` test entirely.** The feature under test (version filtering) no longer exists, so the test is invalid.

2. **Update other SBOM list tests** that call `SbomService::list` to remove the `version_filter` argument. For any test that calls `list` with a version filter value, update the call from:

```rust
sbom_service.list(search, paginated, "", &tx).await
```

to:

```rust
sbom_service.list(search, paginated, &tx).await
```

3. **Remove test helper code or fixtures** specifically related to version filtering, if any exist.

4. **Update HTTP-level integration tests** that send the `version` query parameter to `GET /api/v2/sbom`. Remove the `?version=...` query parameter from test request URLs.

## Files to Create

None.

## API Changes

- `GET /api/v2/sbom` -- CHANGED: the `version` query parameter is no longer accepted. Clients that currently pass `?version=X` will have the parameter silently ignored (if using a permissive query param parser) or receive an error (if using strict parsing). Since the task states version filtering has moved to the client side, this is the intended behavior.

## Handling the `version_filter` Parameter After Removing Filter Logic

This is the critical dead parameter detection scenario (SKILL.md Step 9):

1. **Detection:** After removing the `VersionMatches` filter logic from the `list` method body, the `version_filter: &str` parameter has zero remaining references in the function body. It is a dead parameter.

2. **Resolution:** Remove the parameter entirely from the function signature. Do NOT rename it to `_version_filter` -- that would suppress the compiler warning but leave a dead parameter in the API, confusing future maintainers about whether the parameter is intended for future use.

3. **Call site updates:** There are exactly 3 call sites that must be updated:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- remove the version argument from the `list()` call
   - `modules/search/src/service/mod.rs` -- remove the empty string `""` argument from the `list()` call
   - `tests/api/sbom.rs` -- remove the version argument from all `list()` calls in tests

4. **Verification:** After updating all call sites, run `cargo test -p trustify-fundamental` and `cargo test -p trustify-search` to confirm compilation and test passage.

## Verification Steps

1. `cargo check` -- confirm the project compiles without the `version_filter` parameter
2. `cargo test -p trustify-fundamental` -- confirm fundamental module tests pass
3. `cargo test -p trustify-search` -- confirm search module tests pass (since it calls `SbomService::list`)
4. `cargo test -p trustify-tests` (or equivalent for integration tests) -- confirm API integration tests pass
5. Run any CI checks from CONVENTIONS.md (formatting, linting, clippy)
6. Verify `git diff --name-only` shows only the 3 expected files plus `modules/search/src/service/mod.rs`

## Scope Containment Note

The task description lists 3 files under "Files to Modify." However, `modules/search/src/service/mod.rs` is not listed there -- it is mentioned only under "Implementation Notes" as call site #2. It must be modified to remove the `version_filter` argument from its call to `SbomService::list`. This is an out-of-scope file that would be flagged during Step 9 scope containment for user approval, but the modification is necessary for compilation and is directly implied by the task.

## Commit Message

```
refactor(sbom): remove version-based filtering from SBOM list endpoint

Remove the VersionMatches filter logic from SbomService::list and
remove the now-dead version_filter parameter from the function
signature. Update all 3 call sites (endpoint handler, search service,
integration tests) to remove the argument. Remove the
test_list_sboms_version_filtered test since the feature no longer exists.

Version filtering has been moved to the client side.

Implements TC-9207
```
