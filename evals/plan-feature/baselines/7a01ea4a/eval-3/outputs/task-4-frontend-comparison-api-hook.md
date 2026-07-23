## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook for fetching comparison data. This establishes the data-fetching layer that the comparison page UI (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for comparison response types: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` -- add fetchSbomComparison(leftId: string, rightId: string) function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping fetchSbomComparison with query key ["sbom-comparison", leftId, rightId]; query is enabled only when both IDs are provided

## Implementation Notes
- TypeScript interfaces must exactly match the backend response shape defined in the Figma design context:
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
- Follow the existing API client function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`). Use the Axios instance from `src/api/client.ts`.
- Follow the existing React Query hook pattern from `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with a descriptive query key.
- The hook should accept `leftId` and `rightId` as parameters and set `enabled: !!(leftId && rightId)` to prevent firing when IDs are not yet selected.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape: `SbomComparisonResult` with six diff category arrays (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API client function; follow its pattern for Axios usage and return type
- `src/api/rest.ts::fetchAdvisories` -- another API client function pattern reference
- `src/hooks/useSboms.ts` -- existing React Query hook; follow its useQuery configuration pattern
- `src/hooks/useSbomById.ts` -- existing detail-level React Query hook; reference for single-resource queries
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces for all six diff categories are defined in models.ts
- [ ] fetchSbomComparison() function calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison hook returns comparison data via React Query
- [ ] Hook is disabled (does not fire) when either leftId or rightId is missing
- [ ] All types are properly exported for use by the comparison page

## Test Requirements
- [ ] Unit test: useSbomComparison hook fetches data when both IDs are provided
- [ ] Unit test: useSbomComparison hook does not fetch when leftId is missing
- [ ] Unit test: useSbomComparison hook does not fetch when rightId is missing
- [ ] Unit test: fetchSbomComparison constructs the correct URL with query parameters

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
