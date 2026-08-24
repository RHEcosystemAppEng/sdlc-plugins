## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox-based multi-selection to the SBOM list page and a "Compare selected" action button that navigates to the comparison view with the two selected SBOMs. This enables the comparison workflow from Use Case UC-1 where users select two SBOMs from the list and initiate a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table and a "Compare selected" toolbar action button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — add tests for multi-select and compare navigation behavior

## Implementation Notes
- Per CONVENTIONS.md §Component Library: use PatternFly 5 composable `Table` with `select` variant for checkbox selection. See `src/pages/SbomListPage/SbomListPage.tsx` for the existing table structure to extend.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TSX component file scope.
- **Figma design reference:** The comparison workflow starts on the SBOM list page where users select two SBOMs using checkboxes and click "Compare selected" (Use Case UC-1). Use a PatternFly `Button` (variant="primary") for the compare action in the toolbar area, disabled until exactly two SBOMs are selected.
- Track selected SBOM IDs in component state using `useState<string[]>`.
- When exactly 2 SBOMs are selected, enable the "Compare selected" button. When fewer or more than 2 are selected, keep it disabled.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router `useNavigate`.
- Add a helper text element (e.g., PatternFly `HelperText`) displaying "Select 2 SBOMs to compare" when the count is not exactly 2.
- Ensure existing SBOM list functionality (filtering, pagination, sorting) is not affected by the selection additions.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page component with table, modify in place to add selection
- `src/components/FilterToolbar.tsx` — existing toolbar component, reference for toolbar action button placement

## Acceptance Criteria
- [ ] SBOM list table has a checkbox selection column
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" with 2 selected SBOMs navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Existing SBOM list functionality (filtering, pagination, sorting) is not affected

## Test Requirements
- [ ] Test that checkbox selection toggles correctly on row click
- [ ] Test that "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Test that clicking "Compare selected" with exactly 2 selections navigates to the correct comparison URL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create SBOM comparison page with diff sections
