## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" action button to the existing SBOM list page, enabling users to select two SBOMs and navigate to the comparison page. This completes the user journey from UC-1: the user selects two SBOMs from the list and is taken to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to the SBOM table, selection state management, and "Compare selected" toolbar action button

## Implementation Notes
- Add a checkbox column to the existing SBOM table in `src/pages/SbomListPage/SbomListPage.tsx` using PatternFly's composable `Table` select variant. Track selected row IDs in component state.
- Add a "Compare selected" `Button` to the page toolbar (PatternFly `Toolbar`). The button should be disabled unless exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate()`.
- Follow the existing table patterns in `SbomListPage.tsx` for adding columns and toolbar actions.
- Reference `src/components/FilterToolbar.tsx` for toolbar layout patterns used across the application.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — this is the file being modified; follow its existing table and toolbar patterns
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar action button placement

## Acceptance Criteria
- [ ] Each row in the SBOM list table has a selection checkbox
- [ ] "Compare selected" button appears in the toolbar
- [ ] "Compare selected" button is disabled unless exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selecting more than two SBOMs keeps the button disabled (only exactly two enables it)

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: "Compare selected" button is disabled with 3+ selections
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page with correct query params

## Dependencies
- Depends on: Task 6 — Create SBOM comparison page and components (the target route must exist)

[sdlc-workflow] Description digest: sha256:5945d73de76591e9a129185e4bc3a5070716868953701e8f61a1ccdfba6fe188
