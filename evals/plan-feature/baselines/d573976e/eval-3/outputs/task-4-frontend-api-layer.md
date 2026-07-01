# Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and the React Query hook that components will use to trigger and consume comparison results. This task builds the data-fetching layer that the comparison page (Task 5) depends on.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call with `left` and `right` IDs

## Implementation Notes
- Follow the existing type definition pattern in `src/api/models.ts` — interfaces use PascalCase and match the API response shape exactly.
- Follow the existing API function pattern in `src/api/rest.ts` — functions use the Axios client from `src/api/client.ts` and return typed promises. Example: `fetchSboms()`.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — hooks use `useQuery` from React Query with a descriptive query key.
- The hook should accept `leftId` and `rightId` parameters and only enable the query when both are provided (use `enabled: !!leftId && !!rightId`).
- The query key should be `["sbom-comparison", leftId, rightId]` to ensure cache invalidation when either ID changes.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  Defined in backend: `modules/fundamental/src/sbom/model/comparison.rs`

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for the comparison fetch function
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for the comparison hook
- `src/hooks/useSbomById.ts` — existing single-item query hook pattern (similar enabled/disabled pattern)
- `src/api/client.ts` — Axios instance with base URL and auth interceptors to use for the API call

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories match the backend API response shape
- [ ] API client function `fetchSbomComparison` calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] React Query hook `useSbomComparison` returns query state (data, isLoading, isError) for the comparison
- [ ] Hook only fires the query when both left and right IDs are provided

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook verifying it calls the correct endpoint with left and right params
- [ ] Unit test verifying the hook does not fire when either ID is missing (enabled: false)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
