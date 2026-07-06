## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces, API client functions, and React Query hooks for the two remediation backend endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). This provides the data-fetching layer that the remediation dashboard page (Task 5) and filterable table (Task 6) will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping `fetchRemediationSummary()` with appropriate query key and stale time
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping `fetchRemediationByProduct()` with pagination support via query parameters

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces: `RemediationSummaryItem` (severity, status, count), `RemediationSummaryResponse` (items array), `ProductRemediationBreakdown` (product_name, product_id, total, open, in_progress, resolved), `ByProductResponse` (items array, total)
- `src/api/rest.ts` -- Add API client functions: `fetchRemediationSummary()` and `fetchRemediationByProduct(params?: PaginationParams)`

## Implementation Notes
- Follow the existing API layer pattern: typed functions in `src/api/rest.ts` use the Axios client from `src/api/client.ts`, and React Query hooks in `src/hooks/` wrap those functions.
- Reference `src/hooks/useSboms.ts` for the React Query hook pattern: `useQuery` with a descriptive query key, the fetch function, and appropriate options.
- Reference `src/api/rest.ts::fetchSboms()` for the API client function pattern using the shared Axios instance.
- Per CONVENTIONS.md §API Layer: API client functions go in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`; React Query hooks go in `src/hooks/`. See `src/api/rest.ts` and `src/hooks/useSboms.ts` for the established pattern.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hook filenames (`useRemediationSummary.ts`) and function names (`fetchRemediationSummary`). See `src/hooks/useSboms.ts` for naming reference.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript hook file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ items: [{ severity: string, status: string, count: number }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product` -- response shape: `{ items: [{ product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts::axiosInstance` -- Shared Axios instance with base URL and auth interceptors; use for all API calls
- `src/api/rest.ts::fetchSboms` -- Existing API client function; follow the same pattern for remediation functions
- `src/hooks/useSboms.ts` -- React Query hook pattern; replicate for remediation hooks
- `src/api/models.ts` -- Existing TypeScript interfaces; add new interfaces alongside existing ones

## Acceptance Criteria
- [ ] `RemediationSummaryItem`, `RemediationSummaryResponse`, `ProductRemediationBreakdown`, and `ByProductResponse` interfaces are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` and `fetchRemediationByProduct()` functions are exported from `src/api/rest.ts`
- [ ] `useRemediationSummary` hook returns typed summary data using React Query
- [ ] `useRemediationByProduct` hook returns typed product breakdown data with pagination support
- [ ] All API calls use the shared Axios instance from `src/api/client.ts`

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook with MSW mock returning expected response shape
- [ ] Unit test for `useRemediationByProduct` hook with MSW mock returning paginated product data
- [ ] Verify hooks correctly handle loading, error, and success states

## Verification Commands
- `npx vitest run src/hooks/useRemediationSummary` -- Expected: hook tests pass
- `npx vitest run src/hooks/useRemediationByProduct` -- Expected: hook tests pass

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation service and endpoint (defines the API contract)
- Depends on: Task 2 -- Add remediation by-product aggregation service and endpoint (defines the API contract)
