# Task 6 — Add "Compare selected" action to SBOM list page

## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox selection to the SBOM list table and a "Compare selected" action button that navigates to the comparison page with the two selected SBOM IDs as URL query parameters. This implements UC-1 from the feature description: users select two SBOMs from the list page and click "Compare selected" to initiate a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row checkboxes to the SBOM table, track selection state, add "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Use PatternFly's `Table` composable with `isSelectable` row behavior to add checkboxes. PatternFly 5 tables support row selection natively.
- Track selected SBOM IDs in React component state (e.g., `useState<string[]>([])`).
- Limit selection to exactly 2 SBOMs: disable further checkboxes once 2 are selected, or show a validation message.
- The "Compare selected" button should be disabled until exactly 2 SBOMs are selected.
- On click, use React Router's `useNavigate` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- Follow the existing toolbar pattern in `SbomListPage.tsx` for placing the action button.
- Reference `src/components/FilterToolbar.tsx` for toolbar layout patterns with PatternFly.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing table and toolbar implementation to extend
- `src/components/FilterToolbar.tsx` — Toolbar layout pattern reference

## Acceptance Criteria
- [ ] SBOM list table has selectable rows with checkboxes
- [ ] Users can select exactly 2 SBOMs
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: checkboxes appear in the SBOM list table
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking the button navigates to the correct comparison URL

## Dependencies
- Depends on: Task 5 — Add SBOM comparison page with diff sections and route (the target page must exist)
