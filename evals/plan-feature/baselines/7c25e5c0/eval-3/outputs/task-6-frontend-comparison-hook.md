## Repository
trustify-ui

## Target Branch
main

## Description
Create a React Query hook `useSbomComparison` that wraps the `compareSboms` API function. The hook manages loading, error, and data states for the comparison result and is consumed by the comparison page component.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for SBOM comparison

## Implementation Notes
Follow the existing hook patterns:
- `src/hooks/useSboms.ts` defines `useSboms()` using `useQuery` — follow the same pattern for `useSbomComparison`
- `src/hooks/useSbomById.ts` defines `useSbomById(id)` — follow the same parameter-passing pattern
- The hook should accept `leftId: string | undefined` and `rightId: string | undefined` parameters
- Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
- Set `enabled: !!leftId && !!rightId` so the query only runs when both IDs are provided
- Call `compareSboms(leftId!, rightId!)` as the query function
- Return the standard React Query result object (`{ data, isLoading, isError, error }`)

Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's React Query hook scope.

## Reuse Candidates
- `src/hooks/useSbomById.ts` — existing hook for fetching a single SBOM by ID, reference for parameterized useQuery pattern
- `src/hooks/useSboms.ts` — existing hook for SBOM list, reference for query key naming convention

## Acceptance Criteria
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook uses React Query's `useQuery` with proper query key including both IDs
- [ ] Query is disabled when either ID is undefined (no premature API calls)
- [ ] Hook returns comparison data, loading state, and error state

## Test Requirements
- [ ] Hook does not trigger a query when either ID is undefined
- [ ] Hook triggers a query when both IDs are provided
- [ ] Hook returns the correct data shape from the API response

## Dependencies
- Depends on: Task 5 — Frontend API types and client
