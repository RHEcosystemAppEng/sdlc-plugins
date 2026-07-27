## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add React Query hooks for fetching remediation data from the backend API. These hooks encapsulate the API calls created in Task 5 and provide loading, error, and data states for the dashboard components created in Tasks 7 and 8.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping fetchRemediationSummary(), returns query result with RemediationSummaryResponse data
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping fetchRemediationByProduct(), supports pagination parameters, returns query result with ProductRemediationResponse data

## Implementation Notes
- Follow the React Query hook pattern established in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`: use `useQuery` from TanStack Query with typed query keys and return values.
  Per CONVENTIONS.md: React Query (TanStack Query) for server state; hooks in src/hooks/.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript file scope.
- Use camelCase for hook names (useRemediationSummary, useRemediationByProduct) per project naming conventions.
  Per CONVENTIONS.md: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript file scope.
- The useRemediationByProduct hook should accept optional pagination parameters (offset, limit) and include them in the query key for proper cache management.

## Reuse Candidates
- `src/hooks/useSboms.ts` -- React Query hook for SBOM list; follow as template for useRemediationSummary and useRemediationByProduct
- `src/hooks/useAdvisories.ts` -- React Query hook for advisory list; reference for query key patterns and pagination handling
- `src/hooks/useSbomById.ts` -- React Query hook for single entity; reference for query key patterns

## Acceptance Criteria
- [ ] useRemediationSummary hook returns loading, error, and data states for remediation summary
- [ ] useRemediationByProduct hook returns loading, error, and data states for product-level breakdown
- [ ] useRemediationByProduct supports pagination parameters (offset, limit)
- [ ] Query keys are unique and include pagination parameters where applicable
- [ ] Hooks properly type their return values using the interfaces from Task 5

## Test Requirements
- [ ] Verify useRemediationSummary returns expected data shape when API responds successfully
- [ ] Verify useRemediationByProduct returns expected data shape with pagination
- [ ] Verify hooks handle API error responses gracefully (error state populated)
- [ ] Verify hooks show loading state while request is in flight

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 5 -- Add API client functions and TypeScript models for remediation endpoints
