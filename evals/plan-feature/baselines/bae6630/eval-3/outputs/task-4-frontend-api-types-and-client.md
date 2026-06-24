# Task 4 — Frontend API types and client function for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and a client function that calls the new `GET /api/v2/sbom/compare` endpoint. This provides the typed API layer that hooks and page components will consume.

## Files to Modify
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` via the Axios client

## Files to Create
- `src/api/models/sbom-comparison.ts` — Define TypeScript interfaces matching the backend response: `SbomComparison` (top-level with arrays for each diff category), `AddedPackage` (name, version, license, advisoryCount), `RemovedPackage` (same fields), `VersionChange` (name, leftVersion, rightVersion, direction), `NewVulnerability` (advisoryId, severity, title, affectedPackage), `ResolvedVulnerability` (advisoryId, severity, title, previouslyAffectedPackage), `LicenseChange` (name, leftLicense, rightLicense)

## Implementation Notes
- Follow the existing pattern in `src/api/models.ts` for interface definitions. The new file is placed in `src/api/models/` to keep comparison types organized separately from the main models file.
- Use camelCase for TypeScript field names (the Axios client or a response transformer handles snake_case to camelCase conversion if needed).
- The `fetchSbomComparison` function should follow the same pattern as existing functions in `src/api/rest.ts` (e.g., `fetchSboms()`), using the shared Axios instance from `src/api/client.ts`.
- The `direction` field in `VersionChange` should be typed as `"upgrade" | "downgrade"` string literal union.
- The `severity` field in vulnerability types should match the existing severity type used by `SeverityBadge` in `src/components/SeverityBadge.tsx`.

## Acceptance Criteria
- [ ] `SbomComparison` interface defined with all six diff category arrays
- [ ] All sub-interfaces (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined and exported
- [ ] `fetchSbomComparison` function is exported from `src/api/rest.ts`
- [ ] Function correctly constructs the URL with `left` and `right` query parameters
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Type-check passes with `tsc --noEmit`
- [ ] Verify `fetchSbomComparison` constructs correct URL (unit test or manual verification)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 3 — Backend comparison endpoint and integration tests

## Digest
[sdlc-workflow] Description digest: sha256-md:6385eae4474306591fa7ebd54147cc3353341ff0b258a902e70ca3ba1a5d60a5
