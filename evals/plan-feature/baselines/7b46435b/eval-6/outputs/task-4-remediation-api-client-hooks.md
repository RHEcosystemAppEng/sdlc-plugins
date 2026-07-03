## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript type definitions for the remediation API responses, API client functions to call the new backend endpoints, and React Query hooks for data fetching. This establishes the data layer that the remediation dashboard page components will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for per-product remediation data with pagination support

## Files to Modify
- `src/api/models.ts` -- add RemediationSummary, SeverityStatusCount, ProductRemediation TypeScript interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Implementation Notes
- Follow the existing React Query hook pattern established in `src/hooks/useAdvisories.ts` and `src/hooks/useSboms.ts`: export a custom hook that wraps `useQuery` with a typed query key and fetcher function from `src/api/rest.ts`.
  Per CONVENTIONS.md section "API layer": Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` scope.

- Add TypeScript interfaces in `src/api/models.ts` following the existing pattern for API response types (reference `SbomSummary`, `AdvisorySummary` interface patterns).

- API client functions in `src/api/rest.ts` should use the Axios instance from `src/api/client.ts` for base URL and auth interceptors.

- The `useRemediationByProduct` hook should accept pagination parameters (offset, limit) and optionally filter parameters (product name search) as hook arguments.

- The `useRemediationSummary` hook should return the full summary object with by-severity breakdown and totals.

**Backend API contracts (planned):**
- `GET /api/v2/remediation/summary` -- response shape: `{ by_severity: Array<{ severity: string, open: number, in_progress: number, resolved: number }>, totals: { open: number, in_progress: number, resolved: number } }`
  (See `modules/fundamental/src/remediation/model/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: Array<{ product_name: string, total: number, open: number, in_progress: number, resolved: number }>, total: number }`
  (See `modules/fundamental/src/remediation/model/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/hooks/useAdvisories.ts` -- reference React Query hook pattern with useQuery, typed query key, and error handling
- `src/hooks/useSboms.ts` -- reference React Query hook with pagination parameter support
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors (use directly, do not create a new client)
- `src/api/models.ts` -- existing TypeScript interface patterns for API response types (SbomSummary, AdvisorySummary)
- `src/api/rest.ts` -- existing API client function patterns (fetchSboms, fetchAdvisories)

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary, SeverityStatusCount, and ProductRemediation are defined in src/api/models.ts
- [ ] fetchRemediationSummary() function is added to src/api/rest.ts and calls GET /api/v2/remediation/summary
- [ ] fetchRemediationByProduct() function is added to src/api/rest.ts and calls GET /api/v2/remediation/by-product with pagination parameters
- [ ] useRemediationSummary hook returns typed remediation summary data with loading/error states
- [ ] useRemediationByProduct hook returns typed paginated per-product data with pagination support
- [ ] All TypeScript types compile without errors

## Test Requirements
- [ ] Unit test verifying useRemediationSummary hook fetches and returns correctly typed data (using MSW mock handler)
- [ ] Unit test verifying useRemediationByProduct hook passes pagination parameters correctly
- [ ] Unit test verifying hooks handle loading and error states appropriately

## Verification Commands
- `npm run typecheck` -- verify TypeScript compilation with new types
- `npm run test` -- run unit tests

## Dependencies
- Depends on: Task 1 -- Add remediation module with summary aggregation endpoint
- Depends on: Task 2 -- Add remediation by-product breakdown endpoint
