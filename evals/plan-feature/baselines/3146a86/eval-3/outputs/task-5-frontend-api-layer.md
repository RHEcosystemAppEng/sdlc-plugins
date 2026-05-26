# Task 5 — Add frontend API layer for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces, API client function, and React Query hook needed to call the new SBOM comparison endpoint from the frontend. This establishes the data layer that the comparison page components will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Per the frontend key conventions (API layer): typed API functions go in `src/api/rest.ts`, and React Query hooks go in `src/hooks/`. Follow the pattern of existing functions like `fetchSboms()` in `rest.ts` and `useSboms.ts` in `hooks/`.
- Per the frontend key conventions (State management): use React Query (TanStack Query) for server state. The comparison hook should use `useQuery` with a query key that includes both SBOM IDs so results are cached per comparison pair.
- The hook should accept `leftId` and `rightId` as parameters and only enable the query when both are non-empty (use the `enabled` option).
- Per the frontend key conventions (Naming): camelCase for hooks and utilities.

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  interface AddedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface RemovedPackage { name: string; version: string; license: string; advisory_count: number; }
  interface VersionChange { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
  interface NewVulnerability { advisory_id: string; severity: string; title: string; affected_package: string; }
  interface ResolvedVulnerability { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
  interface LicenseChange { name: string; left_license: string; right_license: string; }
  ```
  (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — follow the same Axios GET pattern for the new `compareSboms` function
- `src/api/client.ts` — reuse the existing Axios instance with base URL and auth interceptors
- `src/hooks/useSboms.ts` — follow the same `useQuery` pattern for the new `useSbomComparison` hook
- `src/hooks/useSbomById.ts` — reference for a hook that takes an ID parameter with enabled/disabled logic
- `src/api/models.ts` — follow the existing interface naming and export patterns

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `models.ts`
- [ ] `compareSboms(leftId, rightId)` function is implemented in `rest.ts` using the Axios client
- [ ] `useSbomComparison` hook wraps the API call with React Query, keyed by both SBOM IDs
- [ ] The hook only fires the query when both IDs are provided (uses `enabled` option)

## Test Requirements
- [ ] Unit test: `compareSboms` function calls the correct endpoint with correct query parameters
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided and the API responds successfully
- [ ] Unit test: `useSbomComparison` hook does not fire when either ID is missing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison endpoint (backend must define the API contract)
