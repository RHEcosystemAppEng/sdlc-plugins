## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook for data fetching. This task establishes the frontend data layer needed by the comparison page component.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces for comparison response types: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` -- Add fetchSbomComparison(leftId: string, rightId: string) API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping fetchSbomComparison with query key management and enabled flag (disabled until both SBOM IDs are provided)

## Implementation Notes
- Add interfaces to `src/api/models.ts` following the existing pattern for SBOM and advisory response types. The response shape matches the backend API contract:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
- Add the API client function to `src/api/rest.ts` using the Axios instance from `src/api/client.ts`. Follow the pattern of existing functions like `fetchSboms()`.
- The React Query hook should follow the pattern in `src/hooks/useSbomById.ts`: accept left and right SBOM IDs, use `useQuery` with an appropriate query key (e.g., `["sbom-comparison", leftId, rightId]`), and set `enabled: !!(leftId && rightId)` to prevent fetching until both IDs are provided.
- Per CONVENTIONS.md: use camelCase for hooks and utility functions (e.g., `useSbomComparison`, `fetchSbomComparison`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook scope.
- Per CONVENTIONS.md: use the Axios client in `src/api/client.ts` for all API calls -- do not create a separate HTTP client.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape: `SbomComparisonResult` with six array fields (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes). See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend.
- `GET /api/v2/sbom` -- existing endpoint used for SBOM list in selectors; response shape: `PaginatedResults<SbomSummary>`. See `modules/fundamental/src/sbom/endpoints/list.rs` in trustify-backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API client function; follow the same Axios call pattern for the comparison endpoint
- `src/hooks/useSbomById.ts` -- existing React Query hook; follow the same useQuery pattern with query key and options
- `src/hooks/useSboms.ts` -- existing SBOM list hook; reference for query key naming convention
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import and use for the comparison request

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories are defined in models.ts matching the backend API response shape
- [ ] fetchSbomComparison() function is exported from rest.ts and correctly calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison hook is exported and returns useQuery result with loading/error/data states
- [ ] Hook is disabled (does not fetch) when either SBOM ID is null/undefined

## Test Requirements
- [ ] Unit test: useSbomComparison hook calls the correct API endpoint with left and right params
- [ ] Unit test: useSbomComparison hook does not fetch when either ID is missing (enabled: false)
- [ ] Unit test: fetchSbomComparison correctly constructs the API URL with query parameters

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests
