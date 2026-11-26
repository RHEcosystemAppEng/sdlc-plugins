# Task 6 — Add remediation API models, REST functions and React Query hooks

**Parent Epic:** TC-9006: trustify-ui (<EPIC-UI>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the frontend data layer for the remediation dashboard (TC-9006). This covers TypeScript response models, typed REST functions, and React Query hooks for the three new backend endpoints, plus MSW mock handlers and fixtures so the dashboard UI tasks (7, 8) can be built and tested. These endpoints are not in a generated client, so the REST calls are written by hand.

## Files to Modify
- `src/api/models.ts` — add the `RemediationSummary`, `SeverityStatusCount`, `ProductRemediation`, `RemediationVulnerability`, `RemediationStatus`, and `RemediationVulnerabilityFilters` types
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, and `fetchRemediationVulnerabilities(filters, params)`
- `tests/mocks/handlers.ts` — add MSW handlers for the three remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — `useQuery` hook for the summary
- `src/hooks/useRemediationByProduct.ts` — `useQuery` hook for the product breakdown
- `src/hooks/useRemediationVulnerabilities.ts` — `useQuery` hook for the filtered vulnerability list (filters and pagination in the query key)
- `tests/mocks/fixtures/remediation.json` — mock summary, by-product, and vulnerability data
- `src/hooks/useRemediationVulnerabilities.test.ts` — hook tests

## Implementation Notes
**Backend API contracts** (from Tasks 2–4 in trustify-backend):
- `GET /api/v2/remediation/summary`. Response: `{ total: number, by_status: { open: number, in_progress: number, resolved: number }, by_severity: Array<{ severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number, total: number }> }`. Defined in `modules/fundamental/src/remediation/endpoints/summary.rs` and `model/summary.rs`.
- `GET /api/v2/remediation/by-product?offset&limit&sort`. Response: `{ items: Array<{ product_id: string, product_name: string, total: number, open: number, in_progress: number, resolved: number }>, total: number }`. Defined in `modules/fundamental/src/remediation/endpoints/by_product.rs`.
- `GET /api/v2/remediation/vulnerabilities?severity&product&status&offset&limit&sort`. `severity` and `status` are comma-separated lists. Response: `{ items: Array<{ advisory_id: string, advisory_title: string, severity: string, status: "open"|"in_progress"|"resolved", product_id: string, product_name: string }>, total: number }`. An invalid filter value returns 400. Defined in `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs`.

At implementation time, verify these contracts against the trustify-backend `TC-9006` branch using the implement-task cross-repo API verification step.

- API values use snake_case/lowercase. Map them to display labels in the UI layer (tasks 7 and 8), not in the API types. Use `open` → "Open", `in_progress` → "In Progress", `resolved` → "Resolved", and lowercase severity → `SeverityBadge` levels via `src/utils/severityUtils.ts`.
- Use the Axios instance in `src/api/client.ts`. Do not create a new client.
- Follow the existing hook shape in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts`. Use query keys `["remediation","summary"]`, `["remediation","by-product",params]`, and `["remediation","vulnerabilities",filters,params]`, so a filter change triggers a refetch.
- Do not swallow request errors or turn them into empty data. Hooks must expose `isError`/`error` so that pages can tell "zero vulnerabilities" apart from "request failed".
- Per CONVENTIONS.md §API layer: put typed functions in `src/api/rest.ts` and React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope. Example: `fetchSboms()` in `src/api/rest.ts` with `src/hooks/useSboms.ts`.
- Per CONVENTIONS.md §State management: use React Query for server state (no Redux). Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's hook scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §Naming: use camelCase for hooks and utilities. Applies: task modifies `src/hooks/useRemediationVulnerabilities.ts` matching the convention's hook naming scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: use Vitest + RTL with MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mocking scope. Example: the existing SBOM handlers in `tests/mocks/handlers.ts` with `tests/mocks/fixtures/sboms.json`.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, a Jira footer, and an `Assisted-by:` trailer.
  - §3: the PR is created with `--base TC-9006` in trustify-ui, and the PR link is posted to Jira.
  - §5: changes stay limited to the listed files, and existing code is reused.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchAdvisories` — pattern for typed list fetch functions with query params
- `src/hooks/useSboms.ts` — React Query list hook pattern
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/advisories.json` — MSW handler and fixture pattern

## Acceptance Criteria
- [ ] The types for all three endpoint responses exist in `src/api/models.ts` and match the backend contracts
- [ ] `fetchRemediationSummary`, `fetchRemediationByProduct`, and `fetchRemediationVulnerabilities` call the exact backend paths through `src/api/client.ts`
- [ ] `fetchRemediationVulnerabilities` serializes multi-value severity/status filters as comma-separated query params, and leaves out unset filters
- [ ] The hooks include filters and pagination in the query keys
- [ ] Request failures are surfaced through `isError` and never turned into empty or zero data
- [ ] MSW handlers and fixtures exist for all three endpoints

## Test Requirements
- [ ] Hook test: `useRemediationVulnerabilities` sends the correct query string for combined filters
- [ ] Hook test: changing filters triggers a new request (query key changes)
- [ ] Hook test: a 500 response from MSW gives `isError === true` and `data === undefined`
- [ ] Hook test: `useRemediationSummary` returns the parsed fixture data

## Verification Commands
- `npx vitest run src/hooks` — the hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product
- Depends on: Task 4 — Add GET /api/v2/remediation/vulnerabilities (filterable list)
