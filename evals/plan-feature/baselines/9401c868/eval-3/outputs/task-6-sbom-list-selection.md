## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection capability to the SBOM list page so users can select two SBOMs and navigate to the comparison view. This implements the primary entry point for comparison (UC-1): users select two SBOMs using checkboxes on the list page, click "Compare selected", and are navigated to the comparison page with the selected SBOM IDs in the URL.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection column to the SBOM table, track selected SBOMs in component state, add "Compare selected" toolbar action button

## Implementation Notes
- Add a PatternFly `Checkbox` column to the existing SBOM table as the first column. Track selected SBOM IDs in React state (e.g., `useState<string[]>([])`).
- Limit selection to exactly two SBOMs. When two are already selected, additional checkboxes should be disabled or clicking a third should deselect the oldest selection.
- Add a "Compare selected" PatternFly `Button` (secondary variant) to the page's toolbar area. The button should be disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- The "Compare selected" button should show the count of selected SBOMs (e.g., "Compare selected (2)") using a PatternFly `Badge`.
- Follow the existing `SbomListPage.tsx` patterns for toolbar actions and state management.
- Per CONVENTIONS.md §Component library: use PatternFly 5 components (Checkbox, Button, Badge) for the selection UI.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- existing list page; extend with selection capability rather than creating a new component
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar action button placement

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for selecting SBOMs
- [ ] Users can select up to two SBOMs using checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled when fewer than two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is visually clear (checked checkboxes, selection count)

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM table
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting fewer than two SBOMs keeps the button disabled
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
