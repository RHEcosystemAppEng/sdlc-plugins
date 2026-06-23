# Task 7 — Add React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a React Query hook (`useSbomComparison`) that wraps the comparison API client function. The hook accepts two SBOM IDs, calls the comparison endpoint, and manages loading/error/data states. It is enabled only when both SBOM IDs are provided, supporting the UI flow where the user selects two SBOMs before triggering the comparison.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` returning `UseQueryResult<SbomComparisonResult>`

## Implementation Notes
- Follow the existing React Query hook pattern from `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
  - Use `useQuery` from TanStack Query
  - Define a unique query key (e.g., `["sbom-comparison", leftId, rightId]`)
  - Call the `compareSboms` client function from `src/api/rest.ts`
- The hook should be **disabled** when either `leftId` or `rightId` is undefined — use the `enabled` option: `enabled: !!leftId && !!rightId`
- This supports the UI flow: the hook does not fire until the user has selected both SBOMs and clicked Compare.
- Per docs/constraints.md §5.4: Reuse existing patterns rather than writing new data-fetching logic.

## Reuse Candidates
- `src/hooks/useSboms.ts` — Follow the same `useQuery` pattern for query key naming and options
- `src/hooks/useSbomById.ts` — Follow the same pattern for hooks that accept an ID parameter with `enabled` guard

## Acceptance Criteria
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook returns `UseQueryResult<SbomComparisonResult>` with data, isLoading, isError states
- [ ] Hook does not fire the API call when either SBOM ID is undefined
- [ ] Hook fires the API call when both SBOM IDs are provided
- [ ] Query key includes both SBOM IDs for proper cache management

## Test Requirements
- [ ] Unit test: hook does not trigger API call when leftId is undefined
- [ ] Unit test: hook triggers API call when both IDs are provided
- [ ] Unit test: hook returns comparison data on successful API response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison API types and client function

sha256-md:0504f3a8ce4792939bfd042f4253198a5bceb5b674ad58c5a5ddf5294a304244
