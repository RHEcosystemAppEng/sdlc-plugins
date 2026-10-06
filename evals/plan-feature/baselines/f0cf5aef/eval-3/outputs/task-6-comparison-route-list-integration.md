## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the route definition for the SBOM comparison page and integrate a "Compare selected" entry point on the SBOM list page. Users will be able to select two SBOMs via checkboxes on the list page and click a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the lazy-loaded `SbomComparisonPage` component
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection to the SBOM table rows and a "Compare selected" toolbar action button

## Implementation Notes
Per the frontend routing convention: React Router v6 with lazy-loaded page components. Add the comparison route using `React.lazy(() => import(...))` pattern consistent with existing routes.
Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route file scope.

Per the frontend component library convention: all UI components use PatternFly 5 equivalents. The checkbox selection uses PatternFly Table's built-in select capability, and the toolbar action uses PatternFly's Button.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript component scope.

**Route definition:**
- Path: `/sbom/compare`
- Component: `SbomComparisonPage` (lazy-loaded)
- Place the route before `/sbom/:id` to avoid route matching conflicts

**SBOM list page changes:**
- Add a selectable row capability to the SBOM table (PatternFly Table `select` property)
- Track selected SBOM IDs in local component state (not React Query — this is UI state)
- Add a "Compare selected" button to the toolbar, disabled unless exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- Show a tooltip or helper text indicating "Select exactly 2 SBOMs to compare"

## Reuse Candidates
- `src/routes.tsx` — existing route definitions to follow for lazy-loading pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page with table and filters; the selection state integrates with the existing table structure
- `src/components/FilterToolbar.tsx` — existing toolbar component pattern (the Compare button integrates into the existing toolbar area)

## Acceptance Criteria
- [ ] Route `/sbom/compare` renders the `SbomComparisonPage` component
- [ ] Route is lazy-loaded consistent with existing route patterns
- [ ] SBOM list page table rows have selectable checkboxes
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] "Compare selected" button is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Route `/sbom/compare` does not conflict with `/sbom/:id` detail route

## Test Requirements
- [ ] Unit test: `/sbom/compare` route renders the comparison page component
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to correct URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections
