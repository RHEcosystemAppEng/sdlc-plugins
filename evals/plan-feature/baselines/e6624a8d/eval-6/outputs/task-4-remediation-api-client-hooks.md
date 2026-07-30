## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, API client functions to call the backend remediation endpoints, and React Query hooks for data fetching. This provides the data layer that the Remediation Dashboard page (Task 5) will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()`

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary` and `ProductRemediation` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Implementation Notes
- Follow the existing API layer pattern: typed API functions in `src/api/rest.ts` use the Axios client from `src/api/client.ts`, and React Query hooks in `src/hooks/` wrap those functions. See `src/hooks/useSboms.ts` and `src/api/rest.ts` for established patterns.
  Per CONVENTIONS.md §API Layer: API functions in rest.ts use Axios client; React Query hooks in hooks/ wrap API functions.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.
- Naming: use camelCase for hooks and utility functions, PascalCase for TypeScript interfaces.
  Per CONVENTIONS.md §Naming: camelCase for hooks and utilities, PascalCase for components.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.
- Backend API contracts (verify these against the backend repo during implementation using implement-task cross-repo API verification):
  - `GET /api/v2/remediation/summary` — response shape: `RemediationSummary[]` where each item has `{ severity: string, status: string, count: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
  - `GET /api/v2/remediation/by-product` — response shape: `{ items: ProductRemediation[], total: number }` where each item has `{ product_name: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
- React Query hooks should use appropriate query keys (e.g., `["remediation", "summary"]` and `["remediation", "by-product"]`) for cache management.
- Per docs/constraints.md §5.4: reuse existing Axios client and API patterns — do not create a new HTTP client.

## Reuse Candidates
- `src/api/client.ts::axiosInstance` — configured Axios client with base URL and auth interceptors; use for all API calls
- `src/api/rest.ts::fetchSboms()` — existing API function pattern; follow the same Axios call + return type pattern
- `src/hooks/useSboms.ts` — existing React Query hook pattern; follow the same useQuery setup with typed return
- `src/api/models.ts` — existing TypeScript interface definitions; follow the same interface declaration pattern

## Acceptance Criteria
- [ ] `RemediationSummary` interface is defined with severity, status, and count fields
- [ ] `ProductRemediation` interface is defined with product_name, total, open, in_progress, and resolved fields
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` and returns typed data
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` and returns typed data
- [ ] `useRemediationSummary` hook uses React Query with appropriate query key and returns typed data
- [ ] `useRemediationByProduct` hook uses React Query with appropriate query key and returns typed data

## Test Requirements
- [ ] Unit test: `useRemediationSummary` hook returns expected data shape using MSW mock
- [ ] Unit test: `useRemediationByProduct` hook returns expected data shape using MSW mock
- [ ] Unit test: hooks handle loading and error states correctly

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product API endpoints
