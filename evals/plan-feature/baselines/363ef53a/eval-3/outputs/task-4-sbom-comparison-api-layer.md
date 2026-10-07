## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript API layer for the SBOM comparison feature: type definitions for the comparison API response, an Axios client function to call the backend comparison endpoint, and a React Query hook for data fetching. This provides the data-fetching foundation that the comparison page UI (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string)` client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that wraps the client function

## Implementation Notes
Follow the existing API layer pattern: types in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.

Per the repo's API layer convention: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API file scope.

Per the repo's naming convention: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook file scope.

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
  See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend (Task 3).

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Type definitions** (matching the backend response shape from Figma design context):
```typescript
interface AddedPackage { name: string; version: string; license: string; advisory_count: number; }
interface RemovedPackage { name: string; version: string; license: string; advisory_count: number; }
interface VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
interface NewVulnerability { advisory_id: string; severity: string; title: string; affected_package: string; }
interface ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
interface LicenseChange { name: string; left_license: string; right_license: string; }
```

**Client function pattern** (following `fetchSboms()` in `rest.ts`):
```typescript
export const fetchSbomComparison = (leftId: string, rightId: string) =>
  client.get<SbomComparisonResult>(`/api/v2/sbom/compare`, {
    params: { left: leftId, right: rightId },
  }).then((res) => res.data);
```

**Hook pattern** (following `useSboms.ts`):
```typescript
export const useSbomComparison = (leftId?: string, rightId?: string) =>
  useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
```

The hook should be disabled when either ID is undefined (before the user selects both SBOMs or clicks Compare).

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function demonstrating the Axios GET pattern with typed response
- `src/api/models.ts` — existing TypeScript interfaces for API response types (e.g., SBOM, Advisory types)
- `src/hooks/useSboms.ts` — existing React Query hook pattern for SBOM list fetching
- `src/hooks/useSbomById.ts` — existing React Query hook with ID parameter and enabled flag
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all six comparison categories are defined in `models.ts`
- [ ] `fetchSbomComparison` function exists in `rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook returns query result with loading, error, and data states
- [ ] Hook is disabled (does not fire) when either SBOM ID is undefined
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns loading state initially
- [ ] Unit test: `useSbomComparison` hook returns data on successful API response (use MSW mock)
- [ ] Unit test: `useSbomComparison` hook does not fire when IDs are undefined
- [ ] Unit test: `useSbomComparison` hook returns error state on API failure

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
