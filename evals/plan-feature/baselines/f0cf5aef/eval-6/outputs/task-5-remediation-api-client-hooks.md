## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add TypeScript interfaces for remediation API response types, API client functions for the three remediation endpoints, and React Query hooks for data fetching. This task establishes the data layer that the remediation dashboard page and its components consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for remediation response types
- `src/api/rest.ts` — add API client functions for remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for `GET /api/v2/remediation/summary`
- `src/hooks/useRemediationByProduct.ts` — React Query hook for `GET /api/v2/remediation/by-product`
- `tests/mocks/fixtures/remediation.json` — mock remediation data for MSW handlers
- `tests/mocks/fixtures/remediation-by-product.json` — mock per-product remediation data

## API Changes
- Consumes `GET /api/v2/remediation/summary` (defined in Task 2)
- Consumes `GET /api/v2/remediation/by-product` (defined in Task 3)
- Consumes `GET /api/v2/remediation/export` (defined in Task 4)

## Implementation Notes
- **TypeScript interfaces** to add in `src/api/models.ts`:
  - `RemediationSeverityCount` — `{ severity: string; open: number; in_progress: number; resolved: number }`
  - `RemediationSummary` — `{ items: RemediationSeverityCount[]; total: number }`
  - `ProductRemediation` — `{ product_name: string; total: number; open: number; in_progress: number; resolved: number }`
  - `ProductRemediationResponse` — `{ items: ProductRemediation[]; total: number }` (matches `PaginatedResults<ProductRemediation>`)
- **API client functions** in `src/api/rest.ts`: follow the existing pattern of `fetchSboms()`, `fetchAdvisories()`. Add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, and `fetchRemediationExport()`.
- Use the existing Axios instance from `src/api/client.ts` for all API calls.
- **React Query hooks**: follow the existing pattern in `src/hooks/useSboms.ts`. Each hook wraps `useQuery` with the appropriate query key and fetch function.
- For the export function, return a Blob response that the calling component can use to trigger a file download.
- **MSW handlers**: add handlers in `tests/mocks/handlers.ts` for the three remediation endpoints, serving the fixture data from the new JSON files.
- Follow naming conventions: camelCase for hooks and API functions.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `PaginatedResults<ProductRemediation>` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
- `GET /api/v2/remediation/export` — response: CSV file with Content-Type `text/csv` (see `modules/fundamental/src/remediation/endpoints/export.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts` — existing API client functions (`fetchSboms()`, `fetchAdvisories()`) as pattern references
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useRemediationSummary`
- `src/hooks/useAdvisories.ts` — React Query hook pattern for list queries with parameters
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — fixture data format reference

## Acceptance Criteria
- [ ] TypeScript interfaces for `RemediationSummary`, `RemediationSeverityCount`, `ProductRemediation`, and `ProductRemediationResponse` are added to `src/api/models.ts`
- [ ] API client functions `fetchRemediationSummary()`, `fetchRemediationByProduct()`, and `fetchRemediationExport()` are added to `src/api/rest.ts`
- [ ] `useRemediationSummary` hook fetches and returns remediation summary data via React Query
- [ ] `useRemediationByProduct` hook fetches and returns per-product remediation data with pagination parameters
- [ ] MSW handlers serve mock data for all three remediation endpoints in tests

## Test Requirements
- [ ] Unit test: `useRemediationSummary` hook returns expected data from MSW mock
- [ ] Unit test: `useRemediationByProduct` hook returns expected paginated data from MSW mock
- [ ] Unit test: `fetchRemediationExport()` returns a Blob response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary aggregation service and endpoint (API contract)
- Depends on: Task 3 — Add per-product remediation breakdown endpoint (API contract)
