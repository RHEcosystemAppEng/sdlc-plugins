## Repository
trustify-ui

## Target Branch
main

## Description
Add the API layer for the vulnerability remediation tracking dashboard (TC-9006). This includes TypeScript interfaces for the remediation API response types, Axios client functions to call the backend endpoints, and React Query hooks for data fetching. This task establishes the data-fetching foundation that the dashboard page components will consume.

## Files to Modify
- `src/api/models.ts` — Add RemediationSummary, SeverityStatusCount, ProductRemediation, and RemediationByProductResponse interfaces
- `src/api/rest.ts` — Add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for fetching remediation summary data
- `src/hooks/useRemediationByProduct.ts` — React Query hook for fetching per-product remediation breakdown with pagination support

## Implementation Notes
- Per CONVENTIONS.md §API layer: follow the established pattern of Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API layer scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks (useRemediationSummary, useRemediationByProduct) and utility functions (fetchRemediationSummary).
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` naming scope.
- Reference `src/api/rest.ts` for the existing API function pattern (fetchSboms, fetchAdvisories).
- Reference `src/hooks/useSboms.ts` for the React Query hook pattern with useQuery.
- Reference `src/hooks/useAdvisories.ts` for another hook example.
- The API client functions should use the Axios instance from `src/api/client.ts`.
- RemediationSummary interface should mirror the backend struct: a matrix of severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) counts.
- ProductRemediation interface: { productName: string, total: number, open: number, inProgress: number, resolved: number }.
- The by-product hook should accept pagination parameters and return paginated results.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ counts: { severity: string, status: string, count: number }[] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API function pattern; follow for fetchRemediationSummary and fetchRemediationByProduct
- `src/api/rest.ts::fetchAdvisories` — Another API function pattern reference
- `src/api/client.ts::axios instance` — Shared Axios client with base URL and auth interceptors
- `src/hooks/useSboms.ts` — React Query hook pattern with useQuery; follow for useRemediationSummary
- `src/hooks/useAdvisories.ts` — Another React Query hook reference
- `src/api/models.ts` — Existing TypeScript interfaces for API types; add new interfaces here

## Acceptance Criteria
- [ ] RemediationSummary interface matches the backend response shape
- [ ] ProductRemediation interface matches the backend response shape
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed data
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination params
- [ ] useRemediationSummary hook provides loading, error, and data states
- [ ] useRemediationByProduct hook supports pagination parameters

## Test Requirements
- [ ] Unit test for useRemediationSummary hook with MSW mock handler returning sample data
- [ ] Unit test for useRemediationByProduct hook with MSW mock handler returning paginated data
- [ ] Verify hooks handle loading and error states correctly
- [ ] Verify API functions construct correct request URLs and parameters

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints (API contract dependency)
