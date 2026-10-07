## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for remediation API response types, API client functions to call the remediation endpoints, and React Query hooks for data fetching. This establishes the data layer that the remediation dashboard components will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for RemediationSummary, SeverityBreakdown, StatusBreakdown, ProductRemediation
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping fetchRemediationSummary()
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping fetchRemediationByProduct()

## Implementation Notes
- Follow the established API layer pattern: types in `src/api/models.ts`, client functions in `src/api/rest.ts`, hooks in `src/hooks/`.
- Reference `src/hooks/useSboms.ts` for the React Query hook pattern — use `useQuery` with a typed query key and the corresponding API function.
- The Axios client in `src/api/client.ts` is pre-configured with base URL and auth interceptors — use it for all API calls, do not create a new client instance.
- Per CONVENTIONS.md §API Layer: follow the Axios client -> typed API functions -> React Query hooks pattern. Applies: task modifies `src/api/rest.ts` matching the convention's API client file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks (useRemediationSummary, useRemediationByProduct) and camelCase for utility functions. Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's hook file scope.
- Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state, no Redux. Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's hook file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ by_severity: [{ severity: string, open: number, in_progress: number, resolved: number }], by_status: [{ status: string, count: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product` — response shape: `{ items: [{ product_name: string, total: number, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — API client function pattern to follow for request construction
- `src/api/models.ts` — existing TypeScript interfaces for reference on naming and structure
- `src/hooks/useSboms.ts` — React Query hook pattern with useQuery, typed query key, and error handling
- `src/api/client.ts` — Axios instance with auth interceptors, reuse directly for API calls

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary and ProductRemediation are defined in models.ts
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed response
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination support
- [ ] useRemediationSummary hook provides loading, error, and data states
- [ ] useRemediationByProduct hook provides loading, error, and data states with refetch capability

## Test Requirements
- [ ] Verify API client functions construct correct request URLs
- [ ] Verify React Query hooks handle loading, success, and error states
- [ ] Verify TypeScript interfaces match the expected backend response shape

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints (backend must define the API contract)
