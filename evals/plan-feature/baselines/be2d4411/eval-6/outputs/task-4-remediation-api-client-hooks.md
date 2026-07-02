## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, API client functions for the two remediation endpoints, and React Query hooks for data fetching. This task establishes the data layer that the dashboard page (Task 5) and vulnerability table (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` — add RemediationSummary, SeverityStatusCount, ProductRemediation, and PaginatedProductRemediation interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping fetchRemediationSummary
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping fetchRemediationByProduct with pagination params

## Implementation Notes
- Follow the existing API layer pattern: typed functions in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, wrapped by React Query hooks in `src/hooks/`.
  Per CONVENTIONS.md: API client functions go in src/api/rest.ts; React Query hooks go in src/hooks/.
  Applies: task modifies `src/api/rest.ts` matching the convention's .ts API file scope.
- Model the TypeScript interfaces to match the backend response shapes:
  - `RemediationSummary = { items: SeverityStatusCount[], total: number }` where `SeverityStatusCount = { severity: string, open: number, in_progress: number, resolved: number }`
  - `PaginatedProductRemediation = { items: ProductRemediation[], total: number }` where `ProductRemediation = { product_name: string, total: number, open: number, in_progress: number, resolved: number }`
- React Query hooks should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` — use `useQuery` with appropriate query keys and stale time.
- The by-product hook should accept pagination parameters (offset, limit) and include them in the query key for proper cache management.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: SeverityStatusCount[], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `PaginatedResults<ProductRemediation>` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern
- `src/hooks/useSboms.ts` — reference for React Query hook pattern with useQuery
- `src/hooks/useAdvisories.ts` — reference for list query hook pattern

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary, SeverityStatusCount, ProductRemediation are defined in models.ts
- [ ] fetchRemediationSummary() and fetchRemediationByProduct() functions are added to rest.ts
- [ ] useRemediationSummary hook returns query result with loading, error, and data states
- [ ] useRemediationByProduct hook accepts pagination params and returns paginated query result
- [ ] All types are exported and consumable by page components

## Test Requirements
- [ ] Type-check passes with no errors (`tsc --noEmit`)
- [ ] Hook returns expected loading/error/data states (verified in Task 7's unit tests)

## Verification Commands
- `npx tsc --noEmit` — verify TypeScript compilation with no type errors

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint

[sdlc-workflow] Description digest: sha256-md:0f8bcc37b349d18ed57bbd7a545be96faeddd4005b02506d8a499651d45f7298
