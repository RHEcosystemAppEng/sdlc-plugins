## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for SBOM comparison (TC-9003): TypeScript types for the comparison response, a REST client function that calls the new backend endpoint `GET /api/v2/sbom/compare`, a React Query hook, and MSW mocks/fixtures so page-level tests (Tasks 4–6) can run without the backend. The auto-generated/typed client in `src/api/rest.ts` does not cover this endpoint yet, so it is added manually.

## Files to Modify
- `src/api/models.ts` — add `SbomComparison`, `PackageDiffEntry`, `VersionChangeEntry`, `VersionDirection`, `NewVulnerabilityEntry`, `ResolvedVulnerabilityEntry`, `LicenseChangeEntry` interfaces
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId?: string, rightId?: string)`
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response covering every diff category, including at least one `critical` new vulnerability and >100 added packages for virtualization tests

## Implementation Notes
- **Backend API contracts** (from trustify-backend Tasks 1–2):
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — query params `left: string`, `right: string` (SBOM IDs as returned by `GET /api/v2/sbom`). Response 200:
    ```ts
    interface SbomComparison {
      added_packages: { name: string; version: string; license: string; advisory_count: number }[];
      removed_packages: { name: string; version: string; license: string; advisory_count: number }[];
      version_changes: { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }[];
      new_vulnerabilities: { advisory_id: string; severity: string; title: string; affected_package: string }[];
      resolved_vulnerabilities: { advisory_id: string; severity: string; title: string; previously_affected_package: string }[];
      license_changes: { name: string; left_license: string; right_license: string }[];
    }
    ```
    Errors: 400 (missing param), 404 (unknown SBOM). Defined in trustify-backend `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/compare.rs`.
  - `GET /api/v2/sbom` — existing list endpoint (`modules/fundamental/src/sbom/endpoints/list.rs`), already wrapped by `fetchSboms()` in `src/api/rest.ts` and `src/hooks/useSboms.ts`; used by the selectors in Task 4.
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- Keep wire field names snake_case in `models.ts` to match the backend (consistent with how existing interfaces in `src/api/models.ts` mirror the API).
- Implement `compareSboms` using the shared Axios instance from `src/api/client.ts` with `params: { left, right }` (do not build the query string manually), following the style of `fetchSboms()` in `src/api/rest.ts`.
- `useSbomComparison` follows `src/hooks/useSbomById.ts`: `useQuery({ queryKey: ["sbom-compare", leftId, rightId], queryFn: () => compareSboms(leftId!, rightId!), enabled: !!leftId && !!rightId })`. Do not retry on 404 (`retry: (count, err) => err.response?.status !== 404 && count < 3`) so a missing SBOM surfaces immediately as an error state.
- **Fail-closed:** the hook must expose errors (`isError`, `error`) — never coerce a failed request into an empty `SbomComparison`, because the UI would then render "no changes" for a comparison that never ran.
- **Per CONVENTIONS.md §API layer:** add the typed function to `src/api/rest.ts`, types to `src/api/models.ts`, and the React Query hook to `src/hooks/`; see `src/hooks/useSbomById.ts` as the example.
  Applies: task modifies src/api/rest.ts matching the convention's TypeScript API-layer (`src/api/`, `src/hooks/`) scope.
- **Per CONVENTIONS.md §Naming:** hook file and function use camelCase (`useSbomComparison.ts`).
  Applies: task modifies src/hooks/useSbomComparison.ts matching the convention's TypeScript hooks/utilities naming scope.
- **Per CONVENTIONS.md §Testing:** API mocking uses MSW handlers in `tests/mocks/handlers.ts` with JSON fixtures in `tests/mocks/fixtures/` (see `tests/mocks/fixtures/sboms.json`).
  Applies: task modifies tests/mocks/handlers.ts matching the convention's Vitest/MSW `.ts` test scope.
- **Constraints (docs/constraints.md):** §2 commits (Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer); §3 PRs (`--base main`, PR link on Jira task); §5 code changes (scoped files, inspect first, reuse `client.ts`, sibling parity with `useSbomById.ts`); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; must be reused
- `src/api/rest.ts::fetchSboms` — pattern for typed API functions
- `src/hooks/useSbomById.ts` — pattern for a parameterized `useQuery` hook with `enabled` guard
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json` — existing MSW setup; reuse SBOM IDs from `sboms.json` in the comparison fixture

## Acceptance Criteria
- [ ] `SbomComparison` and entry interfaces in `src/api/models.ts` match the backend response field names exactly
- [ ] `compareSboms(left, right)` issues `GET /api/v2/sbom/compare?left=...&right=...` through `src/api/client.ts`
- [ ] `useSbomComparison` does not fire a request until both IDs are provided
- [ ] A 404/400/5xx response surfaces as an error from the hook, not as an empty comparison
- [ ] MSW handler and fixture exist and return data for every diff category

## Test Requirements
- [ ] Unit test: `compareSboms` calls the correct URL with `left`/`right` params (MSW)
- [ ] Hook test: `useSbomComparison(undefined, "b")` does not issue a request
- [ ] Hook test: successful response is returned as typed data
- [ ] Hook test: MSW returning 404 yields `isError === true` and no data (fail-closed path)

## Verification Commands
- `npx vitest run src/hooks` — hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/compare endpoint (trustify-backend) — the response contract must be merged before this client is merged
