## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection and a "Compare selected" action to the SBOM list page, enabling users to select two SBOMs and navigate to the comparison view. This implements the entry point described in UC-1 of the feature requirements.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row checkboxes (max 2 selectable) and a "Compare selected" toolbar action that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Checkbox selection**: Add PatternFly `Table` row selection (checkbox type) to the existing SBOM list table. Limit selection to a maximum of two rows — disable remaining checkboxes once two are selected.
- **"Compare selected" button**: Add a toolbar action button that is enabled only when exactly two SBOMs are selected. On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
- Follow the existing table and toolbar patterns in `SbomListPage.tsx`.
- Use PatternFly `ToolbarItem` for placement in the existing toolbar alongside filters.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing SBOM list page where the selection and action will be added
- `src/components/FilterToolbar.tsx` — Reference for toolbar action patterns

## Acceptance Criteria
- [ ] SBOM list table rows have selectable checkboxes
- [ ] Maximum of two SBOMs can be selected at a time
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with correct IDs

## Test Requirements
- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: selecting more than two SBOMs is prevented
- [ ] Unit test: "Compare selected" button is enabled only with exactly two selected
- [ ] Unit test: clicking the button navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Frontend comparison page UI
