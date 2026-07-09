## Repository
trustify-ui

## Target Branch
main

## Description
Add the API layer for the remediation dashboard: TypeScript interfaces for the remediation API response types, Axios client functions for calling the remediation endpoints, and React Query hooks for data fetching. This provides the data access foundation that the dashboard UI components will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data from `GET /api/v2/remediation/summary`
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation breakdown from `GET /api/v2/remediation/by-product`

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `RemediationByProduct`, and `ProductRemediationBreakdown` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Implementation Notes
- Per repo conventions (API layer): follow the established pattern of typed API functions in `src/api/rest.ts` paired with React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms()` and `src/hooks/useSboms.ts` for the canonical example.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API file scope.
- Per repo conventions (State management): use React Query (TanStack Query) for server state. Hooks should use `useQuery` with appropriate query keys and stale time settings.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript hook file scope.
- Per repo conventions (Naming): use camelCase for hooks and utility functions.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript file scope.
- Use the Axios instance from `src/api/client.ts` for all API calls — it includes base URL configuration and auth interceptors.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product` — response shape: `{ items: [{ product_name: string, total: number, open: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern using Axios
- `src/api/rest.ts::fetchAdvisories` — reference for API client function pattern
- `src/hooks/useSboms.ts` — reference for React Query hook pattern with useQuery
- `src/hooks/useAdvisories.ts` — reference for React Query hook pattern
- `src/api/models.ts` — existing TypeScript interfaces to follow naming and structure conventions
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use directly

## Acceptance Criteria
- [ ] TypeScript interfaces for remediation summary and by-product responses are defined in `src/api/models.ts`
- [ ] API client functions `fetchRemediationSummary()` and `fetchRemediationByProduct()` are implemented in `src/api/rest.ts`
- [ ] React Query hooks `useRemediationSummary` and `useRemediationByProduct` are implemented and export correctly
- [ ] All types are properly typed (no `any` types)
- [ ] Hooks follow the established pattern (query keys, error handling)

## Test Requirements
- [ ] Verify TypeScript compilation passes with no type errors
- [ ] Verify hooks return correctly typed data when called with mocked API responses
- [ ] Verify error states are handled by the hooks

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
- Depends on: Task 2 — Add remediation by-product endpoint
