# Task 9 — Add "Compare selected" action to the SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add multi-select checkboxes and a "Compare selected" button to the SBOM list page. When a user selects exactly two SBOMs and clicks "Compare selected", the app navigates to `/sbom/compare?left={id1}&right={id2}`. This provides the primary entry point for the comparison workflow as described in UC-1.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table and a "Compare selected" toolbar action button that navigates to the comparison page with selected SBOM IDs as query parameters

## Implementation Notes
- Use PatternFly's composable `Table` row selection feature (checkbox column) to enable multi-select.
- Add a "Compare selected" button to the existing toolbar area (near filters). The button should be:
  - Disabled when fewer or more than 2 SBOMs are selected
  - Primary variant when exactly 2 SBOMs are selected
- On click, use React Router's `useNavigate` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- Track selected row IDs in component state (`useState<string[]>`).
- Follow the existing toolbar pattern in `SbomListPage.tsx` — add the button alongside existing filter controls.
- Reference `src/components/FilterToolbar.tsx` for toolbar layout patterns.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — The file being modified; understand existing table and toolbar structure
- `src/components/FilterToolbar.tsx` — Existing toolbar component; reference for button placement pattern

## Acceptance Criteria
- [ ] SBOM list table has selection checkboxes on each row
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets appropriately (e.g., on page navigation or filter change)

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled when 0 SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when 1 SBOM is selected
- [ ] Unit test: "Compare selected" button is enabled when 2 SBOMs are selected
- [ ] Unit test: "Compare selected" button is disabled when 3+ SBOMs are selected
- [ ] Unit test: clicking "Compare selected" with 2 SBOMs navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Add SBOM comparison page with diff sections
