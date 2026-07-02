## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, a typed client function to call the comparison endpoint, and a React Query hook that manages the comparison query lifecycle. This provides the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` function using the Axios client instance

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook that wraps `compareSboms()` with query key `["sbom-comparison", leftId, rightId]`, enabled only when both IDs are provided

## Implementation Notes
Interfaces in `models.ts` must match the backend response shape:
```typescript
export interface SbomComparison {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}

export interface AddedPackage {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}
// ... similar for other sub-types
```

The client function in `rest.ts` follows the existing pattern (e.g., `fetchSboms()`):
```typescript
export async function compareSboms(leftId: string, rightId: string): Promise<SbomComparison> {
  const response = await client.get<SbomComparison>("/api/v2/sbom/compare", {
    params: { left: leftId, right: rightId },
  });
  return response.data;
}
```

The React Query hook follows the existing hook pattern in `src/hooks/useSboms.ts`:
```typescript
export function useSbomComparison(leftId: string | undefined, rightId: string | undefined) {
  return useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => compareSboms(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
}
```

Per CONVENTIONS.md §API layer: typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state; no Redux. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (import for client function)
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow
- `src/hooks/useSbomById.ts` — similar single-entity query hook pattern

## Acceptance Criteria
- [ ] TypeScript interfaces compile and match the backend response shape exactly
- [ ] `compareSboms()` calls `GET /api/v2/sbom/compare` with left and right query params
- [ ] `useSbomComparison` hook returns loading/error/data states correctly
- [ ] Hook is disabled (does not fire) when either leftId or rightId is undefined
- [ ] Hook refetches when leftId or rightId changes

## Test Requirements
- [ ] Unit test: `compareSboms()` sends correct request to /api/v2/sbom/compare with query params
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs provided (using MSW mock)
- [ ] Unit test: `useSbomComparison` hook does not fire when an ID is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch (create-branch bookend)
- Depends on: Task 3 — Backend comparison endpoint (API contract must be available)
