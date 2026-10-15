## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces matching the backend response shape, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This provides the data-access foundation for the comparison page UI.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomCompare.ts` — React Query hook `useSbomCompare(leftId, rightId)` that calls `compareSboms` and returns query state

## Implementation Notes
- Per CONVENTIONS.md §API layer: add typed API functions in `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` file scope.
- Per CONVENTIONS.md §State management: use React Query (TanStack Query) for the comparison hook. The hook should only execute when both `leftId` and `rightId` are provided (use `enabled: !!leftId && !!rightId`). See `src/hooks/useSbomById.ts` for the existing pattern.
  Applies: task creates `src/hooks/useSbomCompare.ts` matching the convention's `.ts` hook file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions.
  Applies: task creates `src/hooks/useSbomCompare.ts` matching the convention's `.ts` file scope.

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
  interface AddedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface RemovedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
  interface NewVulnerability { advisory_id: string; severity: string; title: string; affected_package: string; }
  interface ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
  interface LicenseChange { name: string; left_license: string; right_license: string; }
  ```
  (See `modules/fundamental/src/sbom/model/compare.rs` in trustify-backend for the authoritative struct definitions)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API function pattern to follow for `compareSboms`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison request
- `src/hooks/useSbomById.ts` — Existing React Query hook pattern to follow for `useSbomCompare`
- `src/api/models.ts` — Existing TypeScript interfaces; add comparison types alongside them

## Acceptance Criteria
- [ ] `SbomComparisonResult` and all sub-interfaces are defined in `src/api/models.ts` matching the backend response shape
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts` and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomCompare(leftId, rightId)` hook is exported from `src/hooks/useSbomCompare.ts`
- [ ] The hook returns `{ data, isLoading, isError, error }` following the React Query pattern
- [ ] The hook is disabled when either `leftId` or `rightId` is falsy

## Test Requirements
- [ ] Unit test: `compareSboms` sends correct request to `/api/v2/sbom/compare` with query parameters
- [ ] Unit test: `useSbomCompare` returns loading state initially and data after resolution
- [ ] Unit test: `useSbomCompare` does not fire a request when leftId or rightId is undefined

## Dependencies
- Depends on: Task 2 — Add SBOM comparison endpoint and tests (defines the API contract)
