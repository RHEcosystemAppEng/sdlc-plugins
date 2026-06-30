## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and implement the API client function and React Query hook. This task builds the data-fetching layer that the comparison page will consume. The types must match the backend response contract defined in the feature specification.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId, rightId)` that calls `compareSboms` and returns query result

## Implementation Notes
For `src/api/models.ts`, add interfaces matching the backend JSON contract:

```typescript
interface SbomComparison {
  added_packages: PackageDiff[];
  removed_packages: PackageDiff[];
  version_changes: VersionChange[];
  new_vulnerabilities: VulnerabilityDiff[];
  resolved_vulnerabilities: VulnerabilityDiff[];
  license_changes: LicenseChange[];
}
```

For `src/api/rest.ts`, follow the pattern of existing API functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`:

```typescript
export const compareSboms = (leftId: string, rightId: string): Promise<SbomComparison> =>
  axios.get('/api/v2/sbom/compare', { params: { left: leftId, right: rightId } }).then(r => r.data);
```

For `src/hooks/useSbomComparison.ts`, follow the hook pattern in `src/hooks/useSbomById.ts`:
- Use `useQuery` with a query key like `['sbom-comparison', leftId, rightId]`
- Enable the query only when both `leftId` and `rightId` are defined
- Return the standard `UseQueryResult<SbomComparison>`

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `src/api/` directory scope.

Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `src/hooks/` directory scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook naming scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for API client function pattern with Axios
- `src/hooks/useSbomById.ts` — reference for single-resource React Query hook pattern
- `src/hooks/useSboms.ts` — reference for list-fetching hook pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `SbomComparison` and supporting interfaces are defined in `src/api/models.ts`
- [ ] `compareSboms()` function is exported from `src/api/rest.ts`
- [ ] `useSbomComparison` hook is implemented in `src/hooks/useSbomComparison.ts`
- [ ] Hook is only enabled when both SBOM IDs are provided
- [ ] TypeScript compiles without errors: `npx tsc --noEmit`

## Test Requirements
- [ ] Verify TypeScript interfaces match the backend response contract
- [ ] Verify `useSbomComparison` hook query key includes both SBOM IDs for correct cache behavior

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- useSbomComparison` — hook tests pass

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 4 — backend-comparison-endpoint

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:feba9ae9511479eb1a35f110d5feabac110133f7dcd1226394067075f2639d10
