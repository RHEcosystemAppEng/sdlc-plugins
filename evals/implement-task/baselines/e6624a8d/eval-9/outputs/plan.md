# Implementation Plan for TC-9207

## Summary

Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter`
parameter is no longer needed because version filtering has been moved to the client side.
After removing the filter logic from the method body, the `version_filter` parameter itself
becomes dead and must be removed from the function signature and all call sites.

## Project Configuration Validation

The project's CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with `rust-analyzer`

## Task Parsing (from TC-9207)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new PR flow)

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**What to change:**

- Locate the `list` method on `SbomService` with this current signature:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      version_filter: &str,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- Remove the `version_filter: &str` parameter from the signature entirely.
- In the method body, remove the `VersionMatches` filter application that uses `version_filter`.
  Keep the rest of the query pipeline (search, pagination, transaction handling) intact.
- The updated signature becomes:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

**Rationale:** The `version_filter` parameter is only used to apply a `VersionMatches` filter
in the query pipeline. Removing the filter logic makes the parameter dead. Per the skill's
dead parameter detection guidance (Step 9), the correct fix is removal, not renaming to
`_version_filter`.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs`

**What to change:**

- Remove the `version` query parameter extraction from the handler function. This likely
  involves removing a field from a query parameter struct or removing a manual extraction
  of the `version` query string parameter.
- Stop passing the `version_filter` argument to `SbomService::list`. The call site changes
  from something like:
  ```rust
  service.list(search, paginated, &query.version, &tx).await
  ```
  to:
  ```rust
  service.list(search, paginated, &tx).await
  ```
- If there is a query parameter struct (e.g., `ListSbomsQuery`) that includes a `version`
  field, remove that field from the struct definition.

**Rationale:** The endpoint no longer needs to accept or forward the `version` query parameter
since the service method no longer uses it. The `GET /api/v2/sbom` endpoint's API contract
changes: the `version` query parameter is no longer supported.

### 3. `modules/search/src/service/mod.rs`

**What to change:**

- This file calls `SbomService::list` with an empty version filter (e.g., `""`). Remove the
  empty string argument from the call site. The call changes from something like:
  ```rust
  sbom_service.list(search, paginated, "", &tx).await
  ```
  to:
  ```rust
  sbom_service.list(search, paginated, &tx).await
  ```

**Rationale:** This is a call site that must be updated after removing the `version_filter`
parameter from the service method signature. The empty string argument confirms that this
caller never used the version filtering feature.

### 4. `tests/api/sbom.rs`

**What to change:**

- **Remove** `test_list_sboms_version_filtered` entirely, since the feature it tests no
  longer exists.
- **Update** any remaining test call sites that invoke `SbomService::list` directly (if
  integration tests call the service method rather than going through HTTP). Remove the
  `version_filter` argument from those calls.
- **Verify** that other SBOM list tests (e.g., tests for pagination, search, sorting) do
  not depend on version filtering and continue to pass without changes.

**Rationale:** The test covers removed functionality and will fail to compile after the
parameter is removed. Other tests should be unaffected since they test orthogonal features.

## API Changes

- `GET /api/v2/sbom` -- CHANGED: the `version` query parameter is no longer accepted.
  Clients sending `?version=X` will have the parameter silently ignored (or rejected,
  depending on the framework's query parameter handling). Client-side version filtering
  replaces this server-side capability.

## Documentation Impact

- Check `docs/api.md` (referenced in the project CLAUDE.md) for documentation of the
  `GET /api/v2/sbom` endpoint. If the `version` query parameter is documented there,
  remove it.
- Check `README.md` and `CONVENTIONS.md` at the repository root for any references to
  version filtering on the SBOM list endpoint.

## Verification Strategy

1. Run `cargo check` to verify all code compiles after removing the parameter and updating
   call sites.
2. Run `cargo test` to verify all tests pass, including that the removed test no longer
   causes compilation errors.
3. Run any CI check commands from `CONVENTIONS.md` if present.
4. Perform scope containment check: verify `git diff --name-only` only shows the four
   files listed above.
5. Run dead parameter detection on the modified functions to confirm no additional dead
   parameters were introduced.

## Commit Plan

```
refactor(sbom): remove version-based filtering from list endpoint

Version filtering has been moved to the client side. Remove the
VersionMatches filter logic from SbomService::list, remove the
now-dead version_filter parameter from the method signature, update
all three call sites, and remove the version-specific integration test.

Implements TC-9207
```

With `--trailer="Assisted-by: Claude Code"`.

## PR Plan

- Base branch: `main`
- Head branch: `TC-9207`
- Title: `refactor(sbom): remove version-based filtering from list endpoint`
- Description references Jira issue with clickable link: `Implements [TC-9207](<webUrl>)`
