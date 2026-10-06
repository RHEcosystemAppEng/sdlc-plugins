## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This establishes the frontend data layer for the comparison UI without any visual components.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
Add the following TypeScript interfaces to `src/api/models.ts`, matching the backend response shape:
- `AddedPackage { name: string; version: string; license: string; advisory_count: number }`
- `RemovedPackage { name: string; version: string; license: string; advisory_count: number }`
- `VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }`
- `NewVulnerability { advisory_id: string; severity: string; title: string; affected_package: string }`
- `ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string }`
- `LicenseChange { name: string; left_license: string; right_license: string }`
- `SbomComparisonResult { added_packages: AddedPackage[]; removed_packages: RemovedPackage[]; version_changes: VersionChange[]; new_vulnerabilities: NewVulnerability[]; resolved_vulnerabilities: ResolvedVulnerability[]; license_changes: LicenseChange[] }`

Add the API client function in `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`:
```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
```

Create the React Query hook in `src/hooks/useSbomComparison.ts` following the pattern of `src/hooks/useSbomById.ts`:
```typescript
export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) =>
  useQuery({ queryKey: ["sbom-comparison", leftId, rightId], queryFn: () => compareSboms(leftId!, rightId!), enabled: !!leftId && !!rightId });
```

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md (Key Conventions) -- API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API layer scope.

Per CONVENTIONS.md (Key Conventions) -- Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function; follow the same Axios pattern for the comparison call
- `src/hooks/useSbomById.ts` — existing React Query hook; follow the same `useQuery` pattern for the comparison hook
- `src/api/models.ts` — existing TypeScript interfaces; follow the same interface definition pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use this client for the API call

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories defined in `src/api/models.ts`
- [ ] `SbomComparisonResult` interface defined aggregating all diff categories
- [ ] `compareSboms(leftId, rightId)` function added to `src/api/rest.ts`
- [ ] `useSbomComparison` hook created in `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either leftId or rightId is undefined
- [ ] Hook uses the correct query key for cache management
- [ ] All types are exported and importable by page components

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct API endpoint with left and right query params
- [ ] Unit test: `useSbomComparison` returns loading state when query is in progress
- [ ] Unit test: `useSbomComparison` returns data when query succeeds
- [ ] Unit test: `useSbomComparison` is disabled when leftId or rightId is undefined

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run --reporter=verbose -- useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint (backend API contract dependency)
