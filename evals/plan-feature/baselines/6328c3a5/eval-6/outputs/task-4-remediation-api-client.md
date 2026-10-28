## Repository
trustify-ui

## Target Branch
main

## Description
Add the API client layer for the remediation endpoints. Define TypeScript interfaces matching the backend response types, add fetch functions to the REST client, and create React Query hooks for data fetching. This provides the data layer that the remediation dashboard components (Tasks 5 and 6) will consume.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCount`, `ProductRemediation`, and `VulnerabilityItem` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()`

## Implementation Notes
- Follow the API layer pattern: typed interfaces in `src/api/models.ts`, fetch functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
- See `src/hooks/useSboms.ts` for the React Query hook pattern: `useQuery` with a query key and fetch function.
- See `src/api/rest.ts` for the fetch function pattern: use the shared Axios instance from `src/api/client.ts`.
- Per Key Conventions: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.
- Per Key Conventions: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ entries: SeverityStatusCount[] }` where `SeverityStatusCount` = `{ severity: string, status: string, count: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product` — response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation` = `{ product_name: string, total: number, open: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` — reference for fetch function pattern with Axios
- `src/hooks/useSboms.ts` — reference for React Query `useQuery` hook pattern
- `src/api/models.ts` — existing interfaces (SbomSummary, AdvisorySummary) show the model definition pattern
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `RemediationSummary` interface matches backend response shape
- [ ] `ProductRemediation` interface matches backend response shape
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` via shared Axios client
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` via shared Axios client
- [ ] `useRemediationSummary` hook returns `{ data, isLoading, error }` using React Query
- [ ] `useRemediationByProduct` hook returns `{ data, isLoading, error }` using React Query

## Test Requirements
- [ ] Unit test verifying `fetchRemediationSummary` calls correct endpoint path
- [ ] Unit test verifying `fetchRemediationByProduct` calls correct endpoint path
- [ ] Hook tests verifying loading/success/error states using React Testing Library + MSW

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints (API contracts must be defined)
