# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Task Summary

Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter`
parameter in `SbomService::list` is used to apply a `VersionMatches` filter to the query.
Version filtering has been moved to the client side, so the server-side filter logic must
be removed. Once the filter logic is gone, `version_filter` becomes a dead parameter and
must be removed from the signature and all call sites.

## Project Configuration Validation

- Repository Registry: trustify-backend, Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

All required sections are present. Proceeding.

## Target Branch

main

## Files to Modify (3 files)

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- Service method

**Current state:**

The `SbomService::list` method has the signature:

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    version_filter: &str,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

The method body uses `version_filter` to apply a `VersionMatches` filter to the query
pipeline.

**Changes:**

1. **Remove the filtering logic**: delete the lines in the method body that use
   `version_filter` to construct or apply a `VersionMatches` filter. Keep the rest
   of the query pipeline intact (pagination, search, other filters, sorting).

2. **Remove the `version_filter` parameter**: after removing the filter logic, the
   `version_filter` parameter is no longer referenced anywhere in the method body.
   Per the dead parameter detection rule in Step 9 of implement-task, the correct
   fix is **removal** from the signature, not renaming to `_version_filter`. Remove
   the `version_filter: &str` parameter entirely.

3. **Clean up imports**: if `VersionMatches` or related types are no longer used
   anywhere in this file after removing the filter logic, remove the corresponding
   `use` statements.

**Resulting signature:**

```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- REST endpoint handler

**Current state:**

The endpoint handler for `GET /api/v2/sbom` extracts a `version` query parameter from
the request and passes it to `SbomService::list` as the `version_filter` argument.

**Changes:**

1. **Remove the `version` query parameter extraction**: delete the code that extracts
   the `version` query parameter from the Axum request (e.g., `Query` extractor struct
   field, or inline extraction).

2. **Update the `SbomService::list` call**: remove the `version_filter` argument from
   the call. The call changes from:

   ```rust
   service.list(search, paginated, &version, &tx).await
   ```

   to:

   ```rust
   service.list(search, paginated, &tx).await
   ```

3. **Clean up the query parameter struct**: if the endpoint uses a dedicated struct for
   query parameters (e.g., `ListSbomsQuery`), remove the `version` field from it.

4. **Clean up imports**: remove any imports that are no longer needed after removing
   the version parameter handling.

### 3. `tests/api/sbom.rs` -- Integration tests

**Current state:**

Contains `test_list_sboms_version_filtered` test that exercises version filtering.
Other SBOM list tests pass various version filter values to `SbomService::list`.

**Changes:**

1. **Remove `test_list_sboms_version_filtered`**: delete the entire test function since
   the feature it tests is being removed.

2. **Update remaining test call sites**: any other test that calls `SbomService::list`
   must have the `version_filter` argument removed. For example:

   ```rust
   // Before
   service.list(search, paginated, "", &tx).await
   // After
   service.list(search, paginated, &tx).await
   ```

3. **Remove version-related test HTTP requests**: if any integration tests send the
   `version` query parameter in HTTP requests to `GET /api/v2/sbom?version=...`,
   remove those query parameters. Tests that verify listing without version filtering
   should continue to work without changes to the URL.

## Call Site Summary (3 call sites)

| # | File | Current call | Updated call |
|---|------|-------------|--------------|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `service.list(search, paginated, &version, &tx).await` | `service.list(search, paginated, &tx).await` |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(search, paginated, "", &tx).await` | `sbom_service.list(search, paginated, &tx).await` |
| 3 | `tests/api/sbom.rs` | `service.list(search, paginated, "<value>", &tx).await` | `service.list(search, paginated, &tx).await` |

## Handling the `version_filter` Parameter After Removing Filtering Logic

The implement-task skill's Step 9 (Dead parameter detection) prescribes the following
process:

1. **Identify candidates**: after removing the `VersionMatches` filter logic from the
   method body, the `version_filter` parameter has zero remaining references in the
   function body. It is a dead parameter.

2. **Detection method**: the parameter has zero references in the function body after
   the diff is applied. The Rust compiler would also emit an `unused variable` warning
   for `version_filter`, confirming it is dead.

3. **Correct fix -- removal, not renaming**: the skill explicitly states "The correct
   fix is removal, not renaming." Do NOT prefix with underscore (`_version_filter`).
   Remove `version_filter: &str` from the method signature entirely.

4. **Find all call sites**: use `find_referencing_symbols` on `SbomService::list` (via
   the `serena_backend` Serena instance) or Grep for `\.list(` across the codebase to
   locate all 3 call sites.

5. **Update every caller**: remove the corresponding argument from every call site.
   The `version_filter` is the third positional argument (after `search` and
   `paginated`), so remove the third argument and shift `tx` to become the third.

6. **Re-run tests**: after all changes, run `cargo test` to confirm compilation and
   test passage.

## API Changes

- `GET /api/v2/sbom` -- the `version` query parameter is no longer accepted. Clients
  passing `?version=...` will have the parameter silently ignored (standard Axum
  behavior for unrecognized query parameters) or rejected if the endpoint uses strict
  query parameter validation. The version filtering responsibility is now on the client
  side.

## Verification Steps

1. **Compile check**: `cargo check` -- confirms all call sites are updated and the
   removed parameter does not cause compilation errors.
2. **Test run**: `cargo test -p trustify-fundamental` and `cargo test -p trustify-search`
   (or equivalent crate names resolved via `cargo metadata`) to verify the fundamental
   and search modules compile and pass tests.
3. **Integration tests**: run the full test suite in `tests/api/sbom.rs` to confirm
   non-version-related SBOM tests still pass.
4. **Scope containment**: verify `git diff --name-only` only shows the 3 files listed
   in Files to Modify.
5. **Dead parameter re-check**: after all changes, re-scan modified functions for any
   remaining unused parameters.

## Commit Plan

```
refactor(sbom): remove version-based filtering from SBOM list endpoint

Remove the VersionMatches filter logic from SbomService::list and the
version query parameter from the GET /api/v2/sbom endpoint. Version
filtering has been moved to the client side.

Remove the now-dead version_filter parameter from the list method
signature and update all 3 call sites (endpoint handler, search service,
integration tests). Delete the test_list_sboms_version_filtered test.

Implements TC-9207
```
