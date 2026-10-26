## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and modify the SBOM list page to support selecting two SBOMs and navigating to the comparison page. This enables the primary user workflow: select two SBOMs from the list, click "Compare selected," and navigate to the comparison view with both SBOM IDs in the URL.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table and a "Compare selected" action button

## Implementation Notes
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. See existing route definitions in `src/routes.tsx` for the established pattern.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript component scope.
- **Figma design reference:** The SBOM list page needs checkbox selection for multi-select (PatternFly `Table` supports row selection via `isSelectableRow` prop). The "Compare selected" button appears in the toolbar area above the table, enabled only when exactly two SBOMs are selected.
- **Route registration:** Add the comparison route before the SBOM detail route to prevent `/sbom/compare` from being matched as an SBOM ID by `/sbom/:id`.
- **SBOM list page modifications:**
  - Add a checkbox selection column to the existing PatternFly `Table` in `SbomListPage.tsx`
  - Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`)
  - Add a "Compare selected" PatternFly `Button` in the toolbar area, disabled when selection count is not exactly 2
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate` hook
- Use React Router's `useNavigate` hook for programmatic navigation to the comparison page.
- Reference the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` for toolbar layout patterns — the "Compare selected" button should integrate with the existing toolbar UI.
- Ensure the route supports direct navigation with query params for URL-shareable comparisons.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions for the lazy-loading pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — the page being modified; reference its current structure for where to add selection state and button
- `src/components/FilterToolbar.tsx::FilterToolbar` — reference for toolbar layout where the "Compare selected" button should be placed

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered in `src/routes.tsx` and renders the SbomComparePage component
- [ ] SbomComparePage is lazy-loaded using React.lazy or equivalent
- [ ] SBOM list page table has a checkbox selection column
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] "Compare selected" button is disabled when the number of selected SBOMs is not exactly 2
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Direct navigation to `/sbom/compare?left={id1}&right={id2}` renders the comparison page correctly
- [ ] Existing SBOM list page functionality (filtering, sorting, pagination) is not affected

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when no SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when only one SBOM is selected
- [ ] Unit test: "Compare selected" button is enabled when exactly two SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs
- [ ] Unit test: `/sbom/compare` route renders SbomComparePage

## Verification Commands
- `npx tsc --noEmit` — TypeScript compiles without errors
- `npx vitest run src/pages/SbomListPage` — list page tests pass
- `npx vitest run src/routes` — route tests pass (if any)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Build SBOM comparison page UI
