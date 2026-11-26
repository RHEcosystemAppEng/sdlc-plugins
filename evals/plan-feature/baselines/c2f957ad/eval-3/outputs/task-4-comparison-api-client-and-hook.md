# Task 4 — Add comparison API types, REST function and React Query hook

**Summary:** Add SBOM comparison API client, types and useSbomComparison hook
**Issue type:** Task | **Parent (Epic):** Epic B — TC-9003: Comparison UI and navigation
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend data layer for the new backend comparison endpoint: TypeScript types for the diff response, a typed REST function, a React Query hook, and MSW mocks/fixtures so the comparison page (Task 5) and its tests can be built against a stable contract. The auto-generated/typed client in `src/api/rest.ts` does not yet cover the new endpoint, so this is a manual REST integration.

## Files to Modify
- `src/api/models.ts` — add `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` interfaces
- `src/api/rest.ts` — add `fetchSbomComparison(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare` (success, 404 for unknown id)

## Files to Create
- `src/hooks/useSbomComparison.ts` — `useSbomComparison(left?: string, right?: string)` React Query hook, `enabled` only when both ids are set
- `tests/mocks/fixtures/sbom-comparison.json` — mock diff covering all six sections, including at least one `critical` new vulnerability and >0 items per section

## Implementation Notes
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW (trustify-backend Task 3, `modules/fundamental/src/sbom/endpoints/compare.rs`; model in `modules/fundamental/src/sbom/model/comparison.rs`). Query params: `left: string`, `right: string`. Response `200`:
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
    Errors: `400` missing/invalid params, `404` unknown SBOM id.
  - `GET /api/v2/sbom` — existing (`modules/fundamental/src/sbom/endpoints/list.rs`), returns `{ items: SbomSummary[], total: number }`; already wrapped by `fetchSboms()` / `useSboms` — reuse, do not duplicate.
  - Verify these contracts against the backend repo at implementation time using the implement-task cross-repo API verification step (backend is on branch `TC-9003`).
- Keep API field names snake_case in the interfaces (match the wire format, consistent with existing interfaces in `src/api/models.ts`); do not add a camelCase transform layer.
- Query key: `["sbom-comparison", left, right]`; follow `src/hooks/useSbomById.ts` for structure (query key, `enabled` guard on ids, error typing).
- Per CONVENTIONS.md §API layer: add the request to `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, types to `src/api/models.ts`, and the hook under `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `src/api/` + `src/hooks/` API-layer scope.
- Per CONVENTIONS.md §State management: server state via React Query `useQuery` only (no local caches/Redux), as in `src/hooks/useSbomById.ts`.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's React Query hook (`src/hooks/*.ts`) scope.
- Per CONVENTIONS.md §Naming: hook file and function in camelCase (`useSbomComparison.ts`), interfaces in PascalCase.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript (`.ts`/`.tsx`) naming scope.
- Per CONVENTIONS.md §Testing: mock the endpoint with MSW in `tests/mocks/handlers.ts` with fixtures under `tests/mocks/fixtures/`; unit-test with Vitest.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW/Vitest test scope.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `gh pr create --base TC-9003`; §5.1–5.4 scope and reuse; §5.6 trace data flow from fetch → hook → consumer.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (must be used for the new call)
- `src/api/rest.ts::fetchSboms` / `fetchSbomById`-style functions — pattern for typed REST functions
- `src/hooks/useSbomById.ts` — single-resource `useQuery` hook pattern with id-based `enabled`
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json` — existing MSW handler/fixture conventions

## Acceptance Criteria
- [ ] `SbomComparison` and item interfaces in `src/api/models.ts` match the backend contract field-for-field
- [ ] `fetchSbomComparison(left, right)` calls `GET /api/v2/sbom/compare?left=…&right=…` via the shared Axios client
- [ ] `useSbomComparison` does not fire a request unless both ids are provided
- [ ] `useSbomComparison` surfaces `404`/`400` as an error state (does not resolve to an empty diff)
- [ ] MSW handler and fixture exist and cover all six sections

## Test Requirements
- [ ] Vitest test: hook returns fixture data when both ids are set (MSW)
- [ ] Vitest test: hook is idle (no request) when one id is missing
- [ ] Vitest test: hook exposes an error when the MSW handler returns `404`

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
