## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add React Query hooks for fetching remediation data. Create `useRemediationSummary` and `useRemediationByProduct` hooks that wrap the API client functions with React Query's caching, loading states, and error handling.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for per-product remediation data

## Implementation Notes
Follow the existing React Query hook patterns in `src/hooks/`:

- `src/hooks/useSboms.ts` (useQuery for list data) — pattern for useRemediationSummary and useRemediationByProduct
- `src/hooks/useSbomById.ts` (useQuery for detail data) — reference for query key naming

Key patterns:
- Use `useQuery` from TanStack Query with descriptive query keys (e.g., `["remediation", "summary"]`, `["remediation", "by-product"]`)
- Import and call the API client functions from `src/api/rest.ts` (fetchRemediationSummary, fetchRemediationByProduct)
- Return the full useQuery result object for loading/error state handling in components
- Follow the naming convention: hook name matches the file name (useSboms.ts → useSboms)

## Acceptance Criteria
- [ ] useRemediationSummary hook fetches and caches remediation summary data
- [ ] useRemediationByProduct hook fetches and caches per-product remediation data
- [ ] Both hooks use descriptive query keys for cache management
- [ ] Both hooks properly type their return values
- [ ] No TypeScript compilation errors

## Test Requirements
- [ ] Hook tests verify correct query key usage
- [ ] Hook tests verify loading, success, and error states using MSW mocks
- [ ] Tests follow React Testing Library renderHook pattern

## Dependencies
- Depends on: Task 5 — Frontend API types and client
