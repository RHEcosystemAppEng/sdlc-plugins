## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook `useSbomComparison` that wraps the `compareSboms` API client function. The hook manages loading state, error handling, and caching for the comparison request. It is only enabled when both SBOM IDs are provided.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for the SBOM comparison endpoint

## Implementation Notes
Follow the existing React Query hook patterns in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`.

The hook should:
1. Accept `leftId: string | undefined` and `rightId: string | undefined` parameters
2. Use `useQuery` from TanStack Query with:
   - `queryKey: ['sbom-comparison', leftId, rightId]`
   - `queryFn: () => compareSboms(leftId!, rightId!)`
   - `enabled: !!leftId && !!rightId` — only fire the request when both IDs are present
3. Return the standard `useQuery` result (data, isLoading, isError, error)

Import `compareSboms` from `src/api/rest.ts` and `SbomComparison` from `src/api/models.ts`.

## Reuse Candidates
- `src/hooks/useSbomById.ts` — pattern for a React Query hook with a conditional `enabled` flag
- `src/hooks/useSboms.ts` — pattern for a list-fetching React Query hook
- `src/api/rest.ts::compareSboms` — the API client function (from Task 6)

## Acceptance Criteria
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook uses React Query's `useQuery` with proper query key and enabled condition
- [ ] Hook does not fire API call when either SBOM ID is undefined
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Unit test: hook does not trigger a request when `leftId` is undefined
- [ ] Unit test: hook does not trigger a request when `rightId` is undefined
- [ ] Unit test: hook triggers a request and returns data when both IDs are provided (using MSW mock)

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 6 — Frontend API types and client function

[sdlc-workflow] Description digest: sha256-md:50255b94016adff0356356ec14a53cc3c1333c34ef899ea0b8f3be811dd03500
