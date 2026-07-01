# Task 4 — Add remediation API client, TypeScript models, and React Query hooks

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the frontend API layer for the remediation endpoints: TypeScript interfaces for response types, Axios client functions for fetching data, and React Query hooks for data fetching. This provides the data layer that the dashboard page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for `RemediationSummary`, `ProductRemediation`, `SeverityStatusCount`
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()`

## Implementation Notes
- Follow the existing API client pattern in `src/api/rest.ts`: typed functions using the Axios instance from `src/api/client.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`).
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`: each hook uses `useQuery` from React Query with a descriptive query key.
- TypeScript interfaces should be added to `src/api/models.ts` alongside existing interfaces.
- The `RemediationSummary` interface should include arrays of counts grouped by severity x status.
- The `ProductRemediation` interface should include product name, total, open, and resolved count fields.
- The `fetchRemediationByProduct` function should accept pagination parameters (offset, limit) consistent with other paginated endpoints.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ counts: { severity: string, status: string, count: number }[] }` (see `RemediationSummary` struct in `modules/fundamental/src/remediation/model/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` (see `ProductRemediation` struct in `modules/fundamental/src/remediation/model/product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern with Axios
- `src/api/rest.ts::fetchAdvisories` — reference for API client function pattern
- `src/hooks/useSboms.ts` — reference for React Query `useQuery` hook pattern
- `src/hooks/useAdvisories.ts` — reference for React Query hook pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `RemediationSummary` and `ProductRemediation` TypeScript interfaces exist in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function exists in `src/api/rest.ts` and calls `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` function exists in `src/api/rest.ts` and calls `GET /api/v2/remediation/by-product` with pagination parameters
- [ ] `useRemediationSummary` hook exists and returns query result for summary data
- [ ] `useRemediationByProduct` hook exists and returns query result for per-product data with pagination support

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook verifying it calls the correct API endpoint and returns data
- [ ] Unit test for `useRemediationByProduct` hook verifying it calls the correct API endpoint with pagination parameters
- [ ] Tests use MSW mock handlers for the remediation endpoints

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
