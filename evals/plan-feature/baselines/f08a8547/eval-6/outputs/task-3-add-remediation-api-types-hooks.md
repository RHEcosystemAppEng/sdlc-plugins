## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript type definitions for the remediation API responses, API client functions for fetching remediation data, and React Query hooks for the frontend dashboard to consume. This establishes the data-fetching layer that the remediation dashboard components will use.

## Files to Modify
- `src/api/models.ts` — add RemediationSummary, SeverityStatusCounts, ProductRemediation, and related TypeScript interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for per-product remediation data with pagination support

## Implementation Notes
- Per CONVENTIONS.md §API layer: follow the established pattern with Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's .ts API file scope.

- Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state. Follow the `useQuery` pattern established by existing hooks.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's .ts hook file scope.

- Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's .ts file scope.

- Use the existing Axios instance from `src/api/client.ts` for all API calls.
- Model the response types to match the backend API contracts exactly.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ severityCounts: { critical: { open: number, inProgress: number, resolved: number }, high: {...}, medium: {...}, low: {...} } }` (see `modules/remediation/src/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation = { productName: string, total: number, open: number, resolved: number }` (see `modules/remediation/src/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing TypeScript interfaces for API response types (reference for type definition pattern)
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern with Axios
- `src/hooks/useSboms.ts` — reference for React Query useQuery hook pattern
- `src/hooks/useAdvisories.ts` — reference for React Query hook with query key conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary, SeverityStatusCounts, and ProductRemediation are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function exists in `src/api/rest.ts` calling `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` function exists in `src/api/rest.ts` calling `GET /api/v2/remediation/by-product` with pagination parameters
- [ ] `useRemediationSummary` hook wraps the summary API call with React Query `useQuery`
- [ ] `useRemediationByProduct` hook wraps the by-product API call with React Query `useQuery` and supports pagination parameters
- [ ] All new code is properly typed with no TypeScript errors

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook using MSW to mock the summary API response
- [ ] Unit test for `useRemediationByProduct` hook using MSW to mock the by-product API response
- [ ] Test that hooks return loading state initially
- [ ] Test error handling when API calls fail

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
