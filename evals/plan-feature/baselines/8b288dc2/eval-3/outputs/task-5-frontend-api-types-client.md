## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response types and a client function to call the comparison endpoint. This provides the typed API layer that the comparison hook and page components will consume.

## Files to Modify
- `src/api/models.ts` — add comparison-related TypeScript interfaces
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Implementation Notes
- Add the following interfaces to `src/api/models.ts`, matching the backend response shape:
  - `PackageDiff` — fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange` — fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff` — fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `LicenseChange` — fields: `name: string`, `left_license: string`, `right_license: string`
  - `SbomComparisonResult` — fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
- Add `compareSboms` function to `src/api/rest.ts` following the existing API function pattern (e.g., `fetchSboms()`):
  - Use the Axios instance from `src/api/client.ts`
  - Call `GET /api/v2/sbom/compare?left=${leftId}&right=${rightId}`
  - Return typed `SbomComparisonResult`
- Follow camelCase naming for function names and PascalCase for interface names per project conventions.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six array fields (see interfaces above). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` (backend repo).

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces demonstrating naming and typing patterns for API response types
- `src/api/rest.ts::fetchSboms` — existing API client function showing Axios usage pattern with typed responses
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `SbomComparisonResult` and related interfaces are defined in `models.ts`
- [ ] `compareSboms` function is added to `rest.ts` and makes a GET request to the comparison endpoint
- [ ] Function returns typed `SbomComparisonResult`
- [ ] Interfaces match the backend response shape exactly

## Test Requirements
- [ ] Type-check passes with `tsc --noEmit`
- [ ] Unit test: `compareSboms` calls the correct endpoint URL with query parameters

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison endpoint and integration tests

## Description Digest
sha256-md:c78223dd892b6ae703069daddad6fc7b6a512b6b388033f1126f63fa3b6b4f69
