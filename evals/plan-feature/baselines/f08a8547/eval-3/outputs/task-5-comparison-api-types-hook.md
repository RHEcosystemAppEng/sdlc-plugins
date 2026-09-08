## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, a client function to call the comparison endpoint, and a React Query hook for data fetching. This provides the data layer for the comparison page UI (Task 6).

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add compareSboms() API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Add the following TypeScript interfaces to `src/api/models.ts`:
  ```typescript
  interface PackageDiff {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  interface VulnerabilityDiff {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }

  interface SbomComparisonResult {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseChange[];
  }
  ```
- Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` to `src/api/rest.ts` following the pattern of existing API functions (e.g., `fetchSboms()`). Use the Axios instance from `src/api/client.ts`.
- Create the React Query hook following the pattern in `src/hooks/useSbomById.ts`: accept leftId and rightId parameters, return useQuery result, enable only when both IDs are provided.
- Per CONVENTIONS.md: use React Query (TanStack Query) for server state management, not manual fetch or Redux. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.
- Per CONVENTIONS.md: API functions go in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer file scope.
- Per CONVENTIONS.md: use camelCase naming for hooks and utility functions. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's naming scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with fields: added_packages (PackageDiff[]), removed_packages (PackageDiff[]), version_changes (VersionChange[]), new_vulnerabilities (VulnerabilityDiff[]), resolved_vulnerabilities (VulnerabilityDiff[]), license_changes (LicenseChange[]) (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Relevant constraints from docs/constraints.md:**
- Commit rules (section 2): every commit must reference TC-9003, follow Conventional Commits, include AI attribution trailer
- PR rules (section 3): branch named after Jira issue ID, PR link posted to Jira task
- Code change rules (section 5): changes scoped to listed files, inspect code before modifying, follow referenced patterns, no duplication

## Reuse Candidates
- `src/hooks/useSbomById.ts` — existing React Query hook for single SBOM fetch, reference for hook structure and query key patterns
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list, reference for query configuration
- `src/api/rest.ts::fetchSboms` — existing API function, reference for Axios call pattern and response typing
- `src/api/client.ts` — Axios instance with base URL and auth interceptors, used by all API functions

## Acceptance Criteria
- [ ] SbomComparisonResult and related interfaces are exported from src/api/models.ts
- [ ] compareSboms() function is exported from src/api/rest.ts and calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison hook accepts leftId and rightId parameters
- [ ] useSbomComparison hook returns React Query result with typed SbomComparisonResult data
- [ ] useSbomComparison hook is disabled (enabled: false) when either ID is missing
- [ ] compareSboms() uses the shared Axios instance from client.ts

## Test Requirements
- [ ] Unit test: compareSboms() constructs correct URL with query parameters
- [ ] Unit test: useSbomComparison returns loading state initially
- [ ] Unit test: useSbomComparison returns data on successful API response (MSW mock)
- [ ] Unit test: useSbomComparison is disabled when leftId is undefined
- [ ] Unit test: useSbomComparison is disabled when rightId is undefined

## Dependencies
- Depends on: Task 4 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 3 — Add SBOM comparison REST endpoint (cross-repo: backend API contract must be finalized)
