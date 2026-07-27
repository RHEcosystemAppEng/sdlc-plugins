# Task 5: Add remediation API types, client functions, and hooks

**Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for calling the remediation endpoints, and React Query hooks for data fetching. This task establishes the data layer that the dashboard page components will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation breakdown

## Files to Modify
- `src/api/models.ts` — add RemediationSummary and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## API Changes
- `GET /api/v2/remediation/summary` — NEW client function: `fetchRemediationSummary()` returning `RemediationSummary[]`
- `GET /api/v2/remediation/by-product` — NEW client function: `fetchRemediationByProduct(params)` returning `PaginatedResult<ProductRemediation>`

## Implementation Notes
- Add TypeScript interfaces to `src/api/models.ts` following the existing pattern for `SbomSummary` and `AdvisorySummary`:
  - `RemediationSummary`: `{ severity: string; open: number; in_progress: number; resolved: number }`
  - `ProductRemediation`: `{ product_name: string; total: number; open: number; in_progress: number; resolved: number }`
- Add API client functions to `src/api/rest.ts` following the pattern of `fetchSboms()` and `fetchAdvisories()` — use the Axios instance from `src/api/client.ts` with typed responses.
- Create React Query hooks following the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`:
  - `useRemediationSummary()` — `useQuery` with a `["remediation", "summary"]` query key
  - `useRemediationByProduct(params)` — `useQuery` with a `["remediation", "by-product", params]` query key supporting pagination parameters
- Use camelCase for hooks and utility function names per project naming conventions.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `PaginatedResults<ProductRemediation>` where `ProductRemediation = { product_name: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces for API types; extend with remediation types
- `src/api/rest.ts` — existing API client functions (fetchSboms, fetchAdvisories); follow the same Axios call pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for all API calls
- `src/hooks/useSboms.ts` — React Query hook pattern for list data; replicate for remediation summary
- `src/hooks/useAdvisories.ts` — React Query hook pattern; replicate for remediation by-product

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary and ProductRemediation are defined in models.ts
- [ ] API client functions fetchRemediationSummary and fetchRemediationByProduct are implemented in rest.ts
- [ ] React Query hooks useRemediationSummary and useRemediationByProduct are created
- [ ] Hooks use appropriate query keys and support refetching and caching
- [ ] All types are properly exported for use by page components

## Test Requirements
- [ ] Unit test verifying useRemediationSummary hook calls the correct API endpoint
- [ ] Unit test verifying useRemediationByProduct hook passes pagination parameters correctly
- [ ] Unit test verifying hooks handle loading, error, and success states

## Verification Commands
- `npx vitest run src/hooks/useRemediationSummary` — run hook unit tests
- `npx tsc --noEmit` — verify TypeScript types compile without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
