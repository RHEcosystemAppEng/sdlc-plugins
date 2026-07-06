## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces matching the backend comparison response shape, an Axios client function to call the comparison endpoint, and a React Query hook for data fetching with loading and error states. This task establishes the data-fetching foundation that the comparison page (Task 4) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function using the shared Axios client instance

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls compareSboms() and returns query result with loading/error/data states. Enabled only when both IDs are defined.

## Implementation Notes
- Follow the existing API layer pattern: interfaces in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- Model the `compareSboms()` function after existing functions like `fetchSboms()` in `src/api/rest.ts`. Use the shared Axios instance from `src/api/client.ts` which includes base URL configuration and auth interceptors.
- The hook should follow the pattern in `src/hooks/useSbomById.ts`: use `useQuery` from React Query with a query key that includes both SBOM IDs (e.g., `["sbomComparison", leftId, rightId]`), and set `enabled: !!leftId && !!rightId` to prevent fetching when IDs are not yet selected.
- TypeScript interfaces must match the backend response shape exactly:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];       // { name, version, license, advisory_count }
    removed_packages: RemovedPackage[];   // { name, version, license, advisory_count }
    version_changes: VersionChange[];     // { name, left_version, right_version, direction }
    new_vulnerabilities: NewVulnerability[];  // { advisory_id, severity, title, affected_package }
    resolved_vulnerabilities: ResolvedVulnerability[];  // { advisory_id, severity, title, previously_affected_package }
    license_changes: LicenseChange[];     // { name, left_license, right_license }
  }
  ```
- Per CONVENTIONS.md §API Layer: typed API functions go in `src/api/rest.ts`, React Query hooks go in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions (e.g., `useSbomComparison`, `compareSboms`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six diff category arrays as described above. Endpoint defined in `modules/fundamental/src/sbom/endpoints/compare.rs` (trustify-backend).

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for the compareSboms() function signature and Axios usage
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` — existing React Query hook pattern with useQuery, query key construction, and enabled flag
- `src/api/models.ts` — existing TypeScript interfaces showing naming conventions and export patterns

## Acceptance Criteria
- [ ] TypeScript interfaces for SbomComparisonResult and all six diff item types are defined and exported from models.ts
- [ ] compareSboms() function calls `GET /api/v2/sbom/compare` with correct `left` and `right` query parameters
- [ ] useSbomComparison hook returns loading, error, and data states via React Query
- [ ] Hook is disabled (does not fetch) when either SBOM ID is undefined
- [ ] All types compile without TypeScript errors

## Test Requirements
- [ ] Unit test: useSbomComparison hook fetches data when both IDs are provided, returns comparison result
- [ ] Unit test: useSbomComparison hook does not trigger fetch when leftId is undefined
- [ ] Unit test: useSbomComparison hook does not trigger fetch when rightId is undefined
- [ ] Unit test: useSbomComparison hook handles API error response correctly (sets error state)
- [ ] MSW handler for `GET /api/v2/sbom/compare` added to `tests/mocks/handlers.ts` with fixture data

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run src/hooks/useSbomComparison` — hook unit tests pass

## Dependencies
- Depends on: Task 2 — Add SBOM comparison REST endpoint with integration tests
