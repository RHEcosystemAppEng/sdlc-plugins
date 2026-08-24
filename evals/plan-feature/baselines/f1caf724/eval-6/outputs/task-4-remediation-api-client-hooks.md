## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces, API client functions, and React Query hooks for the remediation summary and by-product backend endpoints. This task establishes the data-fetching layer that the dashboard page components (Tasks 5 and 6) will consume. The API client functions call `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`, and the hooks wrap them with React Query for caching, loading states, and error handling.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummaryEntry`, `RemediationSummary`, `RemediationByProductEntry`, and `RemediationByProduct` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` with pagination parameters

## Implementation Notes
- Follow the existing API layer pattern: typed functions in `src/api/rest.ts` using the Axios client from `src/api/client.ts`, wrapped by React Query hooks in `src/hooks/`.
  Per CONVENTIONS.md §API Layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's API layer file scope.
- Use React Query (TanStack Query) for server state management — no Redux.
  Per CONVENTIONS.md §State Management: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.
- Follow camelCase naming for hooks and utility functions.
  Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useRemediationByProduct.ts` matching the convention's `.ts` hook file scope.
- **Backend API contracts:**
  - `GET /api/v2/remediation/summary` — response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
  - `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `PaginatedResults<RemediationByProduct>` where each entry has `{ product_name: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- Reference `useSboms.ts` and `useAdvisories.ts` for the hook pattern (query key naming, stale time configuration, error handling).

## Reuse Candidates
- `src/api/client.ts::client` — Axios instance with base URL and auth interceptors; use for API calls
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern with typed responses
- `src/hooks/useSboms.ts` — reference for React Query hook pattern with query key and options
- `src/api/models.ts` — existing TypeScript interfaces; follow the same interface definition style

## Acceptance Criteria
- [ ] `RemediationSummaryEntry` and `RemediationByProductEntry` TypeScript interfaces are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function is added to `src/api/rest.ts` calling `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` function is added to `src/api/rest.ts` calling `GET /api/v2/remediation/by-product` with pagination params
- [ ] `useRemediationSummary` hook returns `{ data, isLoading, isError }` from React Query
- [ ] `useRemediationByProduct` hook accepts pagination parameters and returns paginated results
- [ ] All TypeScript interfaces match the backend API response shapes

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook using MSW to mock the summary endpoint
- [ ] Unit test for `useRemediationByProduct` hook using MSW to mock the by-product endpoint with pagination
- [ ] Unit test verifying error handling when the API returns a non-200 status

## Verification Commands
- `npx vitest run src/hooks/useRemediationSummary` — verify summary hook tests pass
- `npx vitest run src/hooks/useRemediationByProduct` — verify by-product hook tests pass

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint (API contract)
- Depends on: Task 2 — Add remediation by-product aggregation endpoint (API contract)
