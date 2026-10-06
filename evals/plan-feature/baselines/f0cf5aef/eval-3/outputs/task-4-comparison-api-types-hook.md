## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task establishes the frontend data layer for the comparison feature, following the existing API layer conventions.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Implementation Notes
Per the frontend API layer convention: typed API functions live in `src/api/rest.ts` and React Query hooks live in `src/hooks/`. Follow the existing `fetchSboms()` / `useSboms` pattern.
Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.

Per the frontend naming convention: camelCase for hooks and utilities.
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

  interface AddedPackage {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface RemovedPackage {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  interface NewVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  interface ResolvedVulnerability {
    advisory_id: string;
    severity: string;
    title: string;
    previously_affected_package: string;
  }

  interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the source structs)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Hook implementation:**
- Use `useQuery` from React Query with a query key like `["sbom-comparison", leftId, rightId]`
- The hook should accept `leftId` and `rightId` as parameters
- Enable the query only when both IDs are provided (use `enabled: !!leftId && !!rightId`)
- Follow the pattern established in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern to follow
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (use this for the API call)
- `src/api/models.ts` — existing TypeScript interfaces for API response types
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for query key structure and options
- `src/hooks/useSbomById.ts` — existing single-resource hook pattern

## Acceptance Criteria
- [ ] All six TypeScript interfaces match the backend response shape exactly
- [ ] `fetchSbomComparison` calls `GET /api/v2/sbom/compare` with correct query parameters
- [ ] `fetchSbomComparison` uses the shared Axios client instance from `src/api/client.ts`
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError, error }` matching React Query conventions
- [ ] `useSbomComparison` is disabled when either `leftId` or `rightId` is not provided
- [ ] `useSbomComparison` refetches when `leftId` or `rightId` changes

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` sends correct request URL and query parameters
- [ ] Unit test: `useSbomComparison` returns loading state initially
- [ ] Unit test: `useSbomComparison` returns data on successful API response
- [ ] Unit test: `useSbomComparison` does not fire a request when IDs are missing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
