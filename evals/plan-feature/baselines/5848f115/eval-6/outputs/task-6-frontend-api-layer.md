# Task 6 — Add remediation API layer (types, client, hooks)

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the TypeScript interfaces, API client functions, and React Query hooks for the remediation aggregation endpoints. This establishes the data-fetching layer that the remediation dashboard page (Task 7) will consume. The API layer calls `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` on the backend.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `RemediationSummary`, `SeverityBreakdown`, `ProductRemediation`
- `src/api/rest.ts` — Add API client functions: `fetchRemediationSummary()`, `fetchRemediationByProduct(params?: PaginationParams)`

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` with pagination support

## Implementation Notes
- Follow the existing API layer pattern: interfaces in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- Model the TypeScript interfaces after the backend response shapes:
  - `RemediationSummary`: `{ totalOpen: number, totalInProgress: number, totalResolved: number, breakdowns: SeverityBreakdown[] }`
  - `SeverityBreakdown`: `{ severity: string, open: number, inProgress: number, resolved: number }`
  - `ProductRemediation`: `{ productName: string, total: number, open: number, inProgress: number, resolved: number }`
- Use the Axios instance from `src/api/client.ts` for HTTP requests, following the pattern in `fetchSboms()` and `fetchAdvisories()` in `src/api/rest.ts`.
- React Query hooks should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`: export a custom hook that calls `useQuery` with a unique query key and the API client function.
- The by-product hook should accept optional pagination parameters and pass them as query parameters.
- Per Key Conventions (API layer): Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` file scope.
- Per Key Conventions (Naming): camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `RemediationSummary` with `totalOpen`, `totalInProgress`, `totalResolved`, `breakdowns: SeverityBreakdown[]` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `PaginatedResults<ProductRemediation>` with `items: ProductRemediation[], total: number` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — Existing TypeScript interfaces for API response types (pattern reference)
- `src/api/rest.ts::fetchSboms` — API client function pattern for list endpoints
- `src/api/rest.ts::fetchAdvisories` — API client function pattern for list endpoints
- `src/hooks/useSboms.ts` — React Query hook pattern for list data
- `src/hooks/useAdvisories.ts` — React Query hook pattern for list data
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces `RemediationSummary`, `SeverityBreakdown`, and `ProductRemediation` are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` and `fetchRemediationByProduct()` are implemented in `src/api/rest.ts`
- [ ] `useRemediationSummary` hook is implemented using React Query's `useQuery`
- [ ] `useRemediationByProduct` hook is implemented with pagination parameter support
- [ ] All API functions use the shared Axios instance from `src/api/client.ts`

## Test Requirements
- [ ] Verify TypeScript interfaces compile correctly and match the backend response shape
- [ ] Verify hooks return loading, error, and data states correctly using React Testing Library
- [ ] Verify API client functions construct the correct request URLs and parameters

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 4 — Add remediation summary and by-product endpoints

## Parent Epic
TC-9006: trustify-ui
