# Task 7 — Add SBOM selection and "Compare selected" to SbomListPage

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SBOM list page to support selecting two SBOMs via checkboxes and navigating to the comparison page. Add checkbox selection to each row in the SBOM table and a "Compare selected" button in the toolbar that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and "Compare selected" button in the page toolbar

## Implementation Notes
- Use PatternFly's `Table` composable pattern with a checkbox column (using `Td` with `select` prop). Follow the existing table pattern in `SbomListPage.tsx`.
- Track selected SBOM IDs in component state using `useState<string[]>([])`.
- "Compare selected" button: render as a PatternFly `Button` (secondary variant) in the existing toolbar. Disabled unless exactly 2 SBOMs are selected. On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- The button text should indicate selection count when fewer than 2 or more than 2 are selected, e.g., "Compare selected (2)" or tooltip guidance.
- Do not modify the existing table columns or filters — only add the selection mechanism.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified
- `src/components/FilterToolbar.tsx` — reference for toolbar button placement

## Acceptance Criteria
- [ ] Each SBOM row has a checkbox for selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets on page navigation or filter changes
- [ ] Existing table functionality (sorting, filtering, pagination) is not affected

## Test Requirements
- [ ] Unit test: checkbox appears in each table row
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections (route must exist for navigation)
