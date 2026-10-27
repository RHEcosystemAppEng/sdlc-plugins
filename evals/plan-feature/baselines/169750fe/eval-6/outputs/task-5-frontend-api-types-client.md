## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for the remediation API response types and API client functions to call the backend remediation endpoints. This provides the data layer that React Query hooks and page components will consume.

## Files to Modify
- `src/api/models.ts` — add RemediationSummary and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Implementation Notes
- Add interfaces in `src/api/models.ts` alongside existing types like `SbomSummary` and `AdvisoryDetails`:
  - `RemediationSummary`: severity × status count matrix
  - `ProductRemediation`: product name, total, open, inProgress, resolved counts
  - `PaginatedProductRemediation`: wraps `ProductRemediation[]` with total count for pagination
- Add API client functions in `src/api/rest.ts` following the pattern of `fetchSboms()` and `fetchAdvisories()`:
  - `fetchRemediationSummary()` — calls `GET /api/v2/remediation/summary`
  - `fetchRemediationByProduct(params)` — calls `GET /api/v2/remediation/by-product` with pagination params
- Use the Axios instance from `src/api/client.ts` for HTTP requests, matching existing patterns.
- Per Key Conventions: API layer follows Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`.
Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.
- Per Key Conventions: camelCase for hooks and utilities.
Applies: task modifies `src/api/models.ts` matching the convention's naming scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `RemediationSummary` with severity × status count matrix (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` — example API client function with pagination
- `src/api/models.ts` — existing TypeScript interface patterns
- `src/api/client.ts` — Axios instance with auth interceptors

## Acceptance Criteria
- [ ] `RemediationSummary` interface matches the backend response shape
- [ ] `ProductRemediation` interface includes product name, total, open, inProgress, resolved
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with pagination params
- [ ] Functions use the shared Axios client instance

## Test Requirements
- [ ] TypeScript compilation passes with the new interfaces and functions
- [ ] API client functions handle error responses correctly

## Dependencies
- Depends on: Task 2 — Remediation summary endpoint
- Depends on: Task 3 — Remediation by-product endpoint
