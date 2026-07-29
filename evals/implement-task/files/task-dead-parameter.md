<!-- SYNTHETIC TEST DATA — task that removes code using a function parameter, leaving the parameter dead -->

# Mock Jira Task

**Key**: TC-9207
**Summary**: Remove version-based filter from SBOM list endpoint
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Remove the version-based filtering logic from the SBOM list endpoint. The `version_filter`
parameter in `SbomService::list` was used to filter SBOMs by a specific version string,
but this filter is no longer needed — version filtering has been moved to the client side.
Remove the filter logic from the service method body.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — remove version-based filtering logic from the `list` method
- `modules/fundamental/src/sbom/endpoints/list.rs` — remove the `version` query parameter extraction and stop passing it to the service method
- `tests/api/sbom.rs` — remove or update the `test_list_sboms_version_filtered` test

## Files to Create
- (none)

## API Changes
- `GET /api/v2/sbom` — CHANGED: remove `version` query parameter support

## Implementation Notes
- The `SbomService::list` method in `modules/fundamental/src/sbom/service/sbom.rs` currently has this signature:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      version_filter: &str,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- The `version_filter` parameter is used in the method body to apply a `VersionMatches` filter to the query. Remove the filter logic but keep the rest of the query pipeline intact.
- The endpoint handler in `modules/fundamental/src/sbom/endpoints/list.rs` extracts the `version` query param and passes it to `SbomService::list`. After the service method no longer accepts `version_filter`, the handler should stop extracting and passing it.
- There are 3 call sites for `SbomService::list`:
  1. `modules/fundamental/src/sbom/endpoints/list.rs` — the REST endpoint handler
  2. `modules/search/src/service/mod.rs` — the search service calls `list` with an empty version filter
  3. `tests/api/sbom.rs` — integration tests pass various version filter values

## Acceptance Criteria
- [ ] The `list` method in SbomService no longer filters by version
- [ ] The `version` query parameter is no longer extracted or accepted by the endpoint
- [ ] All call sites compile and pass without the version_filter argument
- [ ] Existing tests that don't depend on version filtering still pass

## Test Requirements
- [ ] Remove or update `test_list_sboms_version_filtered` since the feature is removed
- [ ] Verify other SBOM list tests still pass without changes

## Dependencies
- Depends on: None
