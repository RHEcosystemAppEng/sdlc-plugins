## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for the remediation API response types and API client functions for the two new endpoints. This provides the typed data layer that React Query hooks and page components will consume.

## Files to Modify
- `src/api/models.ts` — add RemediationSummary, SeverityStatusCount, RemediationByProduct, and ProductRemediationEntry interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Implementation Notes
Follow existing patterns in the API layer:

- **Type definitions** in `src/api/models.ts`: add interfaces matching the backend response shapes. Follow the naming conventions of existing interfaces like SbomSummary and AdvisoryDetails in the same file.
  - `SeverityStatusCount` — { severity: string, status: string, count: number }
  - `RemediationSummary` — { items: SeverityStatusCount[] }
  - `ProductRemediationEntry` — { product: string, total: number, open: number, resolved: number }
  - `RemediationByProduct` — { items: ProductRemediationEntry[] }

- **API client functions** in `src/api/rest.ts`: add typed fetch functions using the Axios instance from `src/api/client.ts`. Follow the pattern of `fetchSboms()` and `fetchAdvisories()` in the same file.
  - `fetchRemediationSummary()` → GET /api/v2/remediation/summary
  - `fetchRemediationByProduct()` → GET /api/v2/remediation/by-product

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `RemediationSummary` (see `modules/fundamental/src/remediation/model/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product` — response shape: `RemediationByProduct` (see `modules/fundamental/src/remediation/model/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Acceptance Criteria
- [ ] TypeScript interfaces match backend response shapes
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed response
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product and returns typed response
- [ ] API functions use the existing Axios instance from client.ts
- [ ] No TypeScript compilation errors

## Test Requirements
- [ ] Type-level verification: interfaces compile and are exported
- [ ] API function tests with MSW mock handlers verify correct endpoint paths and response parsing

## Dependencies
- Depends on: Task 3 — Remediation endpoints (backend API must exist)
