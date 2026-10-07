# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Overview

The task removes the version-based filtering logic from `SbomService::list`. Once that filtering logic is removed, the `version_filter` parameter becomes dead -- it is no longer referenced anywhere in the function body. A dead parameter must be removed from the signature entirely, and all call sites must be updated to stop passing the argument.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService::list

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

1. Remove the `VersionMatches` filter logic from the method body that uses `version_filter` to constrain the query. Keep the rest of the query pipeline (search, pagination, transaction) intact.
2. Remove the `version_filter: &str` parameter from the function signature entirely. After removing the filter logic, `version_filter` is no longer referenced in the body -- it is a dead parameter. The correct action is removal, not renaming to `_version_filter`.

**Resulting signature:**

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- endpoint handler (call site 1 of 3)

**Changes:**

1. Remove the extraction of the `version` query parameter from the request (e.g., the `Query` extractor or manual param parsing that reads the `version` field).
2. Update the call to `SbomService::list` to stop passing the `version_filter` argument. The call should go from something like:

   ```rust
   service.list(search, paginated, &version, &tx).await
   ```

   to:

   ```rust
   service.list(search, paginated, &tx).await
   ```

3. If there is a query struct (e.g., `ListSbomsQuery`) that includes a `version` field, remove that field as well.

This also satisfies the API change: `GET /api/v2/sbom` no longer accepts the `version` query parameter.

### 3. `modules/search/src/service/mod.rs` -- search service (call site 2 of 3)

**Changes:**

1. Update the call to `SbomService::list` to remove the `version_filter` argument. The search service currently passes an empty version filter (e.g., `""`), which should simply be dropped:

   ```rust
   // Before
   sbom_service.list(search, paginated, "", &tx).await
   
   // After
   sbom_service.list(search, paginated, &tx).await
   ```

### 4. `tests/api/sbom.rs` -- integration tests (call site 3 of 3)

**Changes:**

1. Remove or update the `test_list_sboms_version_filtered` test entirely, since the version filtering feature is being removed. The test verifies behavior that no longer exists.
2. Update any other test calls to `SbomService::list` (or the endpoint) to remove the `version_filter` / `version` argument. Tests that exercise general SBOM listing (without version filtering) should continue to work after removing the argument.
3. If tests call the endpoint via HTTP with a `?version=...` query parameter, remove that parameter from the request URLs.

## Verification Steps

1. After making all changes, run `cargo check` to confirm compilation succeeds -- the Rust compiler will catch any remaining call sites that still pass the removed parameter.
2. Run `cargo test -p <crate-name>` for each affected crate:
   - The crate containing `modules/fundamental/src/sbom/service/sbom.rs`
   - The crate containing `modules/search/src/service/mod.rs`
   - The integration test crate in `tests/`
3. Verify that existing SBOM list tests (those not dependent on version filtering) still pass without changes.
4. Run any CI check commands from `CONVENTIONS.md` if present (formatting, linting, clippy).
5. Confirm `git diff --name-only` shows only the four files listed in the plan -- flag any out-of-scope modifications for user approval.

## Summary of Call Site Updates

| # | File | Current argument | Action |
|---|------|-----------------|--------|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `&version` (extracted from query params) | Remove query param extraction; remove argument from call |
| 2 | `modules/search/src/service/mod.rs` | `""` (empty string) | Remove argument from call |
| 3 | `tests/api/sbom.rs` | Various test values | Remove argument from calls; delete version-filter-specific test |
