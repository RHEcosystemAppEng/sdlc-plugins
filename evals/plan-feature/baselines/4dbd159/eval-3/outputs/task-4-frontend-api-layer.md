# Task 4 — Add SBOM comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Target Branch
main

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and the React Query hook that wraps the API call. This provides the data-fetching layer that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the `compareSboms` API call with `enabled` flag to defer execution until both IDs are provided

## Implementation Notes
- **TypeScript interfaces** must match the backend response shape exactly:
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
- Follow the existing API function pattern in `src/api/rest.ts` — functions use the Axios client from `src/api/client.ts` and return typed promises (e.g., `fetchSboms()`, `fetchAdvisories()`).
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — hooks call `useQuery` with a query key and query function.
- The hook should accept `leftId` and `rightId` parameters and set `enabled: !!leftId && !!rightId` to prevent the query from firing until both IDs are selected.
- Use a descriptive query key like `["sbom-comparison", leftId, rightId]` for cache management.

  **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Follow the API function pattern (Axios GET call, typed response)
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — Follow the React Query hook pattern (useQuery with query key)
- `src/hooks/useSbomById.ts` — Follow the single-entity query pattern with dynamic parameters
- `src/api/models.ts` — Follow existing interface definition patterns and naming conventions

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-type interfaces are defined in `models.ts`
- [ ] `compareSboms()` function exists in `rest.ts` and calls `GET /api/v2/sbom/compare` with query parameters
- [ ] `useSbomComparison` hook exists and uses React Query with proper `enabled` flag
- [ ] Hook does not fire the API call until both SBOM IDs are provided
- [ ] Query key includes both SBOM IDs for proper cache invalidation

## Test Requirements
- [ ] Unit test: `useSbomComparison` does not fetch when leftId or rightId is undefined
- [ ] Unit test: `useSbomComparison` fetches and returns typed data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests (backend endpoint must exist)
