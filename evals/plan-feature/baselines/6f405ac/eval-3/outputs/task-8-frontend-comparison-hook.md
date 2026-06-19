## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook `useSbomComparison` that wraps the `compareSboms` API client function. The hook accepts two SBOM IDs and returns the comparison result with standard React Query loading/error states. The comparison page (task 9) will use this hook to fetch and display the diff.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for SBOM comparison

## Implementation Notes
Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
- Use `useQuery` from TanStack Query
- Query key: `['sbom-comparison', leftId, rightId]`
- Query function: call `compareSboms(leftId, rightId)` from `src/api/rest.ts`
- The query should be disabled (`enabled: false` or `enabled: !!leftId && !!rightId`) when either ID is missing, since the comparison is triggered on demand

Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook scope.

## Reuse Candidates
- `src/hooks/useSboms.ts` — reference for React Query `useQuery` hook pattern with query key and function
- `src/hooks/useSbomById.ts` — reference for single-entity query pattern with ID parameter
- `src/api/rest.ts::compareSboms` — API client function to call (from task 7)

## Dependencies
- Depends on: Task 7 — Frontend API types and client (uses `compareSboms` function and `SbomComparison` type)

## Acceptance Criteria
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook returns `{ data, isLoading, isError, error, refetch }` from React Query
- [ ] Query is disabled when either SBOM ID is missing
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test: hook returns loading state initially when IDs are provided
- [ ] Unit test: hook returns comparison data on successful fetch (using MSW mock)
- [ ] Unit test: hook is disabled when either ID is undefined
