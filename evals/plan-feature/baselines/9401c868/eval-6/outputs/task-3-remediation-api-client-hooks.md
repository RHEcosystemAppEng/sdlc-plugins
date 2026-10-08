## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript API types, client functions, and React Query hooks for the new remediation backend endpoints. This provides the data-fetching layer that the remediation dashboard page and components will consume. Includes type definitions matching the backend response shapes, Axios-based API functions, and React Query hooks for caching and state management.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for `GET /api/v2/remediation/summary`
- `src/hooks/useRemediationByProduct.ts` — React Query hook for `GET /api/v2/remediation/by-product`

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `ProductRemediation`, and related TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Implementation Notes
- Per CONVENTIONS.md §API Layer: follow the established pattern of Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms` and `src/hooks/useSboms.ts` for the established pattern.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API layer scope.
- Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state — no Redux. See `src/hooks/useSboms.ts` for query key and options pattern.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions. Hook files follow the `use<Entity>.ts` naming pattern.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product` — response shape: `{ items: [{ product_name: string, product_id: string, total: number, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for remediation endpoints
- `src/api/rest.ts::fetchAdvisories` — another API function example with similar response shape
- `src/hooks/useSboms.ts` — React Query hook pattern with query keys and options
- `src/hooks/useAdvisories.ts` — another hook example for list data
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (import and use directly)

## Acceptance Criteria
- [ ] `RemediationSummary` and `ProductRemediation` TypeScript interfaces defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function in `src/api/rest.ts` calls `GET /api/v2/remediation/summary` and returns typed response
- [ ] `fetchRemediationByProduct()` function in `src/api/rest.ts` calls `GET /api/v2/remediation/by-product` and returns typed response
- [ ] `useRemediationSummary` hook provides loading, error, and data states via React Query
- [ ] `useRemediationByProduct` hook provides loading, error, and data states with pagination support
- [ ] All TypeScript types compile without errors

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook verifying data fetching and caching behavior using MSW mock handlers
- [ ] Unit test for `useRemediationByProduct` hook verifying data fetching and pagination
- [ ] Add MSW handlers in `tests/mocks/handlers.ts` for remediation endpoints

## Verification Commands
- `npx tsc --noEmit` — TypeScript type checking passes
- `npx vitest run --reporter=verbose` — unit tests pass

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
