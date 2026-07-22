## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response, implement the API client function to call the comparison endpoint, and create a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that calls the comparison endpoint

## Implementation Notes
For the TypeScript interfaces in `src/api/models.ts`, match the backend response shape:
- `SbomComparisonResult` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
- `PackageDiff` with fields: `name: string`, `version: string`, `license: string`, `advisory_count: number`
- `VersionChange` with fields: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
- `VulnerabilityDiff` with fields: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
- `LicenseChange` with fields: `name: string`, `left_license: string`, `right_license: string`

For the API client function in `src/api/rest.ts`, follow the pattern of existing functions like `fetchSboms()`. Use the Axios client from `src/api/client.ts` and call `GET /api/v2/sbom/compare` with `left` and `right` as query parameters.

For the React Query hook in `src/hooks/useSbomComparison.ts`, follow the pattern in `src/hooks/useSbomById.ts`. The hook should accept `leftId` and `rightId` parameters, and only enable the query when both IDs are provided. Use a query key like `["sbom-comparison", leftId, rightId]`.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Pattern for API client functions using Axios
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` — Pattern for React Query hooks with parameter-based enabling
- `src/hooks/useSboms.ts` — Pattern for React Query hooks

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface exists in `src/api/models.ts` with all six diff category fields
- [ ] `fetchSbomComparison()` function exists in `src/api/rest.ts` and calls the correct endpoint
- [ ] `useSbomComparison` hook exists and returns `{ data, isLoading, isError }` from React Query
- [ ] Hook is disabled (does not fetch) when either SBOM ID is undefined
- [ ] TypeScript interfaces match the backend response JSON shape

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns loading state initially
- [ ] Unit test: `useSbomComparison` hook returns data after successful fetch (using MSW mock)
- [ ] Unit test: hook does not fire query when leftId or rightId is undefined

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 3 — Backend SBOM comparison endpoint and integration tests
