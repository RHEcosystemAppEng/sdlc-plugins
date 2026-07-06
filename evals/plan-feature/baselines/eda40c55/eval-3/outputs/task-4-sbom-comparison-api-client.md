## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the Axios client function to call the comparison endpoint, and the React Query hook that wraps the client function. This task creates the data-fetching layer that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` -- add `fetchSbomComparison(leftId: string, rightId: string)` client function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping fetchSbomComparison

## Implementation Notes
- **TypeScript interfaces** (in `src/api/models.ts`):
  - `SbomComparison` -- top-level response type with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
  - `AddedPackage` -- fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `RemovedPackage` -- fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` -- fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `NewVulnerability` -- fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `ResolvedVulnerability` -- fields: `advisory_id: string`, `severity: string`, `title: string`, `previously_affected_package: string`
  - `LicenseChange` -- fields: `name: string`, `left_license: string`, `right_license: string`
- **Client function** (in `src/api/rest.ts`):
  - `export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparison>` -- calls `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}` using the existing Axios instance from `src/api/client.ts`.
  - Follow the pattern of existing functions in `rest.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`) for Axios usage and response extraction.
  - Per CONVENTIONS.md §API Layer: place the typed API function in `src/api/rest.ts` using the Axios client from `src/api/client.ts`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer file scope.
- **React Query hook** (in `src/hooks/useSbomComparison.ts`):
  - `export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined)` -- returns `useQuery` result.
  - Query key: `["sbom-comparison", leftId, rightId]`.
  - Enable only when both `leftId` and `rightId` are defined: `enabled: !!leftId && !!rightId`.
  - Follow the pattern of existing hooks in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`.
  - Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape: `SbomComparison` with six arrays as described above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API client function demonstrating the Axios call pattern
- `src/hooks/useSboms.ts` -- existing React Query hook demonstrating the query key and useQuery pattern
- `src/hooks/useSbomById.ts` -- existing hook showing the single-resource query pattern with enabled flag
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all seven comparison types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts` and correctly calls the comparison endpoint
- [ ] `useSbomComparison` hook returns React Query result with loading, error, and data states
- [ ] Hook is disabled (does not fire the request) when either SBOM ID is undefined

## Test Requirements
- [ ] Verify TypeScript interfaces compile without errors
- [ ] Verify the hook disables the query when IDs are undefined (unit test with React Testing Library)
- [ ] Verify the hook calls the correct endpoint URL with query parameters (unit test with MSW mock)

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation succeeds
- `npx vitest run src/hooks/useSbomComparison` -- hook unit tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison service and endpoint with integration tests
