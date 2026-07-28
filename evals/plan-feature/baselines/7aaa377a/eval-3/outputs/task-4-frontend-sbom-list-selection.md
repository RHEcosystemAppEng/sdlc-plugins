# Task 4 — Add SBOM selection and compare navigation on list page

## Repository
trustify-ui

## Target Branch
main

## Description
Add SBOM selection support to the existing SBOM list page so users can select two SBOMs and navigate to the comparison page. This implements the entry point for the comparison workflow (UC-1 from TC-9003): users select two SBOMs using checkboxes on the list page, click "Compare selected", and are navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes to the SBOM table and a "Compare selected" toolbar action button that navigates to the comparison page with selected SBOM IDs as query params

## Implementation Notes
- Add PatternFly table row selection (checkboxes) to the existing SBOM table in `SbomListPage.tsx`. Use PatternFly's composable Table selection pattern.
- Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`).
- Add a "Compare selected" action button in the page toolbar. The button should be disabled until exactly 2 SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate` hook.
- Follow the existing toolbar pattern in `SbomListPage.tsx` for button placement and PatternFly styling.
- Use the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` as a reference for toolbar layout patterns.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing list page to extend; study its current toolbar and table structure
- `src/components/FilterToolbar.tsx` — existing reusable filter toolbar pattern for toolbar layout reference

## Acceptance Criteria
- [ ] SBOM list page table rows have selection checkboxes
- [ ] Users can select exactly two SBOMs using checkboxes
- [ ] "Compare selected" button appears in the toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the selected SBOM IDs
- [ ] Selecting/deselecting SBOMs updates the button state correctly
- [ ] Existing list page functionality (filters, sorting, pagination) is not broken

## Test Requirements
- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: "Compare selected" button is disabled with 0 selections
- [ ] Unit test: "Compare selected" button is disabled with 1 selection
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: "Compare selected" button is disabled with 3+ selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with selected IDs

## Dependencies
- Depends on: Task 3 — Build SBOM comparison page with diff sections (the navigation target must exist)
