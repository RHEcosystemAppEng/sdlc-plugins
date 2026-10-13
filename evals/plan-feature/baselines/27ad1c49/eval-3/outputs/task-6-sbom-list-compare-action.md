## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection capability and a "Compare selected" action to the existing SBOM list page, enabling users to select exactly two SBOMs from the table and navigate to the comparison view with the selected IDs pre-populated in the URL.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table and a "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
**Figma Design Context** (UC-1 from feature requirements — SBOM selection for comparison):

Modify the existing SBOM list table in `src/pages/SbomListPage/SbomListPage.tsx` to support row selection for comparison:
- Add PatternFly `Table` row selection with checkbox select variant on each row.
- Limit selection to exactly two SBOMs — disable further checkboxes once two rows are selected.
- Add a "Compare selected" PatternFly `Button` (primary variant) to the toolbar area alongside the existing `FilterToolbar` from `src/components/FilterToolbar.tsx`. Button is disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate` hook, passing the two selected SBOM IDs as query parameters.

The SbomListPage already uses a PatternFly Table and the FilterToolbar component. Add the compare action to the existing toolbar without disrupting current functionality.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page to extend with selection
- `src/components/FilterToolbar.tsx` — existing toolbar where the compare button should be placed

## Acceptance Criteria
- [ ] SBOM list page table rows display selection checkboxes
- [ ] Users can select up to two SBOMs; further selection is disabled after two are checked
- [ ] "Compare selected" button appears in the toolbar, disabled until exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with correct IDs
- [ ] Selection state clears appropriately when the user navigates away and returns

## Test Requirements
- [ ] Unit test: selection checkboxes render on each SBOM table row
- [ ] Unit test: "Compare selected" button is disabled with fewer than two selections
- [ ] Unit test: clicking "Compare selected" triggers navigation to the correct comparison URL
