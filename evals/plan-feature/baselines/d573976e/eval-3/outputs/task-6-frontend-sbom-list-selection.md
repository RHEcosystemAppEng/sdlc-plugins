# Task 6 — Add SBOM selection checkboxes and "Compare selected" action to SbomListPage

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SbomListPage to allow users to select two SBOMs via checkboxes and navigate to the comparison page. This implements UC-1 from the feature requirements: users navigate to the SBOM list page, select two SBOMs using checkboxes, and click "Compare selected" to navigate to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add selection checkboxes to the SBOM table rows and a "Compare selected" toolbar action button

## Implementation Notes
- Use PatternFly's `Table` selection capabilities — the composable Table supports row selection via `isSelected` and `onSelect` props.
- Maintain selection state locally using `useState` — track selected SBOM IDs in an array.
- The "Compare selected" button should:
  - Appear in the table toolbar area (alongside existing filters if any)
  - Be disabled until exactly two SBOMs are selected
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
- Consider adding a visual indicator showing how many SBOMs are selected (e.g., "2 of 2 selected" text near the button).
- Limit selection to a maximum of two SBOMs — after two are selected, further checkboxes should be disabled or show a warning.
- Follow the existing SbomListPage structure — this page already has a table with filters (`src/pages/SbomListPage/SbomListPage.tsx`). Add the selection feature without restructuring the existing table.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — The existing page being modified; understand its current table structure and toolbar layout
- `src/components/FilterToolbar.tsx` — Existing filter toolbar; the Compare button should integrate with or sit alongside this toolbar

## Acceptance Criteria
- [ ] Each SBOM row in the list table has a selection checkbox
- [ ] Users can select up to two SBOMs
- [ ] "Compare selected" button appears in the table toolbar
- [ ] Button is disabled until exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is managed correctly (selecting a third SBOM is prevented or deselects the oldest)

## Test Requirements
- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with header toolbar and diff sections
