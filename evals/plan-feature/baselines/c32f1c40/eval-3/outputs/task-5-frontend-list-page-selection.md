## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox selection and a "Compare selected" button to the SBOM list page, enabling users to select exactly two SBOMs and navigate to the comparison view. This implements the entry point for UC-1 (Compare two SBOM versions) where users start from the SBOM list page.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, track selected rows (max 2), and add a "Compare selected" toolbar action that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Figma design reference:** The SBOM list page adds checkboxes for row selection. When exactly two rows are selected, a "Compare selected" button appears (or becomes enabled) in the page toolbar. Clicking it navigates to the comparison page with the two selected SBOM IDs as URL query parameters.
- Per CONVENTIONS.md §Component library: use PatternFly 5 `Table` composable with `isSelectableRow` for checkbox selection, and a PatternFly `Button` for the "Compare selected" action.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.
- Use React Router's `useNavigate()` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` when the Compare button is clicked.
- Selection state can be managed with `useState<string[]>([])` tracking the selected SBOM IDs. Cap selection at 2 — disable further checkboxes when 2 are already selected, or deselect the oldest selection when a third is checked.
- The "Compare selected" button should be disabled when fewer than 2 SBOMs are selected.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing list page with table; extend with selection capability
- `src/components/FilterToolbar.tsx` — Existing toolbar component; the "Compare selected" button should integrate alongside existing toolbar actions

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select up to two SBOMs via checkboxes
- [ ] "Compare selected" button appears in the toolbar
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Selecting a third SBOM either deselects the oldest or is prevented

## Test Requirements
- [ ] Unit test: checkbox selection toggles SBOM selection state
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page (the navigation target must exist)
