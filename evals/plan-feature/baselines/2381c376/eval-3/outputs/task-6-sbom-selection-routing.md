## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" button to the existing SBOM list page, wire up the route for the new comparison page, and ensure navigation flows correctly between the list page and comparison view. This task connects the comparison page (Task 5) into the application's routing and provides the primary entry point for starting a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and a "Compare selected" toolbar action
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/App.tsx` — ensure the new route is included in the router setup (if not auto-included via routes.tsx)

## Implementation Notes
1. **Route wiring** in `src/routes.tsx`: add a route entry for `/sbom/compare` that lazy-loads `SbomComparePage`. Follow the existing pattern of lazy-loaded page components in `routes.tsx`. The route must be defined before the `/sbom/:id` route to avoid path conflicts (React Router matches in order).

2. **SBOM list page selection** in `src/pages/SbomListPage/SbomListPage.tsx`:
   - Add PatternFly `Table` row selection using checkboxes (PatternFly's `isSelectableRow` prop or a selection state managed via React state).
   - Track selected SBOM IDs in component state (limit selection to exactly 2).
   - Add a "Compare selected" PatternFly `Button` in the page toolbar (alongside existing filters). The button is disabled unless exactly 2 SBOMs are selected.
   - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`. Follow the Figma design where the button navigates directly to the comparison view.

3. **Navigation flow**: when the user selects two SBOMs and clicks "Compare selected", the app navigates to the comparison page with both IDs in the URL. The comparison page (Task 5) reads these params and auto-triggers the comparison.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's routing scope.

Per CONVENTIONS.md §Component Library: use PatternFly 5 for the selection checkboxes and Compare button.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions; follow the lazy-loading pattern for new page routes
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page; extend with selection capability
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for adding toolbar actions

## Acceptance Criteria
- [ ] Route `/sbom/compare` is defined in `routes.tsx` and lazy-loads SbomComparePage
- [ ] SBOM list page renders selection checkboxes on each table row
- [ ] Selection is limited to a maximum of 2 SBOMs
- [ ] "Compare selected" button appears in the list page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Comparison page loads correctly when navigated to from the list page
- [ ] Direct URL navigation to `/sbom/compare?left={id1}&right={id2}` works (bookmarkable)

## Test Requirements
- [ ] Unit test: SbomListPage renders selection checkboxes
- [ ] Unit test: selecting more than 2 SBOMs is prevented or handled
- [ ] Unit test: "Compare selected" button is disabled with fewer than 2 selections
- [ ] Unit test: "Compare selected" navigates to the correct comparison URL
- [ ] Unit test: route `/sbom/compare` renders SbomComparePage component

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections
