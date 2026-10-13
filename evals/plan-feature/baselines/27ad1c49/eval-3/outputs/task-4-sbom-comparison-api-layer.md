## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for SBOM comparison: TypeScript interfaces for the comparison response, an Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison request lifecycle. This provides the data-fetching foundation that the comparison page UI depends on.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add fetchSbomComparison(leftId: string, rightId: string) client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping fetchSbomComparison with left/right ID parameters and enabled guard

## Implementation Notes
TypeScript interfaces should match the backend response shape defined in Task 2. Add them to `src/api/models.ts` following the existing interface patterns already in that file.

The client function in `src/api/rest.ts` should follow the existing pattern (e.g., the fetchSboms function): use the Axios instance from `src/api/client.ts`, call `GET /api/v2/sbom/compare` with `left` and `right` query parameters, and return typed `SbomComparisonResult`.

The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern in `src/hooks/useSbomById.ts`: accept leftId and rightId parameters, use `useQuery` with a descriptive query key like `["sbom-comparison", leftId, rightId]`, and set `enabled: !!leftId && !!rightId` so the query only fires when both IDs are provided.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts` — existing fetch functions (fetchSboms, fetchAdvisories) as pattern reference
- `src/hooks/useSbomById.ts` — React Query hook pattern with ID parameter and enabled guard

## Acceptance Criteria
- [ ] TypeScript interfaces defined for all six diff categories in models.ts
- [ ] fetchSbomComparison function calls GET /api/v2/sbom/compare with correct query parameters
- [ ] useSbomComparison hook returns standard React Query result with loading/error/data states
- [ ] Hook does not fire the request when either SBOM ID is missing (enabled guard)

## Test Requirements
- [ ] Unit test: useSbomComparison returns comparison data when both IDs are provided (mock API with MSW)
- [ ] Unit test: useSbomComparison does not fetch when an ID is missing

## Dependencies
- Depends on: Task 2 — Add SBOM comparison service and endpoint (backend endpoint must exist for the client function to integrate with)
