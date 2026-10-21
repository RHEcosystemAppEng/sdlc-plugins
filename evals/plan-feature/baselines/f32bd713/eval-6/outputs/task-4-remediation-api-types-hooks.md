## Repository
trustify-ui

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for both remediation endpoints, and React Query hooks for data fetching. This task establishes the frontend data layer for the remediation tracking dashboard, connecting the UI to the backend endpoints created in Tasks 1-2.

## Files to Modify
- `src/api/models.ts` -- add RemediationSummaryGroup, RemediationSummaryResponse, RemediationByProductItem, and RemediationByProductResponse TypeScript interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() Axios client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping fetchRemediationSummary
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping fetchRemediationByProduct with filter/pagination params

## Implementation Notes
- TypeScript interfaces must match the backend API response shapes exactly:
  - `RemediationSummaryResponse`: `{ groups: RemediationSummaryGroup[] }` where `RemediationSummaryGroup` is `{ severity: string, status: string, count: number }`
  - `RemediationByProductResponse`: `{ items: RemediationByProductItem[], total: number }` where `RemediationByProductItem` is `{ product: string, total: number, open: number, in_progress: number, resolved: number }`
- API client functions use the shared Axios instance from `src/api/client.ts` with the configured base URL and auth interceptors.
  Per CONVENTIONS.md section API Layer: Axios client in src/api/client.ts; typed API functions in src/api/rest.ts; React Query hooks in src/hooks/.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.
- React Query hooks follow the existing patterns in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` -- use `useQuery` with a descriptive query key.
  Per CONVENTIONS.md section State Management: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript hook scope.
- Hook naming follows the camelCase convention: `useRemediationSummary`, `useRemediationByProduct`.
  Per CONVENTIONS.md section Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's naming scope.
- The `useRemediationByProduct` hook should accept optional filter parameters (severity, product, status) and pagination parameters (offset, limit) to support the filterable table in Task 6.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ groups: [{ severity: string, status: string, count: number }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: RemediationByProductItem[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import and use for API calls
- `src/api/rest.ts::fetchSboms()` -- existing API client function pattern to follow for fetchRemediationSummary
- `src/api/rest.ts::fetchAdvisories()` -- existing API client function pattern to follow for fetchRemediationByProduct
- `src/hooks/useSboms.ts` -- React Query useQuery hook pattern with query key
- `src/hooks/useAdvisories.ts` -- React Query useQuery hook pattern for list data
- `src/api/models.ts` -- existing TypeScript interface patterns (SbomSummary, AdvisorySummary)

## Acceptance Criteria
- [ ] TypeScript interfaces defined for remediation summary and by-product API responses
- [ ] `fetchRemediationSummary()` function calls `GET /api/v2/remediation/summary` and returns typed response
- [ ] `fetchRemediationByProduct()` function calls `GET /api/v2/remediation/by-product` with optional filter and pagination query params
- [ ] `useRemediationSummary` hook returns typed query result with loading/error/data states
- [ ] `useRemediationByProduct` hook accepts filter/pagination params and returns typed query result
- [ ] All types match the backend API response shapes documented above

## Test Requirements
- [ ] Verify `useRemediationSummary` hook returns correctly typed data with MSW mock handlers
- [ ] Verify `useRemediationByProduct` hook returns correctly typed data with MSW mock handlers
- [ ] Verify hooks handle error responses correctly (non-2xx status codes)
- [ ] Verify `useRemediationByProduct` passes filter parameters as query string to the API

## Dependencies
- Depends on: Task 2 -- Add remediation summary and by-product endpoints
