## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Description
Add the API client layer and React Query hooks for the remediation endpoints. This task creates TypeScript interfaces matching the backend response shapes, API client functions using the shared Axios instance, and React Query hooks that the dashboard page components will consume for data fetching. This establishes the data layer for the frontend remediation dashboard.

## Files to Modify
- `src/api/models.ts` — Add RemediationSummary, SeverityStatusCount, ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — Add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping fetchRemediationSummary with appropriate query key and caching
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping fetchRemediationByProduct with query key, caching, and filter parameters

## Implementation Notes
Per CONVENTIONS.md §API layer: API client functions go in `src/api/rest.ts` using the shared Axios instance from `src/api/client.ts`; TypeScript interfaces go in `src/api/models.ts`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` file scope.

Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state with `useQuery` hooks in `src/hooks/`.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions, PascalCase for type interfaces.
Applies: task modifies `src/api/models.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ severities: { critical: { open: number, in_progress: number, resolved: number }, high: {...}, medium: {...}, low: {...} } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product` — response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation = { product_id: string, product_name: string, total: number, open: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Follow the existing hook patterns in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` for React Query configuration (query keys, stale time, error handling).

## Reuse Candidates
- `src/api/client.ts::axiosInstance` — Shared Axios instance with base URL and auth interceptors; use for all remediation API calls
- `src/api/rest.ts::fetchSboms` — Reference pattern for API client function structure with typed responses
- `src/hooks/useSboms.ts` — Reference pattern for React Query useQuery hook with query key and options
- `src/hooks/useAdvisories.ts` — Reference pattern for list-fetching hook with filter parameters
- `src/api/models.ts` — Existing TypeScript interfaces to follow for naming and structure consistency

## Acceptance Criteria
- [ ] RemediationSummary TypeScript interface matches the backend GET /api/v2/remediation/summary response shape
- [ ] ProductRemediation TypeScript interface matches the backend GET /api/v2/remediation/by-product response shape
- [ ] fetchRemediationSummary() calls the correct endpoint and returns typed data
- [ ] fetchRemediationByProduct() calls the correct endpoint with optional filter parameters and returns typed data
- [ ] useRemediationSummary hook returns { data, isLoading, isError } with appropriate React Query configuration
- [ ] useRemediationByProduct hook supports filter parameters and returns typed paginated results

## Test Requirements
- [ ] Unit test: fetchRemediationSummary calls GET /api/v2/remediation/summary and returns typed response
- [ ] Unit test: fetchRemediationByProduct calls GET /api/v2/remediation/by-product with query parameters
- [ ] Unit test: useRemediationSummary hook returns loading state, then data state
- [ ] Unit test: useRemediationByProduct hook passes filter parameters to the API function

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints with integration tests
