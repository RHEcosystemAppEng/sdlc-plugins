## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and an Axios client function to call the comparison endpoint. These types and client function form the API layer that React Query hooks (task 8) and the comparison page (task 9) will consume.

## Files to Modify
- `src/api/models.ts` — Add comparison response type interfaces
- `src/api/rest.ts` — Add `compareSboms()` API client function

## Implementation Notes
In `src/api/models.ts`, add interfaces matching the backend response shape:
- `SbomComparison` — top-level type with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` — nested types

In `src/api/rest.ts`, add a function following the pattern of existing API functions (e.g., `fetchSboms()`):
```
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparison> =>
  client.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } }).then(r => r.data);
```

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` and `src/api/models.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §Naming: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API function pattern using the Axios client
- `src/api/models.ts` — reference for existing interface naming conventions and structure
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (imported by rest.ts)

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint (defines the API contract this task implements client-side)

## Acceptance Criteria
- [ ] `SbomComparison` and all nested interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms(leftId, rightId)` function is exported from `src/api/rest.ts`
- [ ] Function uses the existing Axios client instance from `src/api/client.ts`
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Type-check passes: `SbomComparison` interface matches the expected API response shape
- [ ] Unit test: `compareSboms` calls the correct endpoint with left and right query params
