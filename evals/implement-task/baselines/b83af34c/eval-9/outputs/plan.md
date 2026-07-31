# Implementation Plan for TC-9207: Remove version-based filter from SBOM list endpoint

## Overview

This task removes the version-based filtering logic from `SbomService::list` and propagates the change through all layers: the service method, the endpoint handler, the search service caller, and the integration tests.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- Remove filtering logic from `list` method

**Current state:** The `list` method has this signature:

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

1. Remove the `version_filter: &str` parameter from the method signature entirely.
2. Remove all code in the method body that references `version_filter` -- specifically the `VersionMatches` filter application. Keep the rest of the query pipeline (search, pagination, transaction handling) intact.

**Resulting signature:**

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

**Why remove the parameter instead of underscore-prefixing:** The `version_filter` parameter becomes dead after removing the filtering logic. The correct action per Step 9's dead parameter detection guidance is removal, not renaming to `_version_filter`. Dead parameters pollute the API surface, mislead callers into thinking the argument is used, and accumulate technical debt. Every caller must still construct and pass a value that is silently ignored -- this is worse than removing it, because it hides the fact that the feature no longer exists. Underscore-prefixing silences the compiler warning but does not fix the design problem.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- Remove `version` query parameter extraction

**Current state:** The endpoint handler extracts a `version` query parameter from the HTTP request and passes it to `SbomService::list` as the `version_filter` argument.

**Changes:**

1. Remove the `version` field from the query parameter extraction struct (or remove the `Query<>` extractor for it if it is a standalone extractor).
2. Update the call to `SbomService::list` to remove the `version_filter` argument -- change from `service.list(search, paginated, version.as_str(), &tx)` to `service.list(search, paginated, &tx)`.
3. Remove any imports or types that were only used for version filtering (e.g., if there is a `VersionQuery` struct that is now empty or unused).

### 3. `modules/search/src/service/mod.rs` -- Remove empty version filter argument from `list` call

**Current state:** The search service calls `SbomService::list` with an empty string for the version filter (e.g., `sbom_service.list(search, paginated, "", &tx)`).

**Changes:**

1. Update the call to remove the empty-string argument -- change from `sbom_service.list(search, paginated, "", &tx)` to `sbom_service.list(search, paginated, &tx)`.

### 4. `tests/api/sbom.rs` -- Remove version-filter test, update remaining calls

**Current state:** Contains a `test_list_sboms_version_filtered` test that exercises the version filtering feature, plus other tests that call `SbomService::list` or the list endpoint with version filter arguments.

**Changes:**

1. Remove the `test_list_sboms_version_filtered` test entirely -- the feature it tests no longer exists.
2. Update all remaining calls to `SbomService::list` in other tests to remove the `version_filter` argument.
3. If any remaining tests pass a `version` query parameter to the endpoint URL (e.g., `GET /api/v2/sbom?version=1.0`), remove that query parameter from the test request.

## API Changes

- `GET /api/v2/sbom` -- The `version` query parameter is removed. Clients sending `?version=X` will have the parameter silently ignored by the framework (since it is no longer extracted), but the server-side filtering logic is gone. This is a breaking change for any client relying on server-side version filtering.

## Verification Steps

1. After all code changes, run `cargo test` to verify compilation and test passage.
2. Run `cargo clippy` (if listed in CONVENTIONS.md CI checks) to verify no new warnings.
3. Confirm that removing the test and updating call sites leaves zero compiler errors.
4. Verify scope containment: only the 4 files listed above should be modified. If `git diff --name-only` shows any other files, flag them for review.

## Order of Operations

1. Modify `sbom.rs` -- remove the filtering logic from the method body first.
2. At this point, the `version_filter` parameter is dead (no references in the body). Per Step 9 dead parameter detection: remove the parameter from the signature.
3. The compiler will now report errors at all 3 call sites. Fix each:
   a. `endpoints/list.rs` -- remove query param extraction and the argument.
   b. `search/service/mod.rs` -- remove the empty-string argument.
   c. `tests/api/sbom.rs` -- remove the argument from test calls and delete the version-filter-specific test.
4. Run `cargo test` to confirm all tests pass.
5. Run CI checks from CONVENTIONS.md if available.
