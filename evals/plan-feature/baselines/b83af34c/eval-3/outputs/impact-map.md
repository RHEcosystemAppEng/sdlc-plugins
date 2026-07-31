# Impact Map: TC-9003 — SBOM Comparison View

## Feature Summary

**Key**: TC-9003
**Summary**: SBOM comparison view
**Priority**: Critical (propagated to all tasks)
**Fix Versions**: RHTPA 1.5.0 (propagated to all tasks)
**Labels**: ai-generated-jira
**Documentation Considerations**: New Content — document the comparison endpoint and comparison UI

## Workflow Mode

**Decision**: direct-to-main

**Rationale**: The feature spans two repositories (trustify-backend and trustify-ui). The backend comparison endpoint is additive (a new GET endpoint) and can be merged to main independently without breaking existing functionality. The frontend comparison page is also additive (new page, new route). Cross-repo dependency ordering is enforced via explicit task dependencies — backend tasks complete first, frontend tasks follow. No partial-merge atomicity risk exists because each individual task produces a shippable increment: the endpoint is usable via API clients before the UI exists, and the UI is built against the already-deployed endpoint.

## Repositories Impacted

### trustify-backend

| Area | Change | Files |
|---|---|---|
| SBOM comparison model | New response structs for the structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes) | `modules/fundamental/src/sbom/model/compare.rs` (create), `modules/fundamental/src/sbom/model/mod.rs` (modify) |
| SBOM comparison service | Diff computation logic — fetches package and advisory data for two SBOMs and computes the structured diff on-the-fly | `modules/fundamental/src/sbom/service/compare.rs` (create), `modules/fundamental/src/sbom/service/mod.rs` (modify) |
| SBOM comparison endpoint | `GET /api/v2/sbom/compare?left={id1}&right={id2}` — validates inputs, calls service, returns structured diff | `modules/fundamental/src/sbom/endpoints/compare.rs` (create), `modules/fundamental/src/sbom/endpoints/mod.rs` (modify) |
| Integration tests | Tests for the comparison endpoint covering normal diff, identical SBOMs, invalid IDs, large SBOMs | `tests/api/sbom_compare.rs` (create) |

### trustify-ui

| Area | Change | Files |
|---|---|---|
| API types | TypeScript interfaces for the comparison response shape (SbomComparisonResult, PackageDiff, VulnerabilityDiff, LicenseChange) | `src/api/models.ts` (modify) |
| API client | New `compareSboms(leftId, rightId)` function using Axios | `src/api/rest.ts` (modify) |
| React Query hook | `useSbomComparison` hook wrapping the API call with React Query | `src/hooks/useSbomComparison.ts` (create) |
| Comparison page | Full-page comparison view with SBOM selectors, diff sections (ExpandableSection), data tables, empty state, and loading state — per Figma design | `src/pages/SbomComparePage/SbomComparePage.tsx` (create), `src/pages/SbomComparePage/components/DiffSection.tsx` (create), `src/pages/SbomComparePage/SbomComparePage.test.tsx` (create) |
| Route registration | Add `/sbom/compare` route to the app router | `src/routes.tsx` (modify) |
| List page integration | Add "Compare" navigation link on the SBOM list page to navigate to the comparison page | `src/pages/SbomListPage/SbomListPage.tsx` (modify) |

## Task Breakdown

| Task | Title | Repository | Dependencies | Priority | Fix Version |
|---|---|---|---|---|---|
| 1 | SBOM comparison model and diff service | trustify-backend | None | Critical | RHTPA 1.5.0 |
| 2 | SBOM comparison endpoint and integration tests | trustify-backend | Task 1 | Critical | RHTPA 1.5.0 |
| 3 | SBOM comparison API types, client function, and React Query hook | trustify-ui | Task 2 | Critical | RHTPA 1.5.0 |
| 4 | SBOM comparison page and components | trustify-ui | Task 3 | Critical | RHTPA 1.5.0 |
| 5 | SBOM comparison documentation | trustify-backend | Tasks 2, 4 | Critical | RHTPA 1.5.0 |

## Field Propagation

- **Priority**: Critical — propagated from TC-9003 to all created tasks
- **Fix Versions**: RHTPA 1.5.0 — propagated from TC-9003 to all created tasks (fixVersion scope config absent, defaulting to 'both')

## Cross-Repository Dependencies

- Task 3 (trustify-ui) explicitly depends on Task 2 (trustify-backend) — the frontend API client and hook require the backend comparison endpoint to be available
- Task 4 (trustify-ui) depends on Task 3 (trustify-ui) which transitively depends on the backend endpoint
- Task 5 (documentation) depends on both Task 2 (backend endpoint) and Task 4 (frontend page) being complete

## Non-Functional Requirements Addressed

- p95 response time < 1s for SBOMs with up to 2000 packages: addressed in Task 1 (service diff algorithm efficiency) and Task 2 (endpoint performance test)
- Virtualized lists for > 100 changed packages: addressed in Task 4 (frontend comparison page)
- No new database tables — compute diff on-the-fly: addressed in Task 1 (service design)
