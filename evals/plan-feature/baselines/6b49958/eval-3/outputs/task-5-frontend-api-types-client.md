## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This provides the data layer that the comparison UI page will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `fetchSbomComparison(leftId, rightId)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Add the following TypeScript interfaces to `src/api/models.ts`, matching the backend response shape:
  - `PackageDiff` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`
  - `SbomComparisonResult` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
- Follow the existing API client pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts`. Example: `fetchSboms()` for the function signature and return type pattern.
- The `fetchSbomComparison` function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` and return `SbomComparisonResult`.
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` for the `useSbomComparison` hook. The hook should accept `leftId` and `rightId` parameters and use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The query should be disabled when either ID is undefined.
- The `resolved_vulnerabilities` diff type uses `previously_affected_package` instead of `affected_package` — define a separate `ResolvedVulnerabilityDiff` interface or use a union type.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six arrays (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes). See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern to follow for `fetchSbomComparison`
- `src/api/models.ts` — existing TypeScript interface definitions to follow for new comparison types
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for `useSbomComparison`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (reuse, do not create a new client)

## Acceptance Criteria
- [ ] TypeScript interfaces for `SbomComparisonResult` and all sub-types are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook is disabled when either SBOM ID is undefined
- [ ] All types match the backend response contract

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verifies it calls the correct API endpoint with given IDs
- [ ] Unit test for `useSbomComparison` hook: verifies query is disabled when an ID is undefined
- [ ] Mock handler added to `tests/mocks/handlers.ts` for the comparison endpoint

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 4 — Add SBOM comparison endpoint (trustify-backend) — API contract must be finalized

[sdlc-workflow] Description digest: sha256:200dbbe38a63f7caaf14f1ff24bd7a994731c96053ab840775e128a59a2eb847
