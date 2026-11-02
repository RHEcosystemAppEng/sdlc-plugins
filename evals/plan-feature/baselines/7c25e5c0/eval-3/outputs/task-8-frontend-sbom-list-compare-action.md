## Repository
trustify-ui

## Target Branch
main

## Description
Add multi-select checkboxes and a "Compare selected" action button to the existing SBOM list page. When users select exactly two SBOMs and click the button, the app navigates to the comparison page with the selected SBOM IDs as URL query parameters. This enables the primary user workflow described in UC-1.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add selection state, checkbox column to the SBOM table, and "Compare selected" toolbar action

## Implementation Notes
Modify the existing `SbomListPage` component:
- Add a selection state using React `useState` to track selected SBOM IDs (limit to 2)
- Add a checkbox column to the existing SBOM table using PatternFly `Table` row selection
- Add a "Compare selected" button to the page toolbar, disabled unless exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- Reference `src/pages/SbomListPage/SbomListPage.tsx` for the existing table structure and toolbar layout
- The `SbomListPage.test.tsx` should be updated to cover the new selection and navigation behavior

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React component scope.

## Acceptance Criteria
- [ ] SBOM list table has selectable rows with checkboxes
- [ ] Selection is limited to a maximum of 2 SBOMs
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Test that checkboxes are rendered in the table
- [ ] Test that selecting more than 2 SBOMs is prevented or the button remains disabled
- [ ] Test that clicking "Compare selected" with 2 SBOMs navigates to the correct URL

## Dependencies
- Depends on: Task 7 — Frontend comparison page
