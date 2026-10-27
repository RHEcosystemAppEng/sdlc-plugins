## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and an API client function to call the backend comparison endpoint. Also add a React Query hook for data fetching. This is the API-layer foundation that the comparison page component will consume.

## Files to Modify
- `src/api/models.ts` — add SbomComparison, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange interfaces
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
Follow the existing API layer pattern:
- TypeScript interfaces in `src/api/models.ts` following existing types like SbomSummary, AdvisoryDetails
- API client function in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, following the pattern of `fetchSboms()` and `fetchAdvisories()`
- React Query hook in `src/hooks/` following `src/hooks/useSboms.ts` pattern with `useQuery`

**Backend API contract:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

The React Query hook should:
- Accept `leftId` and `rightId` parameters
- Only enable the query when both IDs are provided
- Use a query key like `["sbom-comparison", leftId, rightId]`

Per CONVENTIONS.md §API Layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript source file scope.

Per CONVENTIONS.md §State Management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook file scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function demonstrating the Axios call pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — existing React Query hook demonstrating useQuery pattern
- `src/hooks/useSbomById.ts` — existing React Query hook for single-entity fetch

## Acceptance Criteria
- [ ] `SbomComparison` TypeScript interface matches the backend response shape
- [ ] `compareSboms(leftId, rightId)` function makes GET request to `/api/v2/sbom/compare`
- [ ] `useSbomComparison` hook returns query result with loading, error, and data states
- [ ] Hook is disabled when either SBOM ID is not provided

## Test Requirements
- [ ] TypeScript compilation passes with new interfaces and function
- [ ] Hook can be imported and used in a test component

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Backend comparison endpoint
