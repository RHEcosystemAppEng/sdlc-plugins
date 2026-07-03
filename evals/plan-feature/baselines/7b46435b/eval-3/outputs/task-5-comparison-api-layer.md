## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response types, an API client function, and a React Query hook. This task establishes the data-fetching infrastructure that the comparison page component will consume.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces for comparison response types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook for the comparison endpoint

## Implementation Notes
- Add interfaces to `src/api/models.ts` following the existing pattern alongside `SbomSummary` and `AdvisoryDetails`:
  ```typescript
  export interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- Add the API function to `src/api/rest.ts` using the Axios client from `src/api/client.ts`:
  ```typescript
  export const fetchSbomComparison = (leftId: string, rightId: string) =>
    client.get<SbomComparisonResult>('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } });
  ```
- Create the React Query hook in `src/hooks/useSbomComparison.ts` following the pattern in `src/hooks/useSbomById.ts`. The hook should only fire when both IDs are defined (use the `enabled` option):
  ```typescript
  export const useSbomComparison = (leftId?: string, rightId?: string) =>
    useQuery(['sbom-comparison', leftId, rightId], () => fetchSbomComparison(leftId!, rightId!), {
      enabled: !!leftId && !!rightId,
    });
  ```
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend and `modules/fundamental/src/sbom/endpoints/compare.rs` for the handler)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- Per CONVENTIONS.md (Key Conventions) -- API layer: typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's API layer scope.
- Per CONVENTIONS.md (Key Conventions) -- Naming: camelCase for hooks and utilities. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's naming scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer.

## Reuse Candidates
- `src/api/models.ts` -- existing TypeScript interfaces for API types (pattern reference)
- `src/api/rest.ts::fetchSboms` -- existing API client function pattern (Axios GET with typed response)
- `src/hooks/useSbomById.ts` -- React Query hook pattern with `useQuery` and `enabled` option
- `src/hooks/useSboms.ts` -- React Query hook for list endpoint (query key pattern)
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined and exported from `models.ts`
- [ ] API client function `fetchSbomComparison` makes GET request to `/api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] React Query hook `useSbomComparison` returns comparison data when both SBOM IDs are provided
- [ ] Hook does not fire when either SBOM ID is undefined (enabled: false)

## Test Requirements
- [ ] TypeScript compilation succeeds with no type errors
- [ ] Hook unit test: verify query is disabled when IDs are undefined
- [ ] Hook unit test: verify query fires with correct endpoint when both IDs are provided

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
