# Task 5 -- Frontend API types and client for SBOM comparison

## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page UI (Task 6) and MSW mocks (Task 7) will consume.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces: SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` function using the API client

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls fetchSbomComparison() and returns query result; only enabled when both IDs are defined

## Implementation Notes
- Follow the existing pattern in `src/api/models.ts` for interface definitions -- match the JSON field names from the backend response.
- Follow the existing pattern in `src/api/rest.ts` for client functions -- use the shared API client with proper typing.
- Follow the existing hook pattern in `src/hooks/useSboms.ts` for the React Query hook structure -- use `useQuery` with a descriptive query key like `["sbom-comparison", leftId, rightId]`.
- The hook should set `enabled: !!leftId && !!rightId` to prevent fetching until both SBOM IDs are selected.
- Per CONVENTIONS.md Mutation pattern: use React Query patterns with proper query key management. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

## Acceptance Criteria
- [ ] SbomComparison TypeScript interface matches the backend response shape (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] fetchSbomComparison() calls GET /api/v2/sbom/compare?left={id1}&right={id2} and returns typed response
- [ ] useSbomComparison hook returns loading/error/data states via React Query
- [ ] Hook does not fire the API call until both leftId and rightId are defined

## Test Requirements
- [ ] Unit test: fetchSbomComparison() calls the correct endpoint URL with query parameters
- [ ] Unit test: useSbomComparison returns isLoading: false and does not fetch when either ID is undefined

## Verification Commands
- `npx tsc --noEmit` -- no TypeScript compilation errors
- `npx vitest run src/hooks/useSbomComparison` -- hook unit tests pass

## Dependencies
- Depends on: Task 3 -- SBOM comparison endpoint (backend endpoint must exist for integration)
