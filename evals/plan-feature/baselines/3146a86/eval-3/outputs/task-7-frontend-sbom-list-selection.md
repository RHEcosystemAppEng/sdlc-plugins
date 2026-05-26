# Task 7 — Add SBOM selection and "Compare selected" to SbomListPage

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SBOM list page to support selecting two SBOMs for comparison. Add checkboxes to each row in the SBOM table and a "Compare selected" toolbar button that navigates to the comparison page with the selected SBOM IDs as URL query parameters. The button should be disabled until exactly two SBOMs are selected.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and "Compare selected" button to the toolbar

## Implementation Notes
- Per the frontend key conventions (Component library): use PatternFly 5 components. The SBOM list table likely already uses PF5 `Table` — add the `select` variant for row checkboxes.
- Per the Figma design (UC-1): the user selects two SBOMs using checkboxes, then clicks "Compare selected". The button navigates to `/sbom/compare?left={id1}&right={id2}`.
- Use React Router's `useNavigate` hook to navigate to the comparison page with the selected IDs as query parameters.
- Limit selection to exactly two SBOMs. When two are selected, disable further checkbox selection (or show a tooltip indicating the maximum). When fewer than two are selected, disable the "Compare selected" button.
- The "Compare selected" button should be a secondary PatternFly `Button` in the page toolbar area, near existing action buttons.
- Per constraint 5.1: changes must be scoped to the files listed — only modify `SbomListPage.tsx`.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing component to modify; inspect current table implementation for select variant integration
- `src/components/FilterToolbar.tsx` — reference for toolbar layout and button placement patterns

## Acceptance Criteria
- [ ] Each SBOM row in the list table has a selection checkbox
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer than two SBOMs are selected
- [ ] Clicking "Compare selected" with two SBOMs selected navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection is limited to a maximum of two SBOMs

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with zero or one SBOM selected
- [ ] Unit test: "Compare selected" button is enabled with exactly two SBOMs selected
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs
- [ ] Unit test: user cannot select more than two SBOMs simultaneously

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections (the target page must exist for navigation)
