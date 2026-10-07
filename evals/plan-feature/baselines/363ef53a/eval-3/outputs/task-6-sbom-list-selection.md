## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add multi-select capability to the SBOM list page so users can select exactly two SBOMs and navigate to the comparison view. This implements UC-1 from the feature requirements: users select two SBOMs using checkboxes on the list page, click "Compare selected", and are navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and a "Compare selected" toolbar action button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Add tests for selection and compare navigation behavior

## Implementation Notes
Follow the existing page pattern in `src/pages/SbomListPage/`. The `SbomListPage.tsx` already has a table with filters — add a checkbox column for row selection.

Per the repo's component library convention: all UI components use PatternFly 5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript/TSX component file scope.

Per the repo's testing convention: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.test.tsx` matching the convention's TypeScript test file scope.

**Selection implementation:**
- Add a checkbox column as the first column of the SBOM table using PatternFly's `Td` with `select` prop
- Maintain selection state as an array of selected SBOM IDs (max 2)
- When a third checkbox is checked, deselect the oldest selection (FIFO behavior) or disable additional checkboxes
- The "Compare selected" button appears in the toolbar when selection count > 0, enabled only when exactly 2 SBOMs are selected

**Navigation:**
- On "Compare selected" click, use React Router's `useNavigate` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`
- The first selected SBOM becomes the `left` (baseline), the second becomes `right` (comparison target)

**Figma design context:** The SBOM list page uses PatternFly composable `Table` with sortable columns. Add the checkbox column following PatternFly's selectable table pattern.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page to extend with selection
- `src/components/FilterToolbar.tsx` — existing toolbar component; the "Compare selected" button can be added alongside existing toolbar actions

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly two SBOMs via checkboxes
- [ ] "Compare selected" button appears in the toolbar when at least one SBOM is selected
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared when navigating away and returning

## Test Requirements
- [ ] Component test: checkbox column renders in the SBOM table
- [ ] Component test: selecting two SBOMs enables the "Compare selected" button
- [ ] Component test: selecting fewer than two SBOMs disables the "Compare selected" button
- [ ] Component test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections and export
