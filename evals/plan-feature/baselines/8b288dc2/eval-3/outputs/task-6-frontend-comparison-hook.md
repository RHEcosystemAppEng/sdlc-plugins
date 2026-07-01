## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a React Query hook `useSbomComparison` that wraps the `compareSboms` API client function. The hook manages loading, error, and success states for the comparison data and is consumed by the comparison page component.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for SBOM comparison data fetching

## Implementation Notes
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
  - Use `useQuery` from React Query (TanStack Query).
  - Query key: `["sbom-comparison", leftId, rightId]` to enable proper caching and invalidation.
  - Query function: call `compareSboms(leftId, rightId)` from `src/api/rest.ts`.
  - The hook should accept `leftId: string | undefined` and `rightId: string | undefined` parameters.
  - Use the `enabled` option: only fetch when both `leftId` and `rightId` are defined and non-empty.
  - Return the standard `useQuery` result (`data`, `isLoading`, `isError`, `error`).
- The hook is a pure data-fetching layer — no UI logic.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating query key pattern, useQuery configuration, and return type
- `src/hooks/useSbomById.ts` — existing hook showing parameter-dependent querying with `enabled` option
- `src/hooks/useAdvisories.ts` — additional reference for React Query hook patterns

## Acceptance Criteria
- [ ] `useSbomComparison(leftId, rightId)` hook exists and returns React Query result
- [ ] Hook does not fetch when either ID is undefined or empty
- [ ] Hook uses correct query key for caching
- [ ] Hook returns typed `SbomComparisonResult` data

## Test Requirements
- [ ] Unit test: hook does not trigger a fetch when leftId is undefined
- [ ] Unit test: hook triggers a fetch when both IDs are provided
- [ ] Unit test: hook returns loading state while fetch is in progress

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add API types and client function for comparison

## Description Digest
sha256-md:4e2e35cfd2c1dcdead964fe4bd914a26430b54472f43f5abbedfbd536cd60384
