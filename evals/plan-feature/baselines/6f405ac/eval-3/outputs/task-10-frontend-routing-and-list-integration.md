## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and add a "Compare selected" workflow to the SBOM list page. Users select two SBOMs via checkboxes on the list page, click "Compare selected", and are navigated to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column and "Compare selected" button

## Implementation Notes
**Route registration** in `src/routes.tsx`:
Follow the existing pattern of lazy-loaded page components (React Router v6). Add a route entry for `/sbom/compare` that lazy-loads `SbomComparePage`.

**SBOM list page integration** in `src/pages/SbomListPage/SbomListPage.tsx`:
- Add a checkbox selection column to the existing SBOM table (PatternFly `Table` supports row selection)
- Add a "Compare selected" button in the toolbar area, disabled until exactly two SBOMs are selected
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` page scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions for pattern reference (lazy loading, path structure)
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page to extend with selection and comparison navigation

## Dependencies
- Depends on: Task 9 — Frontend comparison page (the page component this route points to)

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered in `src/routes.tsx` with lazy-loaded `SbomComparePage`
- [ ] SBOM list page has checkbox selection for each row
- [ ] "Compare selected" button appears in the list page toolbar
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: SbomListPage renders checkbox selection column
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the comparison URL with correct query params
