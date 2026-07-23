## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, API client functions for calling the backend remediation endpoints, and React Query hooks for data fetching. This establishes the frontend data layer for the remediation dashboard, following the existing API layer pattern (models.ts for types, rest.ts for client functions, hooks/ for React Query hooks).

## Files to Modify
- `src/api/models.ts` — Add RemediationSummary, SeverityStatus, DailyCount, and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — Add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for GET /api/v2/remediation/summary
- `src/hooks/useRemediationByProduct.ts` — React Query hook for GET /api/v2/remediation/by-product with pagination support

## Implementation Notes
- Follow the existing TypeScript interface pattern in `src/api/models.ts` for defining response types.
- Follow the API client function pattern in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`. Example reference: `fetchSboms()` and `fetchAdvisories()` in rest.ts.
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` for query key naming, stale time, and error handling.
- The useRemediationByProduct hook should support pagination parameters following the `useSboms.ts` pattern.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ by_severity: SeverityStatus[], total_open: number, total_in_progress: number, total_resolved: number, trend: DailyCount[] }` where `SeverityStatus = { severity: string, open: number, in_progress: number, resolved: number }` and `DailyCount = { date: string, resolved: number }` (see `modules/remediation/src/model/summary.rs` and `modules/remediation/src/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation = { product_name: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/remediation/src/model/product.rs` and `modules/remediation/src/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; all API functions use this client
- `src/api/rest.ts::fetchSboms` — Reference API client function for list endpoints with pagination
- `src/api/rest.ts::fetchAdvisories` — Reference API client function for list endpoints
- `src/hooks/useSboms.ts` — Reference React Query hook pattern for list data with pagination
- `src/hooks/useAdvisories.ts` — Reference React Query hook pattern for list data

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary, SeverityStatus, DailyCount, and ProductRemediation are defined in src/api/models.ts
- [ ] fetchRemediationSummary() function is added to src/api/rest.ts and calls GET /api/v2/remediation/summary
- [ ] fetchRemediationByProduct() function is added to src/api/rest.ts and calls GET /api/v2/remediation/by-product with pagination parameters
- [ ] useRemediationSummary hook is created and returns typed query result
- [ ] useRemediationByProduct hook is created with pagination support and returns typed query result
- [ ] All new code is properly typed with TypeScript (no `any` types)

## Test Requirements
- [ ] Unit test: useRemediationSummary hook calls the correct API endpoint and returns typed data (using MSW mock handler)
- [ ] Unit test: useRemediationByProduct hook calls the correct API endpoint with pagination parameters
- [ ] Add MSW mock handlers for remediation endpoints in `tests/mocks/handlers.ts`
- [ ] Add mock fixture data for remediation responses in `tests/mocks/fixtures/remediation.json`
- [ ] Follow the testing pattern in existing hook tests using Vitest + React Testing Library

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
- Depends on: Task 2 — Add GET /api/v2/remediation/by-product endpoint
