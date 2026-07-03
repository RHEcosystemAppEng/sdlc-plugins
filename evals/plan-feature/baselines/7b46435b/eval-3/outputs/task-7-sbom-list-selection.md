## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Modify the existing SBOM list page to support selecting two SBOMs for comparison. Add checkbox selection to the SBOM table rows and a "Compare selected" button in the page toolbar that navigates to the comparison page with the selected SBOM IDs as URL parameters.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add checkbox selection column to the SBOM table and "Compare selected" button to the toolbar

## Implementation Notes
- Add PatternFly `Table` row selection (checkbox) to the existing SBOM table. Use PatternFly's composable `Table` selection pattern -- check the existing table implementation in `SbomListPage.tsx` for the current column configuration and extend it with a select column.
- Add a "Compare selected" button to the page toolbar (alongside existing filters from `FilterToolbar`). The button should:
  - Be disabled until exactly 2 SBOMs are selected
  - Show a tooltip "Select exactly 2 SBOMs to compare" when fewer or more than 2 are selected
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate` hook
- The selection state should be local component state (React `useState`), cleared on pagination or filter changes.
- Do not use React Query mutations for selection -- this is purely client-side state.
- Per CONVENTIONS.md (Key Conventions) -- Component library: all UI components use PatternFly 5 equivalents. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's component scope.
- Per CONVENTIONS.md (Key Conventions) -- Routing: React Router v6 for navigation. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's routing scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer. Per SS5: changes must be scoped to files listed in Files to Modify.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- existing page being modified; study current table configuration and toolbar layout
- `src/components/FilterToolbar.tsx` -- existing toolbar component pattern for adding the Compare button alongside filters

## Acceptance Criteria
- [ ] SBOM table rows have checkbox selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Button tooltip shows "Select exactly 2 SBOMs to compare" when disabled
- [ ] Button navigates to `/sbom/compare?left={id1}&right={id2}` with correct SBOM IDs
- [ ] Selection state clears on pagination change
- [ ] Selection state clears on filter change
- [ ] Existing SBOM list functionality (filtering, sorting, pagination) is not affected

## Test Requirements
- [ ] Test that checkbox selection works on table rows
- [ ] Test that "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Test that "Compare selected" button is enabled with exactly 2 selections
- [ ] Test navigation to comparison page with correct URL parameters
- [ ] Test that existing list page functionality is unaffected (regression test)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
