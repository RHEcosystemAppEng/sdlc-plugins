## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the `/sbom/compare` route to the application router and integrate a "Compare selected" action into the existing SbomListPage. Users can select two SBOMs via checkboxes on the list page and click "Compare selected" to navigate to the comparison view with the selected SBOM IDs in the URL.

## Files to Modify
- `src/routes.tsx` — add route definition for /sbom/compare pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to SBOM table, track selected SBOMs, add "Compare selected" button in toolbar

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response data for MSW handlers
- `tests/mocks/handlers.ts` — add MSW handler for GET /api/v2/sbom/compare (modify existing file)

## Implementation Notes
- Add the route to `src/routes.tsx` following the existing lazy-loading pattern. See how `SbomDetailPage` and other pages are registered as routes.
- For SbomListPage changes:
  1. Add a checkbox column to the existing SBOM table (PatternFly `Table` supports row selection via `select` prop)
  2. Track selected SBOM IDs in component state (limit to max 2 selections)
  3. Add a "Compare selected" button to the toolbar area (next to existing filter controls)
  4. Button is disabled when fewer than 2 SBOMs are selected
  5. On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- For MSW mock handler: add a handler for `GET /api/v2/sbom/compare` that returns the fixture data from `sbom-comparison.json`. Follow the pattern in `tests/mocks/handlers.ts`.
- Per CONVENTIONS.md: use React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition file scope.
- Per CONVENTIONS.md: testing uses Vitest + React Testing Library for unit tests and MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's test mock file scope.

**Relevant constraints from docs/constraints.md:**
- Commit rules (section 2): every commit must reference TC-9003, follow Conventional Commits, include AI attribution trailer
- PR rules (section 3): branch named after Jira issue ID, PR link posted to Jira task
- Code change rules (section 5): changes scoped to listed files, inspect code before modifying, follow referenced patterns, no duplication

## Reuse Candidates
- `src/routes.tsx` — existing route definitions, follow the same lazy-loading pattern for the compare route
- `src/pages/SbomListPage/SbomListPage.tsx` — the page being modified; reference for existing toolbar and table structure
- `tests/mocks/handlers.ts` — existing MSW handlers, follow the same pattern for the comparison endpoint mock
- `tests/mocks/fixtures/sboms.json` — existing mock fixture, reference for fixture data structure

## Acceptance Criteria
- [ ] /sbom/compare route is registered in routes.tsx and renders SbomComparePage
- [ ] SbomComparePage is lazy-loaded (code-split)
- [ ] SbomListPage shows a checkbox column in the SBOM table
- [ ] Users can select up to 2 SBOMs via checkboxes
- [ ] "Compare selected" button appears in the SbomListPage toolbar
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to /sbom/compare?left={id1}&right={id2}
- [ ] MSW handler for comparison endpoint is registered and returns fixture data
- [ ] Comparison fixture data matches the SbomComparisonResult interface shape

## Test Requirements
- [ ] Unit test: /sbom/compare route renders SbomComparePage component
- [ ] Unit test: SbomListPage renders checkbox column in SBOM table
- [ ] Unit test: selecting 2 SBOMs enables the "Compare selected" button
- [ ] Unit test: clicking "Compare selected" navigates to correct URL with both SBOM IDs
- [ ] Unit test: selecting fewer than 2 SBOMs keeps "Compare selected" button disabled
- [ ] Unit test: MSW handler returns valid comparison response for tests

## Dependencies
- Depends on: Task 4 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 6 — Build SBOM comparison page with diff sections
