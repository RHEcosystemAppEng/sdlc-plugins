## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, a typed API client function to call the backend comparison endpoint, and a React Query hook for data fetching. This establishes the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` -- add `fetchSbomComparison(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook `useSbomComparison(leftId, rightId)` that calls the comparison endpoint and returns the diff result

## Implementation Notes
- Follow the existing API layer pattern: interfaces in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- The TypeScript interfaces must match the backend API response shape exactly:
  - `SbomComparison` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
  - Each field typed as an array of the corresponding sub-interface
- The API client function should use the Axios instance from `src/api/client.ts` to call `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}`.
- The React Query hook should follow the pattern in `src/hooks/useSbomById.ts`: use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should be disabled (via `enabled` option) when either ID is missing.
- Per CONVENTIONS.md §API layer: follow the Axios client -> typed API functions -> React Query hooks pattern.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.
- Per CONVENTIONS.md §Naming: use camelCase for the hook function name and utility functions.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API client function pattern; follow the same Axios call structure for the comparison endpoint
- `src/hooks/useSbomById.ts` -- existing React Query hook for SBOM detail; follow the same `useQuery` pattern with query key and enabled option
- `src/hooks/useSboms.ts` -- existing React Query hook for SBOM list; reference for query key conventions
- `src/api/models.ts` -- existing TypeScript interfaces; follow the same naming and typing patterns

## Acceptance Criteria
- [ ] `SbomComparison` TypeScript interface is defined in `src/api/models.ts` with all six diff category arrays
- [ ] Each diff category has a corresponding TypeScript interface (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- [ ] `fetchSbomComparison(leftId, rightId)` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either leftId or rightId is undefined/empty
- [ ] Hook query key includes both SBOM IDs for proper cache invalidation

## Test Requirements
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (mock API with MSW)
- [ ] Unit test: `useSbomComparison` does not fire a request when leftId is undefined
- [ ] Unit test: `useSbomComparison` does not fire a request when rightId is undefined
- [ ] Unit test: verify TypeScript interfaces match the expected API response shape

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison endpoint with integration tests
