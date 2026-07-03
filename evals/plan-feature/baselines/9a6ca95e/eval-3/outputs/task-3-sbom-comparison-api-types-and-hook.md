## Repository

trustify-ui

## Target Branch

main

## Priority

Critical

## Fix Versions

RHTPA 1.5.0

## Description

Add the TypeScript types, API client function, and React Query hook for the SBOM comparison endpoint. This task defines the frontend data model matching the backend `SbomComparisonResult` response shape, adds a `compareSboms(leftId, rightId)` function to the API client, and creates a `useSbomComparison` React Query hook that the comparison page will consume. The hook accepts left and right SBOM IDs and is enabled only when both IDs are provided.

## Acceptance Criteria

- [ ] TypeScript interfaces exist for `SbomComparisonResult`, `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, and `LicenseChangeEntry` matching the backend response shape
- [ ] `compareSboms(leftId: string, rightId: string)` function exists in the API client and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomComparison(leftId?: string, rightId?: string)` React Query hook exists, returns `UseQueryResult<SbomComparisonResult>`, and is disabled (enabled: false) when either ID is undefined
- [ ] The hook uses a query key that includes both SBOM IDs for proper cache invalidation
- [ ] All types are exported from the models file for use by page components

## Test Requirements

- [ ] Unit test: `compareSboms` calls the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` is disabled when either ID is missing
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (using MSW mock)

## Dependencies

- Task 2 (sbom-comparison-endpoint) -- defines the API contract this task implements against

## Files to Modify

- `src/api/models.ts` -- add comparison result TypeScript interfaces
- `src/api/rest.ts` -- add `compareSboms()` API client function

## Files to Create

- `src/hooks/useSbomComparison.ts` -- React Query hook for SBOM comparison

## Implementation Notes

- Follow the existing type definition patterns in `src/api/models.ts` for interface naming and field conventions.
- Follow the API client function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`, `fetchAdvisories()`) for the `compareSboms` function, using the Axios instance from `src/api/client.ts`.
- Follow the React Query hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` for the `useSbomComparison` hook structure, including query key naming and enabled flag.
- Add MSW mock handler for the comparison endpoint in `tests/mocks/handlers.ts` for testing.
- Add mock comparison fixture data in `tests/mocks/fixtures/` for the MSW handler.

## Conventions

- **API layer**: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` and creates `src/hooks/useSbomComparison.ts` matching the convention's API layer scope.
- **Naming**: camelCase for hooks and utilities. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's naming scope.
