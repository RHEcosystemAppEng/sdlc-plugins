## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript interfaces, API client function, and React Query hook for the SBOM comparison endpoint. This provides the data-fetching layer that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the compareSboms API call

## Implementation Notes
- Follow the existing API client pattern in `src/api/rest.ts` where typed API functions call the Axios instance from `src/api/client.ts`.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` for React Query hook structure.
- TypeScript interfaces should match the backend API response shape exactly:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- The `compareSboms` function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`.
- The `useSbomComparison` hook should:
  - Accept `leftId` and `rightId` parameters
  - Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
  - Be disabled (`enabled: false`) when either ID is undefined/empty — the comparison is triggered explicitly by the user clicking "Compare", not automatically
  - Return the standard React Query result object (data, isLoading, error, refetch)
- Use `refetch()` pattern for explicit triggering rather than automatic fetching on mount.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six array fields (see interfaces above). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` (backend task 3).
- `GET /api/v2/sbom` — existing endpoint returning SBOM list, already covered by `useSboms` hook.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — demonstrates the API client function pattern with Axios
- `src/hooks/useSboms.ts` — demonstrates the React Query useQuery hook pattern for SBOM data
- `src/hooks/useSbomById.ts` — demonstrates the React Query hook pattern with a parameter-based query key
- `src/api/models.ts` — existing TypeScript interfaces showing naming conventions for API response types

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types exist in `src/api/models.ts`
- [ ] `compareSboms` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook exists and wraps the API call with React Query
- [ ] Hook is disabled by default when IDs are not provided
- [ ] Hook supports explicit triggering via refetch()

## Test Requirements
- [ ] Unit test: `compareSboms` function constructs the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook returns comparison data when both IDs are provided (with MSW mock)
- [ ] Unit test: `useSbomComparison` hook does not fetch when either ID is missing

## Verification Commands
- `npm run build` — TypeScript compiles without errors
- `npm run test` — all tests pass

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint (API contract must be finalized)
