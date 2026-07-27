## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces matching the backend comparison response shape, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task establishes the data-fetching foundation consumed by the comparison page UI (Task 5).

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces: SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseDiff
- `src/api/rest.ts` -- add compareSboms(leftId: string, rightId: string) function that calls GET /api/v2/sbom/compare

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping compareSboms() with query key ["sbom-comparison", leftId, rightId], enabled only when both IDs are provided

## Implementation Notes
Per CONVENTIONS.md API layer: follow the established pattern of typed API functions in `src/api/rest.ts` and React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms()` and `src/hooks/useSboms.ts` for the established pattern.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md React Query: use `useQuery` with a descriptive query key array. The hook should accept parameters for both SBOM IDs and only enable the query when both are non-null. See `src/hooks/useSbomById.ts` for the conditional query pattern.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```
  {
    "added_packages": [{ "name": string, "version": string, "license": string | null, "advisory_count": number }],
    "removed_packages": [{ "name": string, "version": string, "license": string | null, "advisory_count": number }],
    "version_changes": [{ "name": string, "left_version": string, "right_version": string, "direction": "upgrade" | "downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": string, "severity": string, "title": string, "affected_package": string }],
    "resolved_vulnerabilities": [{ "advisory_id": string, "severity": string, "title": string, "previously_affected_package": string }],
    "license_changes": [{ "name": string, "left_license": string, "right_license": string }]
  }
  ```
  (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend and `modules/fundamental/src/sbom/endpoints/compare.rs` for endpoint definition)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**TypeScript interface mapping:**
- Map Rust snake_case field names to the same snake_case in TypeScript since the API returns JSON with snake_case keys
- The `severity` field in VulnerabilityDiff uses lowercase strings ("critical", "high", "medium", "low") matching the existing SeverityBadge component's expected input

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API function pattern to follow for compareSboms()
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors, used by all API functions
- `src/hooks/useSbomById.ts` -- React Query hook pattern with conditional enable based on ID availability
- `src/api/models.ts` -- existing TypeScript interfaces for API types (SbomSummary, etc.)

## Acceptance Criteria
- [ ] TypeScript interfaces SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, and LicenseDiff are defined in models.ts
- [ ] compareSboms() function in rest.ts correctly calls GET /api/v2/sbom/compare with left and right query params
- [ ] useSbomComparison hook returns query state (data, isLoading, isError) from React Query
- [ ] Hook is disabled (does not fire request) when either SBOM ID is null or undefined
- [ ] Interface field names match the backend API response shape exactly

## Test Requirements
- [ ] Unit test: compareSboms() constructs the correct URL with query parameters
- [ ] Unit test: useSbomComparison hook fires request when both IDs are provided (using MSW mock handler)
- [ ] Unit test: useSbomComparison hook does not fire request when an ID is missing
- [ ] Unit test: response data is correctly typed and accessible via the hook

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison endpoint (backend API contract dependency)
