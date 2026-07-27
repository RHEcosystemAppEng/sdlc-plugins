## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add TypeScript interfaces for remediation API response types and API client functions to call the new backend remediation endpoints. This provides the data layer that React Query hooks (Task 6) will consume.

## Files to Modify
- `src/api/models.ts` -- add RemediationSummaryItem, RemediationSummaryResponse, ProductRemediationItem, and ProductRemediationResponse TypeScript interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() API client functions using the Axios instance

## Implementation Notes
- Add TypeScript interfaces to `src/api/models.ts` following the existing interface patterns (e.g., the patterns used for SBOM and advisory response types).
  Per CONVENTIONS.md: TypeScript interfaces for API response types live in src/api/models.ts.
  Applies: task modifies `src/api/models.ts` matching the convention's TypeScript file scope.
- Add API client functions to `src/api/rest.ts` following the existing function patterns (e.g., fetchSboms(), fetchAdvisories()). Use the Axios instance from `src/api/client.ts`.
  Per CONVENTIONS.md: API client functions are typed functions in src/api/rest.ts using Axios client from src/api/client.ts.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript file scope.
- Use camelCase for function and variable names per project naming conventions.
  Per CONVENTIONS.md: camelCase for hooks and utilities.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ items: [{ severity: string, status: string, count: number }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product` -- response shape: `{ items: [{ product_name: string, total: number, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` -- existing TypeScript interfaces for SBOMs and advisories; follow the same interface definition pattern
- `src/api/rest.ts` -- existing API client functions (fetchSboms, fetchAdvisories); follow the same function signature and Axios usage pattern
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; reuse for all API calls

## Acceptance Criteria
- [ ] RemediationSummaryItem interface defines severity, status, and count fields
- [ ] RemediationSummaryResponse interface wraps an array of RemediationSummaryItem
- [ ] ProductRemediationItem interface defines product_name, total, open, in_progress, and resolved fields
- [ ] ProductRemediationResponse interface wraps an array of ProductRemediationItem with total count
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary and returns typed response
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with optional pagination params and returns typed response

## Test Requirements
- [ ] Verify TypeScript interfaces compile without errors
- [ ] Verify API client functions call correct endpoints with expected parameters
- [ ] Verify response types match backend API contract

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 3 -- Add remediation API endpoints and register routes
