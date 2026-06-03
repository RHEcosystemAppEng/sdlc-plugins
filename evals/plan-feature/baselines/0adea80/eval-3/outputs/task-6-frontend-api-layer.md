# Task 6 — Add frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer that the comparison page component (Task 7) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` when both IDs are defined

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — add interfaces matching the backend response shape with snake_case field names (TypeScript convention in this codebase follows the API response naming).
- Follow the existing API client function pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts` to call `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}`.
- Follow the existing React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` with a descriptive query key like `["sbom-comparison", leftId, rightId]`.
- The hook should be disabled (`enabled: false` or conditional) when either `leftId` or `rightId` is undefined, to prevent calls before both SBOMs are selected.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
    ```json
    {
      "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
      "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
      "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
      "new_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "affected_package": "string" }],
      "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
      "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
    }
    ```
  - Defined in backend at `modules/fundamental/src/sbom/endpoints/compare.rs`
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — Existing TypeScript interfaces for API response types; follow the same pattern
- `src/api/rest.ts` — Existing API client functions (e.g., `fetchSboms()`) using the Axios instance
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — React Query hook pattern for list endpoints
- `src/hooks/useSbomById.ts` — React Query hook pattern for detail endpoints with ID parameter

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend API response shape exactly
- [ ] API client function correctly constructs the URL with left/right query parameters
- [ ] React Query hook returns comparison data when both IDs are provided
- [ ] React Query hook does not fire when either ID is undefined
- [ ] No TypeScript compilation errors

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided (using MSW mock)
- [ ] Unit test: `useSbomComparison` hook does not fetch when either ID is undefined
- [ ] Unit test: `fetchSbomComparison` constructs the correct URL with query parameters

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
