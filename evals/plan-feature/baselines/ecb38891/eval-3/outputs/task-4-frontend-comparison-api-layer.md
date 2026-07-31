## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response types, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task establishes the data-fetching plumbing that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `fetchSbomComparison` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- **TypeScript interfaces** in `src/api/models.ts` — add interfaces matching the backend response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  interface AddedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface RemovedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
  interface NewVulnerability { advisory_id: string; severity: string; title: string; affected_package: string; }
  interface ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
  interface LicenseChange { name: string; left_license: string; right_license: string; }
  ```
- **API client function** in `src/api/rest.ts` — follow the pattern of existing functions (`fetchSboms`, `fetchAdvisories`):
  ```typescript
  export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
    client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
  ```
  Use the Axios instance from `src/api/client.ts` which includes base URL and auth interceptors.
- **React Query hook** in `src/hooks/useSbomComparison.ts` — follow the pattern of existing hooks (`useSboms.ts`, `useSbomById.ts`):
  - Use `useQuery` from TanStack Query
  - Query key: `["sbomComparison", leftId, rightId]`
  - `enabled` option: only fetch when both `leftId` and `rightId` are defined
  - Return the query result object
- Use camelCase for hook and function names per project conventions.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend, created in Task 2)
- `GET /api/v2/sbom` — existing endpoint, returns list of SBOMs. Used by the existing `useSboms` hook for the SBOM selector dropdowns.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern (Axios GET call with typed response)
- `src/api/rest.ts::fetchAdvisories` — reference for API client function with query parameters
- `src/hooks/useSboms.ts` — reference for React Query hook pattern (useQuery, query key, return type)
- `src/hooks/useSbomById.ts` — reference for React Query hook with parameter-dependent query key
- `src/api/models.ts` — reference for TypeScript interface naming and export patterns
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; import and use directly

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-type interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function is exported from `src/api/rest.ts` and returns `Promise<SbomComparisonResult>`
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook only fires the query when both IDs are provided (enabled guard)
- [ ] Hook returns loading, error, and data states consistent with other hooks
- [ ] TypeScript interfaces match the backend response shape exactly

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct URL with left and right query params
- [ ] Unit test: `useSbomComparison` returns loading state initially, then data after resolution
- [ ] Unit test: `useSbomComparison` does not fire query when either ID is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Backend comparison endpoint (API contract must exist)
