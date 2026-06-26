## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and implement the API client function that calls the backend comparison endpoint. This establishes the data contract between frontend and backend.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` function

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Client function to call the backend comparison endpoint

## Implementation Notes
Follow the existing patterns in `src/api/models.ts` for interface definitions and `src/api/rest.ts` for API client functions.

In `src/api/models.ts`, add interfaces matching the backend response shape:
```typescript
export interface SbomComparison {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

In `src/api/rest.ts`, add the client function using the Axios instance from `src/api/client.ts`:
```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparison> =>
  client.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } })
    .then(response => response.data);
```

Follow the pattern of existing functions like `fetchSboms()` in `src/api/rest.ts`.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — pattern for API client function with Axios
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/models.ts` — existing interface definition patterns

## Acceptance Criteria
- [ ] `SbomComparison` and all child interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms()` function is exported from `src/api/rest.ts`
- [ ] Function correctly constructs the query parameters
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Type-check passes with `tsc --noEmit`

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npm run lint` — no linting errors

## Dependencies
- Depends on: Task 1 — Create feature branch

[sdlc-workflow] Description digest: sha256-md:3900226f9ce5367f2a904bf48317a5c78deca6209c9f108bda26b74042780ff1
