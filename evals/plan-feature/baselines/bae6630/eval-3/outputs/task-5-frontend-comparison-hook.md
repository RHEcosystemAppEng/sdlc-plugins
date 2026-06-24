# Task 5 — Frontend React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook that wraps the `fetchSbomComparison` API function, providing loading/error/data states for the comparison page. The hook accepts left and right SBOM IDs and only fires the query when both are provided.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)`. Uses `useQuery` with query key `["sbom-comparison", leftId, rightId]`. The query is `enabled` only when both `leftId` and `rightId` are defined and non-empty. Calls `fetchSbomComparison` from `src/api/rest.ts`.

## Implementation Notes
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`.
- Use `useQuery` from TanStack React Query.
- The query key should include both IDs so React Query correctly caches and refetches when IDs change.
- Set `enabled: !!leftId && !!rightId` so the hook does not fire on initial page load when no SBOMs are selected.
- Return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).

## Acceptance Criteria
- [ ] Hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook accepts optional left and right SBOM ID parameters
- [ ] Query is disabled when either ID is undefined or empty
- [ ] Query fires when both IDs are provided
- [ ] Query key includes both SBOM IDs for correct caching
- [ ] Hook returns standard React Query result shape

## Test Requirements
- [ ] Unit test: hook does not fire query when leftId is undefined
- [ ] Unit test: hook does not fire query when rightId is undefined
- [ ] Unit test: hook fires query and returns data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 4 — Frontend API types and client function for SBOM comparison

## Digest
[sdlc-workflow] Description digest: sha256-md:4facd9ee61f141bbaf2a5f29cbbbf4718ee46575bf3cd926aca673de29d0ccf6
