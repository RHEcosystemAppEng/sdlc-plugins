# Task 4: Add remediation API types, client functions, and React Query hooks

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the API integration layer for the remediation dashboard: TypeScript interfaces for remediation response types, Axios client functions to call the backend remediation endpoints, and React Query hooks for data fetching. This provides the data layer that the dashboard UI components (Tasks 5 and 6) will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for `RemediationSummaryItem`, `RemediationSummaryResponse`, `ProductRemediationItem`, and `ProductRemediationResponse`
- `src/api/rest.ts` -- add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping `fetchRemediationByProduct()`

## Implementation Notes
- Follow the existing API layer pattern: TypeScript interfaces in `src/api/models.ts`, Axios functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
- Use the Axios instance from `src/api/client.ts` which has base URL and auth interceptors already configured.
- React Query hooks follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` -- use `useQuery` with typed generics.
- Use unique query keys for cache management (e.g., `["remediation", "summary"]` and `["remediation", "by-product"]`).

### Backend API contracts:
- `GET /api/v2/remediation/summary` -- response shape: `{ items: RemediationSummaryItem[], total: number }` where `RemediationSummaryItem = { severity: "Critical" | "High" | "Medium" | "Low", status: "Open" | "In Progress" | "Resolved", count: number }`
- `GET /api/v2/remediation/by-product` -- response shape: `{ items: ProductRemediationItem[], total: number }` where `ProductRemediationItem = { product: string, total: number, open: number, in_progress: number, resolved: number }`

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms()` -- reference for API client function pattern with typed responses
- `src/hooks/useSboms.ts` -- reference for React Query useQuery hook pattern
- `src/hooks/useAdvisories.ts` -- reference for React Query hook with list data
- `src/api/client.ts` -- Axios instance to use for all API calls

## Acceptance Criteria
- [ ] TypeScript interfaces `RemediationSummaryItem`, `RemediationSummaryResponse`, `ProductRemediationItem`, and `ProductRemediationResponse` are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` function exists in `src/api/rest.ts` and calls `GET /api/v2/remediation/summary`
- [ ] `fetchRemediationByProduct()` function exists in `src/api/rest.ts` and calls `GET /api/v2/remediation/by-product`
- [ ] `useRemediationSummary` hook exists and returns typed React Query result
- [ ] `useRemediationByProduct` hook exists and returns typed React Query result
- [ ] Both hooks use the Axios instance from `src/api/client.ts`

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook using MSW to mock the API response, verifying correct data return
- [ ] Unit test for `useRemediationByProduct` hook using MSW to mock the API response, verifying correct data return
- [ ] Add MSW handler for `GET /api/v2/remediation/summary` in `tests/mocks/handlers.ts`
- [ ] Add MSW handler for `GET /api/v2/remediation/by-product` in `tests/mocks/handlers.ts`
- [ ] Add mock fixture data for remediation responses in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 2 -- Add remediation aggregation service and API endpoints (defines the response shapes)
