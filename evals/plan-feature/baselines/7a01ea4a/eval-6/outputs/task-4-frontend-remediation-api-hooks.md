# Task 4: Add remediation API types, client functions, and React Query hooks

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the remediation tracking dashboard. This includes TypeScript interfaces for the remediation API response types, Axios client functions for fetching remediation data, and React Query hooks that the dashboard page components will consume. This task establishes the data-fetching foundation required by the dashboard page (Task 5) and the filterable table (Task 6) for TC-9006.

## Files to Modify
- `src/api/models.ts` -- add `RemediationSummary`, `RemediationSummaryItem`, `ProductRemediation`, and `PaginatedProductRemediation` TypeScript interfaces
- `src/api/rest.ts` -- add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook for `GET /api/v2/remediation/summary`
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the existing API client pattern in `src/api/rest.ts`: each function uses the Axios instance from `src/api/client.ts` and returns typed responses. See `fetchSboms()` and `fetchAdvisories()` for examples.
  - Applies: task modifies `src/api/rest.ts` matching the TypeScript API client file scope.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`: use `useQuery` with a query key and the corresponding API client function.
  - Applies: task creates `src/hooks/useRemediationSummary.ts` matching the TypeScript hooks file scope.
- Use camelCase for hook names (`useRemediationSummary`, `useRemediationByProduct`) consistent with the naming convention in `src/hooks/`.
- TypeScript interfaces should match the backend response shapes exactly.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: { open: number, in_progress: number, resolved: number } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `PaginatedResults<ProductRemediation>` where `ProductRemediation = { product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; use for all API calls
- `src/api/rest.ts` -- existing API client functions (`fetchSboms`, `fetchAdvisories`); follow the same pattern
- `src/hooks/useSboms.ts` -- React Query hook example; follow the same `useQuery` pattern
- `src/hooks/useAdvisories.ts` -- React Query hook example; follow the same `useQuery` pattern

## Acceptance Criteria
- [ ] TypeScript interfaces for `RemediationSummary`, `RemediationSummaryItem`, and `ProductRemediation` are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function is implemented in `src/api/rest.ts` and calls `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` function is implemented in `src/api/rest.ts` and calls `GET /api/v2/remediation/by-product` with pagination support
- [ ] `useRemediationSummary` hook returns typed remediation summary data via React Query
- [ ] `useRemediationByProduct` hook returns typed per-product remediation data via React Query with pagination parameters
- [ ] All types and hooks are exported and available for consumption by page components

## Test Requirements
- [ ] Unit test: `useRemediationSummary` hook returns expected data shape with MSW mock handler
- [ ] Unit test: `useRemediationByProduct` hook returns expected paginated data shape with MSW mock handler
- [ ] Unit test: API client functions construct correct request URLs and parameters
- [ ] Add MSW handlers for remediation endpoints in `tests/mocks/handlers.ts`

## Dependencies
- Depends on: Task 1 -- Create remediation module with summary aggregation endpoint
- Depends on: Task 2 -- Add per-product remediation breakdown endpoint
