## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and the API client function to call the comparison endpoint. This task establishes the data contract between the frontend and the new backend endpoint without introducing any UI components.

## Files to Modify
- `src/api/models.ts` -- Add `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseChange` interfaces matching the backend response shape
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` function using the Axios client

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook `useSbomComparison(leftId?: string, rightId?: string)` that calls `fetchSbomComparison` and is enabled only when both IDs are provided

## Implementation Notes
- Follow the existing API layer pattern: interfaces in `src/api/models.ts`, client functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
- The `fetchSbomComparison` function should call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` using the Axios instance from `src/api/client.ts`.
- The `useSbomComparison` hook should follow the pattern in `src/hooks/useSbomById.ts`: use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]` and set `enabled: !!leftId && !!rightId`.
- TypeScript interfaces must match the backend JSON shape exactly:
  - `added_packages: PackageDiff[]`
  - `removed_packages: PackageDiff[]`
  - `version_changes: VersionChange[]`
  - `new_vulnerabilities: VulnerabilityDiff[]`
  - `resolved_vulnerabilities: VulnerabilityDiff[]`
  - `license_changes: LicenseChange[]`

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import and use for the comparison API call
- `src/api/rest.ts::fetchSboms` -- Pattern for API client functions; follow the same style
- `src/hooks/useSbomById.ts` -- Pattern for React Query hooks with ID parameters; follow the same `useQuery` configuration

## Acceptance Criteria
- [ ] `SbomComparison` interface and sub-types are exported from `src/api/models.ts`
- [ ] `fetchSbomComparison()` calls the correct endpoint with query parameters
- [ ] `useSbomComparison()` hook returns query result and is disabled when IDs are missing
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook: verify it calls the correct endpoint and handles loading/error/success states

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- SBOM comparison REST endpoint (defines the API contract)

[sdlc-workflow] Description digest: sha256-md:3a6d8e5c72bb3e89153f367bab6146deb06311287164b10b8644aa155324c824
