## Repository
trustify-ui

## Target Branch
main

## Description
Add a "Compare selected" action to the SbomListPage that allows users to select two SBOMs via checkboxes and navigate to the comparison page. This implements the entry point for Use Case UC-1 where users start from the SBOM list page.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection (checkboxes), "Compare selected" toolbar action button, and navigation to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- Follow the existing page pattern in `src/pages/SbomListPage/SbomListPage.tsx` which already has a table with filters.
- Add PatternFly `Table` row selection with checkboxes (use `isSelectable` prop on table rows).
- Add a "Compare selected" button to the toolbar (alongside any existing toolbar actions).
- The button should:
  - Be disabled unless exactly two SBOMs are selected
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
  - Show a tooltip or disabled state text when fewer or more than two SBOMs are selected
- Use React state to track selected row IDs.
- Do not modify the existing table columns, filters, or pagination behavior.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified
- `src/components/FilterToolbar.tsx` — existing toolbar pattern for reference on where to place the action button

## Acceptance Criteria
- [ ] SBOM list table has selectable rows with checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Button is enabled when exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Existing table functionality (sorting, filtering, pagination) is not affected

## Test Requirements
- [ ] Unit test: checkboxes render on each table row
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL

## Verification Commands
- `npm run build` — TypeScript compiles without errors
- `npm run test` — all tests pass

## Dependencies
- Depends on: Task 5 — Frontend comparison page (the comparison page route must exist for navigation to work)
