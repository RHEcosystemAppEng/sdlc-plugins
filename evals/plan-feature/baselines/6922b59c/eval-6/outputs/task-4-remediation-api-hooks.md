## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for remediation API response types, API client functions
for the remediation endpoints, and React Query hooks for data fetching. This provides
the data layer that the remediation dashboard page will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()` for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` for the by-product endpoint

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCount`, and `ProductRemediation` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Implementation Notes
- Follow the established API layer pattern: typed interfaces in `src/api/models.ts`, Axios-based client functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
  Per CONVENTIONS.md §API Layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.
- Use the existing Axios instance from `src/api/client.ts` for HTTP requests — do not create a separate client.
- `RemediationSummary` interface should match the backend struct: `{ severityStatusCounts: SeverityStatusCount[], totalOpen: number, totalInProgress: number, totalResolved: number }`.
- `SeverityStatusCount` interface: `{ severity: string, status: string, count: number }`.
- `ProductRemediation` interface: `{ productName: string, total: number, open: number, resolved: number }`.
- React Query hooks should follow the existing hook patterns (e.g., `useSboms.ts`): use `useQuery` with appropriate query keys and stale time configuration.
  Per CONVENTIONS.md §State Management: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook file scope.
- The by-product hook should accept optional pagination parameters (offset, limit).
- Follow camelCase naming for hooks and utility functions.
  Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ severityStatusCounts: SeverityStatusCount[], totalOpen: number, totalInProgress: number, totalResolved: number }`
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` (paginated)

Verify these contracts against the backend repo during implementation using the
implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; reuse for all API calls
- `src/api/rest.ts::fetchSboms` — reference for API client function implementation pattern
- `src/hooks/useSboms.ts` — reference for React Query hook implementation with useQuery
- `src/api/models.ts` — reference for TypeScript interface definition patterns

## Acceptance Criteria
- [ ] `RemediationSummary` interface is defined in `src/api/models.ts` with correct field types
- [ ] `SeverityStatusCount` interface is defined with severity, status, and count fields
- [ ] `ProductRemediation` interface is defined with productName, total, open, and resolved fields
- [ ] `fetchRemediationSummary()` function calls `GET /api/v2/remediation/summary` using the shared Axios client
- [ ] `fetchRemediationByProduct()` function calls `GET /api/v2/remediation/by-product` with optional pagination params
- [ ] `useRemediationSummary` hook returns query result with loading, error, and data states
- [ ] `useRemediationByProduct` hook accepts pagination parameters and returns paginated results

## Test Requirements
- [ ] Unit test for `fetchRemediationSummary()` using MSW to mock the API response
- [ ] Unit test for `fetchRemediationByProduct()` using MSW to mock paginated response
- [ ] Unit test for `useRemediationSummary` hook verifying React Query integration
- [ ] Unit test for `useRemediationByProduct` hook verifying pagination parameter passing

## Verification Commands
- `npx vitest run --reporter=verbose src/hooks/useRemediationSummary.test.ts` — run summary hook tests
- `npx vitest run --reporter=verbose src/hooks/useRemediationByProduct.test.ts` — run by-product hook tests

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product REST endpoints (API contracts must be finalized)
