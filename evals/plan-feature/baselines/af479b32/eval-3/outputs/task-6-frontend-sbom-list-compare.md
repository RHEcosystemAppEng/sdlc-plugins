## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Modify the existing SBOM list page to enable users to select two SBOMs for comparison. Add checkbox selection to the SBOM table rows and a "Compare selected" action button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected. This implements Use Case UC-1 from the feature description, where a security analyst selects two SBOMs from the list and initiates a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox column to the SBOM table, track selected rows, add "Compare selected" toolbar action button
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- add tests for selection and compare navigation behavior

## Implementation Notes

Per CONVENTIONS.md §Component Library: use PatternFly 5 components for the table checkboxes and toolbar action. See `src/pages/SbomListPage/SbomListPage.tsx` for the existing table and toolbar patterns.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Naming: use camelCase for state variables (e.g., `selectedSbomIds`) and event handlers (e.g., `handleCompareClick`).
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

**Selection behavior:**
1. Add a checkbox column as the first column in the SBOM table using PatternFly's `Td` with `select` prop.
2. Track selected SBOM IDs in component state (`useState<string[]>`).
3. Add a "Compare selected" button to the page toolbar. The button should:
   - Be disabled when fewer than 2 or more than 2 SBOMs are selected
   - Show a count indicator (e.g., "Compare selected (2)")
   - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
4. Optionally show a helper text when 1 SBOM is selected: "Select one more SBOM to compare"

**Navigation:** Use React Router's `useNavigate()` hook to programmatically navigate to the comparison page with query parameters. Do not use `window.location` for client-side navigation.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- the existing list page; extend its table and toolbar rather than creating a parallel component
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar action button placement patterns

## Acceptance Criteria
- [ ] SBOM table rows have checkboxes for selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" with exactly 2 SBOMs selected navigates to /sbom/compare?left={id1}&right={id2}
- [ ] Selection state is managed correctly (select, deselect, clear)
- [ ] Existing SBOM list page functionality (filtering, pagination, sorting) is not broken

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM table
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting one or three SBOMs keeps the button disabled
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs
- [ ] Unit test: deselecting an SBOM updates the selection state correctly
- [ ] Unit test: existing table functionality (sorting, filtering) still works with checkboxes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Create SBOM comparison page (the navigation target must exist)
