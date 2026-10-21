## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" button to the SBOM list page, and register the `/sbom/compare` route in the application router. When a user selects two SBOMs from the list and clicks "Compare selected", the app navigates to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and "Compare selected" toolbar action
- `src/routes.tsx` — register the `/sbom/compare` route with lazy-loaded SbomComparePage component
- `src/App.tsx` — verify route is included in router setup (may not need changes if routes.tsx is the single source)

## Implementation Notes
### Figma design context

The SBOM list page gains PatternFly row selection checkboxes on each table row and a "Compare selected" toolbar button. The button is disabled until exactly two SBOMs are selected. Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`.

### Technical implementation

- Per CONVENTIONS.md §Component Library: use PatternFly 5 `Table` row selection (checkbox column) and PatternFly `Button` for the compare action.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Page Structure: the SbomListPage already exists; add selection state management and the compare navigation action.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` page scope.
- Use React Router's `useNavigate()` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` when the Compare button is clicked.
- Per CONVENTIONS.md §Routing: register the route in `src/routes.tsx` with lazy loading, following the existing pattern for other pages.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route scope.
- Track selected SBOM IDs in local component state (useState). Enable the "Compare selected" button only when exactly 2 SBOMs are selected.
- Follow the existing toolbar pattern in `SbomListPage.tsx` which already uses `FilterToolbar` from `src/components/FilterToolbar.tsx`.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page with PatternFly Table; extend with selection support
- `src/components/FilterToolbar.tsx` — existing toolbar component; the Compare button sits alongside existing toolbar actions
- `src/routes.tsx` — existing route definitions; follow the lazy-loading pattern for the new comparison route

## Acceptance Criteria
- [ ] SBOM list page table rows have selection checkboxes
- [ ] "Compare selected" button appears in the list page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] `/sbom/compare` route is registered in `src/routes.tsx` and renders SbomComparePage
- [ ] Route uses lazy loading for the SbomComparePage component

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when 0 SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when 1 SBOM is selected
- [ ] Unit test: "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when 3+ SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page with correct query params
- [ ] Unit test: `/sbom/compare` route renders the SbomComparePage component

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Build SBOM comparison page UI with diff sections
