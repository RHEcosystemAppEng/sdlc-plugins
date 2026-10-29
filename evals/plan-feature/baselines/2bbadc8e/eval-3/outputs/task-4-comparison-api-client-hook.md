## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the API client function and React Query hook for the SBOM comparison endpoint. This task creates the TypeScript interfaces for the comparison response, the Axios-based API client function, and the React Query hook that frontend components will use to fetch comparison data. This is the API integration layer — no UI components are created in this task.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for SbomComparison and its sub-types (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call with query key management

## Implementation Notes
Follow the existing API layer pattern:
1. TypeScript interfaces in `src/api/models.ts` (see existing interfaces for SBOMs and advisories)
2. API client function in `src/api/rest.ts` using the shared Axios instance from `src/api/client.ts`
3. React Query hook in `src/hooks/` following the pattern of `useSboms.ts` and `useSbomById.ts`

**Backend API contract:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
  See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the authoritative struct definitions.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

The React Query hook should:
- Accept `leftId` and `rightId` parameters
- Use a query key like `["sbom-comparison", leftId, rightId]`
- Only enable the query when both IDs are provided (`enabled: !!leftId && !!rightId`)
- Return standard React Query result (data, isLoading, isError, error)

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function; follow its pattern for Axios GET calls with the shared client
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors; import and use for the comparison API call
- `src/hooks/useSbomById.ts` — existing React Query hook for single SBOM fetch; follow its pattern for query key management and enabled logic
- `src/api/models.ts` — existing TypeScript interfaces; follow naming conventions for new comparison types

## Acceptance Criteria
- [ ] `SbomComparison` interface and all sub-type interfaces are defined in `models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` makes a GET request to `/api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomComparison` hook returns typed React Query result with `SbomComparison` data
- [ ] Hook is disabled (does not fire) when either `leftId` or `rightId` is undefined/empty
- [ ] Hook uses a unique query key that includes both SBOM IDs for proper cache management

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct URL with both query parameters
- [ ] Unit test: `useSbomComparison` returns loading state initially and data after resolution
- [ ] Unit test: `useSbomComparison` does not fire the query when leftId is undefined
- [ ] Unit test: `useSbomComparison` does not fire the query when rightId is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
