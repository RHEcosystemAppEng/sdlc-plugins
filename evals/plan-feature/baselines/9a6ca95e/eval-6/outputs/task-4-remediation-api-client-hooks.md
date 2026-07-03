## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for remediation API response types, API client functions for fetching remediation data, and React Query hooks for consuming the backend remediation endpoints. This provides the data layer that the dashboard UI components will use.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook for remediation summary data
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for per-product remediation data

## Files to Modify
- `src/api/models.ts` -- add RemediationSummary, SeverityStatusCount, and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## API Changes
- `GET /api/v2/remediation/summary` -- CONSUME: fetch aggregated remediation counts by severity and status
- `GET /api/v2/remediation/by-product` -- CONSUME: fetch per-product remediation breakdown with pagination

## Implementation Notes
- Add TypeScript interfaces in `src/api/models.ts` following the existing pattern for API response types (see existing interfaces in that file for SBOMs and advisories).
- Add API client functions in `src/api/rest.ts` following the pattern of `fetchSboms()` and `fetchAdvisories()` -- use the Axios instance from `src/api/client.ts`.
- Create React Query hooks in `src/hooks/` following the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` -- use `useQuery` with appropriate query keys and stale times.
- The by-product hook should support pagination parameters consistent with existing list hooks.
- Use the severity type definitions from `src/utils/severityUtils.ts` for severity level typing (Critical, High, Medium, Low).

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ bySeverity: { critical: { open: number, inProgress: number, resolved: number }, high: {...}, medium: {...}, low: {...} }, totals: { open: number, inProgress: number, resolved: number } }`
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: ProductRemediation[], total: number }` where ProductRemediation = `{ productName: string, total: number, open: number, resolved: number }`

Verify these contracts against the backend repo during implementation.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` -- reference pattern for API client function with Axios
- `src/hooks/useSboms.ts` -- reference pattern for React Query useQuery hook
- `src/hooks/useAdvisories.ts` -- reference pattern for React Query useQuery hook
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] RemediationSummary and ProductRemediation TypeScript interfaces are defined in models.ts
- [ ] fetchRemediationSummary() and fetchRemediationByProduct() functions are implemented in rest.ts
- [ ] useRemediationSummary hook returns typed remediation summary data
- [ ] useRemediationByProduct hook returns typed per-product data with pagination support
- [ ] All functions use the shared Axios client instance from src/api/client.ts

## Test Requirements
- [ ] Unit test for useRemediationSummary hook using MSW to mock the API response
- [ ] Unit test for useRemediationByProduct hook with pagination parameters
- [ ] Test error handling when API returns a non-200 response
- [ ] Test that TypeScript types match the expected API response shapes

## Verification Commands
- `npm run type-check` -- verify TypeScript compilation
- `npm test -- --grep remediation` -- run remediation-related tests

## Dependencies
- Depends on: Task 2 -- Add remediation REST endpoints (backend API must be defined)
