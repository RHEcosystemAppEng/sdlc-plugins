## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response, create the Axios client function to call the comparison endpoint, and implement a React Query hook for data fetching — for feature TC-9003 (SBOM comparison view). This task builds the API integration layer that the comparison page (Task 4) will consume.

**Priority**: Critical (inherited from TC-9003)
**Fix Version**: RHTPA 1.5.0 (inherited from TC-9003)

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function using the Axios client

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that wraps the API call, enabled only when both IDs are provided

## Implementation Notes
Follow the existing API layer pattern where types are defined in `src/api/models.ts`, client functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`.

The TypeScript interfaces should match the backend response shape:
```typescript
export interface SbomComparisonResult {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

The API client function should follow the pattern in `src/api/rest.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`) using the Axios instance from `src/api/client.ts`.

The React Query hook should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key and the `enabled` option set to `!!leftId && !!rightId` so the query only fires when both SBOM IDs are available.

Per CONVENTIONS.md §Framework: use React 18 and TypeScript for all new code. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §State management: use React Query (TanStack Query) for the comparison data fetching — no Redux. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §API layer: define types in `src/api/models.ts`, client function in `src/api/rest.ts`, and React Query hook in `src/hooks/` following the existing file organization. Applies: task modifies `src/api/models.ts` and `src/api/rest.ts` matching the convention's API file scope.

Per CONVENTIONS.md §Naming: use camelCase for the hook function name (`useSbomComparison`) and utility functions (`compareSboms`). Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Testing: use Vitest + MSW for testing the hook and API function if tests are added. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript scope.

Per CONVENTIONS.md §Mutation pattern: the comparison is a read-only query (not a mutation), but if any cache invalidation is needed, use `queryClient.invalidateQueries()` pattern; never use `window.location.reload()`. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript scope.

## Reuse Candidates
- `src/api/client.ts` — existing Axios instance with base URL and auth interceptors; reuse for the comparison API call
- `src/api/rest.ts::fetchSboms` — existing API function; follow its pattern for the new `compareSboms` function
- `src/hooks/useSbomById.ts` — existing React Query hook for SBOM detail; follow its pattern for query key structure and enabled logic
- `src/api/models.ts` — existing TypeScript interfaces; add new interfaces alongside existing ones

## Acceptance Criteria
- [ ] `SbomComparisonResult` and related interfaces are exported from `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts` and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomComparison(leftId, rightId)` hook returns `{ data, isLoading, isError }` via React Query
- [ ] Hook is disabled (does not fire) when either ID is undefined or empty
- [ ] TypeScript interfaces match the backend response shape from the API specification

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook returns loading state initially and data after resolution (using MSW mock handler)
- [ ] Unit test: `useSbomComparison` does not fire when leftId is undefined
- [ ] Unit test: `useSbomComparison` does not fire when rightId is undefined

## Dependencies
- Depends on: Task 2 — SBOM comparison endpoint and integration tests (cross-repo: trustify-backend)
