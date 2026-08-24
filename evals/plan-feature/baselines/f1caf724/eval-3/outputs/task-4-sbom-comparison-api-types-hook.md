## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, add the API client function to call the comparison endpoint, and create a React Query hook for the comparison data. This task establishes the frontend data layer for the comparison feature.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types (SbomComparisonResult, PackageDiffEntry, VersionChangeEntry, VulnerabilityDiffEntry, LicenseChangeEntry)
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Per CONVENTIONS.md §API Layer: add the API function to `src/api/rest.ts` following the existing pattern (e.g., `fetchSboms()`), and create the hook in `src/hooks/` following the existing hook pattern (e.g., `useSbomById.ts`).
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript source file scope.
- Per CONVENTIONS.md §Naming: use camelCase for the hook (`useSbomComparison`) and API function (`compareSboms`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript source file scope.
- The hook should accept `leftId` and `rightId` as parameters and return a `useQuery` result with `enabled: !!(leftId && rightId)` to prevent fetching when IDs are not yet selected.
- TypeScript interfaces must match the backend response shape:
  - `SbomComparisonResult` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
  - `PackageDiffEntry`: `{ name: string; version: string; license: string; advisory_count: number }`
  - `VersionChangeEntry`: `{ name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }`
  - `VulnerabilityDiffEntry`: `{ advisory_id: string; severity: string; title: string; affected_package: string }`
  - `LicenseChangeEntry`: `{ name: string; left_license: string; right_license: string }`

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `{ added_packages: PackageDiffEntry[], removed_packages: PackageDiffEntry[], version_changes: VersionChangeEntry[], new_vulnerabilities: VulnerabilityDiffEntry[], resolved_vulnerabilities: VulnerabilityDiffEntry[], license_changes: LicenseChangeEntry[] }` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern, follow same Axios call structure
- `src/hooks/useSbomById.ts` — existing React Query hook pattern for single-entity fetch
- `src/api/models.ts` — existing TypeScript interfaces for API response types, follow naming and export patterns

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function added to `src/api/rest.ts`
- [ ] `useSbomComparison` hook created in `src/hooks/useSbomComparison.ts` with proper `enabled` guard
- [ ] Hook returns typed `SbomComparisonResult` data

## Test Requirements
- [ ] Unit test for `useSbomComparison` hook with MSW mock handler returning comparison data
- [ ] Test that hook does not fetch when IDs are not provided (enabled guard)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint with integration tests
