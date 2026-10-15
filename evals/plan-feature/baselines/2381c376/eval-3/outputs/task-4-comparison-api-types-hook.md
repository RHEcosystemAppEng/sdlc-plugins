## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task builds the API integration layer that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add fetchSbomComparison() client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
1. **TypeScript interfaces** in `src/api/models.ts`: add interfaces matching the backend response shape:
   ```
   SbomComparisonResult { added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }
   AddedPackage { name, version, license, advisory_count }
   RemovedPackage { name, version, license, advisory_count }
   VersionChange { name, left_version, right_version, direction }
   NewVulnerability { advisory_id, severity, title, affected_package }
   ResolvedVulnerability { advisory_id, severity, title, previously_affected_package }
   LicenseChange { name, left_license, right_license }
   ```

   Follow the existing interface patterns in `src/api/models.ts` for naming and structure conventions.

2. **API client function** in `src/api/rest.ts`: add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` that calls `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}` using the existing Axios instance from `src/api/client.ts`. Follow the pattern of existing functions like `fetchSboms()`.

3. **React Query hook** in `src/hooks/useSbomComparison.ts`: create `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that uses `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The query should be disabled when either ID is undefined (using `enabled: !!leftId && !!rightId`). Follow the pattern of `src/hooks/useSbomById.ts` for hook structure.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{"name": "...", "version": "...", "license": "...", "advisory_count": 0}],
    "removed_packages": [{"name": "...", "version": "...", "license": "...", "advisory_count": 0}],
    "version_changes": [{"name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade"}],
    "new_vulnerabilities": [{"advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..."}],
    "resolved_vulnerabilities": [{"advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..."}],
    "license_changes": [{"name": "...", "left_license": "...", "right_license": "..."}]
  }
  ```
  See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend for the endpoint definition.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md §API Layer: API client functions go in `src/api/rest.ts` with typed return values; React Query hooks go in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.

Per CONVENTIONS.md §Naming: hooks use camelCase naming (e.g., `useSbomComparison`), interfaces use PascalCase.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's camelCase hooks naming scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function; follow its pattern for Axios call structure and error handling
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; reuse for the comparison API call
- `src/hooks/useSbomById.ts` — existing single-entity React Query hook; follow its pattern for query key, enabled condition, and return type
- `src/api/models.ts` — existing TypeScript interfaces; follow naming and structure patterns

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface in `models.ts` matches the backend response shape with all six diff categories
- [ ] `fetchSbomComparison(leftId, rightId)` calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError, error }` from React Query
- [ ] Hook is disabled when either `leftId` or `rightId` is undefined
- [ ] TypeScript types are strict (no `any` types)

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct URL with left and right query parameters
- [ ] Unit test: `useSbomComparison` returns loading state initially
- [ ] Unit test: `useSbomComparison` returns data on successful API response
- [ ] Unit test: `useSbomComparison` does not fire when either ID is undefined
- [ ] Unit test: `useSbomComparison` returns error state on API failure

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add comparison endpoint and integration tests (backend API contract)
