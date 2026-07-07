## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for calling the backend remediation endpoints, and React Query hooks for data fetching. This establishes the frontend data layer for the remediation tracking dashboard (TC-9006).

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping fetchRemediationSummary()
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping fetchRemediationByProduct() with pagination support

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces: RemediationSummary, SeverityStatusCount, ProductRemediation
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Implementation Notes
- Add TypeScript interfaces in `src/api/models.ts` matching the backend response shapes:
  - `RemediationSummary` — contains arrays of `SeverityStatusCount` entries grouped by severity and status
  - `ProductRemediation` — contains product name, total, open, and resolved counts
- Add API client functions in `src/api/rest.ts` using the existing Axios instance from `src/api/client.ts`. Follow the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()`.
- Create React Query hooks following the pattern of existing hooks like `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`. Use `useQuery` with appropriate query keys and stale time configuration.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: SeverityStatusCount[], total: number }` where SeverityStatusCount has fields `severity: string, status: string, count: number` (see `modules/fundamental/src/remediation/model/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` where ProductRemediation has fields `product: string, total: number, open: number, resolved: number` (see `modules/fundamental/src/remediation/model/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md Section "API layer": Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md Section "State management": React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md Section "Naming": camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for all API calls
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern with typed responses
- `src/hooks/useSboms.ts` — reference for React Query hook pattern with useQuery
- `src/hooks/useAdvisories.ts` — reference for React Query hook pattern for list data
- `src/api/models.ts` — existing TypeScript interfaces to follow naming and structure conventions

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary and ProductRemediation are defined in models.ts
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed response
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination params and returns typed response
- [ ] useRemediationSummary hook provides loading, error, and data states via React Query
- [ ] useRemediationByProduct hook provides loading, error, and data states with pagination support
- [ ] All TypeScript types compile without errors

## Test Requirements
- [ ] Verify useRemediationSummary hook returns loading state initially and data after fetch
- [ ] Verify useRemediationByProduct hook returns loading state initially and data after fetch
- [ ] Verify API functions call correct endpoints with correct parameters
- [ ] Verify error states are handled properly in hooks

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --grep "remediation"` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create remediation domain models and aggregation service
- Depends on: Task 2 — Add remediation REST endpoints with route registration
