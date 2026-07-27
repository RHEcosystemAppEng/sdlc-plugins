# Task 4: Add comparison API types and React Query hook

**Summary**: Add TypeScript types and React Query hook for comparison API

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response types, an API client function to call the comparison endpoint, and a React Query hook (`useSbomComparison`) that wraps the API call with loading, error, and caching behavior. This provides the data-fetching layer that the SbomComparePage (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook that calls `fetchSbomComparison` and returns `{ data, isLoading, isError, error }`

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — each interface should use camelCase property names matching the snake_case JSON response via the existing Axios response transformation or explicit mapping.
- Follow the existing API function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`) — use the shared Axios instance from `src/api/client.ts` which handles base URL and auth interceptors.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` — use `useQuery` from React Query with a descriptive query key (e.g., `["sbom-comparison", leftId, rightId]`). The hook should only enable the query when both `leftId` and `rightId` are provided (use the `enabled` option).
- The hook should accept parameters for both SBOM IDs and return standard React Query state (`data`, `isLoading`, `isError`, `error`).

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
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
  (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the authoritative struct definitions)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function; follow its pattern for the comparison fetch function
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interfaces for API response types; follow naming conventions
- `src/hooks/useSboms.ts` — existing React Query hook; follow its pattern for query key naming, enabled/disabled logic, and return type

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult` and all sub-types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function is added to `src/api/rest.ts` and correctly calls `GET /api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] `useSbomComparison` hook is created in `src/hooks/useSbomComparison.ts` using React Query's `useQuery`
- [ ] The hook disables the query when either SBOM ID is missing (no API call until both are selected)
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns loading state when query is in progress
- [ ] Unit test: `useSbomComparison` hook returns comparison data when the API call succeeds (mock API response via MSW)
- [ ] Unit test: `useSbomComparison` hook does not fire the query when `leftId` or `rightId` is undefined
- [ ] Unit test: `fetchSbomComparison` constructs the correct URL with query parameters

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add comparison endpoint (defines the API contract this task consumes)
