## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for remediation API response types, API client functions for calling the remediation endpoints, and React Query hooks for data fetching. This establishes the data layer that the remediation dashboard page components will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation breakdown with pagination support

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: RemediationSummary, SeverityStatusCount, ProductRemediation, RemediationByProductResponse
- `src/api/rest.ts` — add API client functions: fetchRemediationSummary(), fetchRemediationByProduct()

## API Changes
- `GET /api/v2/remediation/summary` — CONSUME: frontend calls this endpoint for summary card and chart data
- `GET /api/v2/remediation/by-product` — CONSUME: frontend calls this endpoint for product filter and table data

## Implementation Notes
Per CONVENTIONS.md §API Layer: follow the Axios client pattern in `src/api/client.ts` for base URL and auth interceptors; add typed API functions in `src/api/rest.ts`; create React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state. Follow the existing hook patterns in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md §Naming: use camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ severityCounts: { critical: { open: number, inProgress: number, resolved: number }, high: {...}, medium: {...}, low: {...} }, totalOpen: number, totalInProgress: number, totalResolved: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` where ProductRemediation is `{ productName: string, total: number, open: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` — reference for API client function pattern with typed responses
- `src/api/rest.ts::fetchAdvisories()` — reference for list endpoint client function with pagination
- `src/hooks/useSboms.ts` — reference for React Query useQuery hook pattern
- `src/hooks/useAdvisories.ts` — reference for React Query hook with query parameters
- `src/api/models.ts` — existing TypeScript interfaces to follow for new type definitions
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] RemediationSummary TypeScript interface matches the backend response shape
- [ ] ProductRemediation TypeScript interface matches the backend by-product response shape
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed data
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination parameters
- [ ] useRemediationSummary hook provides loading, error, and data states
- [ ] useRemediationByProduct hook supports pagination parameter changes

## Test Requirements
- [ ] Unit test for fetchRemediationSummary correctly calling the API endpoint
- [ ] Unit test for fetchRemediationByProduct correctly passing pagination parameters
- [ ] Unit test for useRemediationSummary hook returning correct data shape
- [ ] Unit test for useRemediationByProduct hook with pagination state management

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints
