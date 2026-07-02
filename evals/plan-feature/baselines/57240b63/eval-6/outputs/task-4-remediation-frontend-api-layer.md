## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add the frontend API layer for the remediation tracking dashboard. This includes TypeScript interfaces for the remediation API response types, Axios client functions to call the backend endpoints, and React Query hooks for data fetching. This task establishes the data-fetching foundation that the dashboard UI components (Tasks 5 and 6) will consume.

## Files to Modify
- `src/api/models.ts` -- add RemediationSummary, SeverityStatusCount, RemediationTotals, ProductRemediation, and PaginatedProductRemediation interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() functions using the Axios client

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping fetchRemediationSummary()
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping fetchRemediationByProduct() with pagination parameters

## Implementation Notes
- Add TypeScript interfaces in `src/api/models.ts` following the existing pattern (e.g., adjacent to SbomSummary, AdvisoryDetails interfaces). Define:
  - `SeverityStatusCount`: `{ severity: string; open: number; inProgress: number; resolved: number }`
  - `RemediationTotals`: `{ total: number; open: number; inProgress: number; resolved: number }`
  - `RemediationSummary`: `{ bySeverity: SeverityStatusCount[]; totals: RemediationTotals }`
  - `ProductRemediation`: `{ productId: string; productName: string; total: number; open: number; inProgress: number; resolved: number }`
  - `PaginatedProductRemediation`: `{ items: ProductRemediation[]; total: number }`
  - Applies: task modifies `src/api/models.ts` matching the convention's API layer scope.
- Add API client functions in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`. Follow the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()`:
  - `fetchRemediationSummary(): Promise<RemediationSummary>` -- calls GET /api/v2/remediation/summary
  - `fetchRemediationByProduct(params: { offset?: number; limit?: number }): Promise<PaginatedProductRemediation>` -- calls GET /api/v2/remediation/by-product
  - Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.
- Create React Query hooks in `src/hooks/` following the pattern of `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`. Use `useQuery` from TanStack Query with appropriate query keys:
  - `useRemediationSummary()` -- query key: `["remediation", "summary"]`
  - `useRemediationByProduct({ offset, limit })` -- query key: `["remediation", "by-product", { offset, limit }]`
  - Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's React Query hooks scope.
- Use camelCase for hook file names and function names per the naming convention.
  - Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's naming scope.

### Backend API contracts
- `GET /api/v2/remediation/summary` -- response shape: `{ bySeverity: [{ severity: string, open: number, inProgress: number, resolved: number }], totals: { total: number, open: number, inProgress: number, resolved: number } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: [{ productId: string, productName: string, total: number, open: number, inProgress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; reuse for all API calls
- `src/api/rest.ts::fetchSboms()` -- reference pattern for API client function structure
- `src/hooks/useSboms.ts` -- reference pattern for React Query hook with useQuery
- `src/hooks/useAdvisories.ts` -- reference pattern for list-based React Query hook

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummary, ProductRemediation, and related types are defined in models.ts
- [ ] fetchRemediationSummary() and fetchRemediationByProduct() functions are exported from rest.ts
- [ ] useRemediationSummary hook returns query result with data, isLoading, isError states
- [ ] useRemediationByProduct hook accepts pagination parameters and returns paginated results
- [ ] All new code compiles without TypeScript errors

## Test Requirements
- [ ] Unit test for useRemediationSummary hook verifying it calls the correct endpoint and returns typed data
- [ ] Unit test for useRemediationByProduct hook verifying pagination parameter forwarding
- [ ] Type-check passes with `tsc --noEmit`

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation succeeds with no errors

## Dependencies
- Depends on: Task 2 -- Create remediation REST API endpoints (backend must define the API contract)

---
Description digest: sha256-md:95ce3bb99ff6011315e3efab0ac5387802add277a513701991266c0c2dfe445c
