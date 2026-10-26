## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the REST client function to call the comparison endpoint, and a React Query hook for managing comparison data fetching. This establishes the frontend data layer for the comparison feature, enabling the UI tasks to consume comparison results.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for SbomComparisonResult and its sub-types
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Per CONVENTIONS.md §API layer: follow the `api/client.ts` -> `api/rest.ts` -> `hooks/` pattern for the data-fetching layer. Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope. See `src/api/rest.ts` and `src/hooks/useSboms.ts` for the established pattern.
- Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state, no Redux. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook file scope. See `src/hooks/useSboms.ts` for the established pattern.
- TypeScript interfaces to add in `src/api/models.ts`:
  - `SbomComparisonResult` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
  - `AddedPackage`: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `RemovedPackage`: same shape as AddedPackage
  - `VersionChange`: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability`: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `ResolvedVulnerability`: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
  - `LicenseChange`: `name: string`, `left_license: string`, `right_license: string`
- Follow the REST client function pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts` and return typed response data. Example: `export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> => client.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } }).then(r => r.data);`
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` — use `useQuery` with a query key that includes both SBOM IDs. Enable the query only when both IDs are provided (`enabled: !!leftId && !!rightId`).

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for reference on naming and typing conventions
- `src/api/rest.ts::fetchSboms` — reference for REST client function pattern (Axios get with typed response)
- `src/hooks/useSboms.ts` — reference for React Query hook pattern (useQuery with query key)
- `src/hooks/useSbomById.ts` — reference for conditional query enabling pattern

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult` and all sub-types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison()` function is exported from `src/api/rest.ts` and calls the correct endpoint with query parameters
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] The hook only fires the API call when both SBOM IDs are provided
- [ ] The hook returns standard React Query state (data, isLoading, isError)
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify the hook calls `fetchSbomComparison` with correct parameters when both IDs are provided
- [ ] Unit test for `useSbomComparison` hook: verify the hook does not fire when one or both IDs are undefined
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning mock comparison data

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run src/hooks/useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service and REST endpoint
