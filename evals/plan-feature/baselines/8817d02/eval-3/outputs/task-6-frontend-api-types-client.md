# Task 6 — Add SBOM comparison API types and client function

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and a client function to call the new comparison endpoint. This provides the typed API layer that the React Query hook and page components will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` client function

## Implementation Notes
- Follow the existing type definition pattern in `src/api/models.ts` — interfaces use PascalCase names and camelCase property names.
- Follow the existing API client function pattern in `src/api/rest.ts` — functions use the Axios instance from `src/api/client.ts` with typed return values.
- The response shape matches the backend API contract:
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
- Note: the backend uses snake_case field names. Check whether the existing Axios client has a response transformer that converts to camelCase. If not, keep field names as snake_case in the TypeScript interfaces to match the API response.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with six array fields (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — Existing interfaces (follow the same naming and typing patterns)
- `src/api/rest.ts` — Existing API functions like `fetchSboms()` (follow the same Axios call pattern)
- `src/api/client.ts` — Reuse the configured Axios instance

## Acceptance Criteria
- [ ] All TypeScript interfaces are defined and exported from `src/api/models.ts`
- [ ] `compareSboms` function is defined and exported from `src/api/rest.ts`
- [ ] Function calls `GET /api/v2/sbom/compare` with left and right query parameters
- [ ] Function returns typed `SbomComparisonResult`
- [ ] TypeScript compilation passes with no type errors

## Test Requirements
- [ ] Type-level test: verify the interfaces match the expected API response shape (TypeScript compilation is the test)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint

sha256-md:6661362eacb2242a63072c147131a23a922a1432813f16c5a977021da61f2215
