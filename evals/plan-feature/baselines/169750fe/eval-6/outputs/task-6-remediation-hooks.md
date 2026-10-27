## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create React Query hooks for fetching remediation data from the backend endpoints. These hooks provide the data-fetching layer between the API client functions and the dashboard page components.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for per-product remediation data

## Implementation Notes
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`:
  - `useRemediationSummary()` wraps `fetchRemediationSummary()` with `useQuery`
  - `useRemediationByProduct(params)` wraps `fetchRemediationByProduct()` with `useQuery`, accepting pagination params
- Use appropriate query keys for cache management (e.g., `["remediation", "summary"]` and `["remediation", "by-product", params]`).
- Per Key Conventions: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's state management scope.
- Per Key Conventions: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's naming scope.

## Reuse Candidates
- `src/hooks/useSboms.ts` — example React Query hook with useQuery
- `src/hooks/useAdvisories.ts` — example React Query hook pattern
- `src/hooks/useDeleteSbomMutation.ts` — example mutation hook with cache invalidation

## Acceptance Criteria
- [ ] `useRemediationSummary()` returns query result with loading, error, and data states
- [ ] `useRemediationByProduct(params)` returns paginated query result
- [ ] Query keys are properly scoped for cache isolation
- [ ] Hooks re-fetch on parameter changes (e.g., pagination offset)

## Test Requirements
- [ ] Hooks render without errors when wrapped in QueryClientProvider
- [ ] Loading and error states are correctly exposed
- [ ] Query key changes trigger re-fetches

## Dependencies
- Depends on: Task 5 — Frontend API types and client functions
