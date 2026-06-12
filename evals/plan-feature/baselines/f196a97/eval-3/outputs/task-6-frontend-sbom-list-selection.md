# Task 6 — Add SBOM selection and "Compare selected" action to SbomListPage

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SBOM list page to support selecting two SBOMs via checkboxes and navigating to the comparison page. Add a row selection mechanism to the SBOM list table, a "Compare selected" action button that appears when exactly two SBOMs are selected, and navigation to `/sbom/compare?left={id1}&right={id2}` when clicked. This is the primary entry point for UC-1 (Compare two SBOM versions).

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column, selection state management, and "Compare selected" toolbar action

## Implementation Notes
- Add PatternFly `Table` row selection using the composable table's `select` feature. Each row gets a checkbox in the first column.
- Track selected SBOM IDs in component state using `useState<string[]>([])`. Limit selection to a maximum of two SBOMs.
- Add a "Compare selected" `Button` to the page's toolbar/action area. The button should:
  - Be hidden or disabled when fewer than 2 SBOMs are selected
  - Be enabled (primary variant) when exactly 2 SBOMs are selected
  - On click, use React Router's `useNavigate()` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`
- Follow the existing toolbar pattern in `SbomListPage.tsx` which already uses `FilterToolbar` from `src/components/FilterToolbar.tsx`.
- When more than 2 SBOMs are checked, either prevent additional selection or show a tooltip/message indicating only 2 can be compared at once.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the file being modified; study its existing table and toolbar structure
- `src/components/FilterToolbar.tsx` — existing toolbar pattern in the SBOM list page, reference for action button placement

## Acceptance Criteria
- [ ] SBOM list table rows have selectable checkboxes
- [ ] "Compare selected" button appears when exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection is limited to a maximum of 2 SBOMs
- [ ] Deselecting an SBOM updates the button state correctly

## Test Requirements
- [ ] Unit test: checkbox selection adds SBOM ID to selection state
- [ ] Unit test: "Compare selected" button is disabled/hidden with fewer than 2 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections (route must exist for navigation)
