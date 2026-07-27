## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the `/sbom/compare` route to the application router and integrate the comparison flow with the SBOM list page. Users will be able to select two SBOMs using checkboxes on the list page and click a "Compare selected" action button that navigates to the comparison page with the selected SBOM IDs as URL query parameters. This completes the end-to-end user workflow from SBOM selection to comparison view.

**Figma design reference:** The SBOM list page (SbomListPage) adds checkbox selection per row and a "Compare selected" action button in the toolbar area. The button is a PatternFly `Button` (secondary variant) that becomes enabled when exactly two SBOMs are selected. Navigation to `/sbom/compare?left={id1}&right={id2}` uses React Router's `useNavigate` hook. The comparison page route is lazy-loaded per the existing routing convention.

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to lazy-loaded SbomComparePage
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox column to the SBOM table, add "Compare selected" button to the toolbar, manage selected SBOM state, navigate to comparison page on button click
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- add tests for the checkbox selection and compare navigation behavior

## Implementation Notes
Per CONVENTIONS.md routing: React Router v6 with lazy-loaded page components. Add the comparison route alongside existing routes in `src/routes.tsx`. See the existing route definitions for the lazy import pattern.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route file scope.

Per CONVENTIONS.md page structure: modifications to SbomListPage follow the existing component patterns in that directory. See `src/pages/SbomListPage/SbomListPage.tsx` for the current toolbar and table structure.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md testing: update the existing test file with new test cases for the checkbox and compare functionality using Vitest + React Testing Library. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established test pattern.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.test.tsx` matching the convention's `.tsx` test file scope.

**Route definition:**
- Path: `/sbom/compare`
- Component: lazy(() => import("./pages/SbomComparePage/SbomComparePage"))
- Place the route after the existing `/sbom/:id` route to avoid route matching conflicts

**SBOM list page changes:**
- Add a `useState<string[]>` for selected SBOM IDs (initialize as empty array)
- Add a checkbox column to the PatternFly Table as the first column using `Td` with `select` prop
- Add a "Compare selected" `Button` (secondary variant) to the toolbar, enabled only when `selectedIds.length === 2`
- On button click: `navigate(\`/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}\`)`
- When more than 2 SBOMs are selected, show a tooltip on the Compare button: "Select exactly two SBOMs to compare"

**URL-shareable comparison:**
- The comparison page reads `left` and `right` from `useSearchParams()` on mount
- This enables bookmarking and sharing comparison URLs directly

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- existing list page to extend with selection capability
- `src/routes.tsx` -- existing route definitions to follow for the new route entry
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` -- reference for lazy-loaded page import pattern in routes

## Acceptance Criteria
- [ ] Route `/sbom/compare` is defined and loads SbomComparePage
- [ ] SBOM list page table has checkbox column for row selection
- [ ] "Compare selected" button appears in the SbomListPage toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Comparison page loads with pre-populated SBOM selectors when accessed via URL with query params
- [ ] Direct navigation to `/sbom/compare?left={id1}&right={id2}` renders the comparison without re-selection

## Test Requirements
- [ ] Component test: checkbox column renders in the SBOM list table
- [ ] Component test: selecting two SBOMs enables the Compare button
- [ ] Component test: selecting one or three SBOMs keeps the Compare button disabled
- [ ] Component test: clicking Compare button navigates to the correct URL with query params
- [ ] Component test: route `/sbom/compare` renders SbomComparePage component
- [ ] E2E consideration: verify end-to-end flow from list page selection to comparison view rendering

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Implement SBOM comparison page UI (the page component this route points to)
