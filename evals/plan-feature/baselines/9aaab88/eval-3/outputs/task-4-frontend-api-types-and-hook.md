## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, a client function to call the comparison endpoint, and a React Query hook for data fetching. This is the API layer that the comparison UI components will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW client function: `fetchSbomComparison(leftId, rightId)` returns `SbomComparisonDiff`

## Implementation Notes
Add the following interfaces to `src/api/models.ts`:
- `SbomComparisonDiff` with fields: `added_packages: AddedPackage[]`, `removed_packages: RemovedPackage[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: NewVulnerability[]`, `resolved_vulnerabilities: ResolvedVulnerability[]`, `license_changes: LicenseChange[]`
- Sub-interfaces: `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` matching the backend response shape

The `fetchSbomComparison` function in `src/api/rest.ts` should follow the pattern of existing functions like `fetchSboms()` — use the Axios client from `src/api/client.ts` to call the endpoint and return typed data.

The `useSbomComparison` hook in `src/hooks/useSbomComparison.ts` should follow the pattern of `src/hooks/useSbomById.ts` — use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]` and enable only when both IDs are provided.

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` file scope.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors for API calls
- `src/api/rest.ts::fetchSboms` — pattern for typed API client functions
- `src/hooks/useSbomById.ts` — pattern for React Query hook with conditional enablement
- `src/api/models.ts` — existing interfaces to follow naming and typing conventions

## Acceptance Criteria
- [ ] `SbomComparisonDiff` and all sub-interfaces are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` is exported from `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison(leftId, rightId)` hook returns `{ data, isLoading, isError }` and is only enabled when both IDs are provided
- [ ] TypeScript compiles without errors (`npx tsc --noEmit`)

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook verifies it calls the correct endpoint with query parameters
- [ ] Unit test verifies the hook is disabled when either ID is undefined
- [ ] MSW handler added to `tests/mocks/handlers.ts` for the comparison endpoint

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run --reporter=verbose -- useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 3 — Backend comparison service and endpoint (defines the API contract)

sha256-md:eb736bfc8f529a08a5e90a0f61383ed9a9c17f087a312446cc482b5496166f95
