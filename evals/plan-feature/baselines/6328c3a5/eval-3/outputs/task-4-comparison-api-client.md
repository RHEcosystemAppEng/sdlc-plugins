## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, implement the REST client function to call the comparison endpoint, and create a React Query hook for data fetching. This task establishes the frontend data layer for the comparison feature, enabling the comparison page (Task 5) to fetch and display diff results.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` with `enabled` flag requiring both IDs

## Implementation Notes
Per CONVENTIONS.md §API Layer: follow the established pattern — types in `models.ts`, fetch functions in `rest.ts`, React Query hooks in `hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.

Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state; the hook should use `useQuery` with a query key that includes both SBOM IDs.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's React Query hook scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- Response shape:
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
- See `modules/fundamental/src/sbom/model/compare.rs` in trustify-backend for the authoritative type definitions.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**React Query hook pattern** (follow `src/hooks/useSbomById.ts` as reference):
```typescript
export const useSbomComparison = (leftId?: string, rightId?: string) => {
  return useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

**Axios client:** use the existing Axios instance from `src/api/client.ts` with base URL and auth interceptors.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` — existing fetch function; follow its pattern for the comparison fetch function
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call
- `src/hooks/useSbomById.ts` — existing React Query hook; follow its pattern for the comparison hook
- `src/api/models.ts` — existing TypeScript interfaces; follow naming and structure conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `models.ts`
- [ ] `fetchSbomComparison()` calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] `useSbomComparison` hook returns loading, error, and data states
- [ ] Hook is disabled (does not fire) when either SBOM ID is undefined
- [ ] Hook fires automatically when both SBOM IDs are provided
- [ ] Query key includes both SBOM IDs for proper cache invalidation

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` constructs the correct API URL with query parameters
- [ ] Unit test: `useSbomComparison` hook does not fire when leftId is undefined
- [ ] Unit test: `useSbomComparison` hook does not fire when rightId is undefined
- [ ] Unit test: `useSbomComparison` hook returns data on successful API response (using MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Create SBOM comparison REST endpoint with integration tests (cross-repo: defines the API contract)
