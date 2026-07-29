# Implementation Plan: TC-9207 -- Remove version-based filter from SBOM list endpoint

## Overview

Task TC-9207 removes the version-based filtering logic from `SbomService::list`. The
`version_filter` parameter was used to apply a `VersionMatches` filter in the query
pipeline, but version filtering has been moved to the client side. The filter logic in
the method body must be removed, and crucially, the now-dead `version_filter` parameter
must be removed from the function signature and all call sites updated accordingly.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs` -- service method

**What changes:**

- Remove the `version_filter: &str` parameter from the `list` method signature. The
  current signature is:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      version_filter: &str,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

  The new signature becomes:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

- Remove the filtering logic in the method body that uses `version_filter` to apply a
  `VersionMatches` filter to the query. The rest of the query pipeline (search,
  pagination, transaction handling) remains intact.

**Why remove the parameter entirely:** Removing the filter logic from the body leaves
`version_filter` as a dead parameter -- it is accepted but never read. The correct fix
is to remove it from the signature, not rename it to `_version_filter`. See
`parameter-cleanup.md` for the rationale.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` -- endpoint handler

**What changes:**

- Remove the extraction of the `version` query parameter from the HTTP request. This
  likely involves removing a query parameter struct field or an extractor call that reads
  the `version` value from the request.
- Update the call to `SbomService::list` to no longer pass the version filter argument.
  The call changes from something like:

  ```rust
  sbom_service.list(search, paginated, &query.version, &tx).await
  ```

  to:

  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

- If there is a query parameter struct (e.g., `ListSbomQuery`) with a `version` field,
  remove that field.

**API impact:** `GET /api/v2/sbom` no longer accepts a `version` query parameter. Any
client sending `?version=...` will have the parameter silently ignored (standard HTTP
behavior for unknown query params in Axum).

### 3. `tests/api/sbom.rs` -- integration tests

**What changes:**

- Remove or gut the `test_list_sboms_version_filtered` test. Since version filtering is
  no longer supported by the endpoint, this test exercises removed functionality and
  must be deleted.
- Update any other test that calls `SbomService::list` directly (if tests call the
  service layer rather than going through HTTP) to remove the `version_filter` argument
  from those calls.
- Verify that remaining SBOM list tests (those that do not depend on version filtering)
  still compile and pass without changes.

### 4. `modules/search/src/service/mod.rs` -- search service (call site)

**What changes:**

- The search service calls `SbomService::list` with an empty version filter (`""`).
  Remove the empty-string argument from this call site. The call changes from something
  like:

  ```rust
  sbom_service.list(search, paginated, "", &tx).await
  ```

  to:

  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

## Dead Parameter Handling (Step 9)

After removing the filter logic from the `list` method body in sbom.rs, the
`version_filter` parameter becomes dead -- it is declared in the signature but never
referenced in the body. Per the skill's dead parameter detection protocol (Step 9):

1. **Identify the dead parameter**: `version_filter: &str` in `SbomService::list` has
   zero references in the function body after the filter logic is removed.
2. **Remove, do not rename**: The parameter must be removed from the signature entirely.
   Prefixing with an underscore (`_version_filter`) would suppress the compiler warning
   but leave unnecessary API surface. See `parameter-cleanup.md`.
3. **Update all 3 call sites**:
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- the REST endpoint handler
   - `modules/search/src/service/mod.rs` -- the search service
   - `tests/api/sbom.rs` -- integration tests
4. **Re-run tests** after removing the parameter and updating call sites to confirm
   nothing broke.

## Verification Steps

1. **Compile check**: Run `cargo build` to verify all call sites compile after removing
   the parameter.
2. **Test suite**: Run `cargo test` to verify:
   - The `test_list_sboms_version_filtered` test is removed and no longer referenced.
   - All other SBOM list tests pass without modification.
   - The search service tests (if any) pass with the updated call.
3. **CI checks**: If CONVENTIONS.md specifies CI commands (formatting, linting, clippy),
   run those to ensure no warnings are introduced.
4. **Scope containment**: Run `git diff --name-only` and verify only the 4 files listed
   above are modified. Flag any unexpected changes.

## Acceptance Criteria Verification

- [x] The `list` method in SbomService no longer filters by version -- filter logic
  removed from method body.
- [x] The `version` query parameter is no longer extracted or accepted by the endpoint --
  query param extraction and struct field removed from list.rs.
- [x] All call sites compile and pass without the version_filter argument -- all 3 call
  sites updated (list.rs handler, search/service/mod.rs, tests/api/sbom.rs).
- [x] Existing tests that don't depend on version filtering still pass -- verified by
  running `cargo test`.
