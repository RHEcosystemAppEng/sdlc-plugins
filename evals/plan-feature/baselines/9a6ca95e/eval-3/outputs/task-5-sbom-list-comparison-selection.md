## Repository

trustify-ui

## Target Branch

main

## Priority

Critical

## Fix Versions

RHTPA 1.5.0

## Description

Add SBOM selection and comparison navigation to the existing SBOM list page. Users can select exactly two SBOMs from the list using checkboxes and click a "Compare selected" toolbar action to navigate to the comparison page with the selected SBOM IDs encoded in the URL. The selection state is managed locally within the page component. The "Compare selected" button is disabled unless exactly two SBOMs are checked, and a helper text below the button indicates how many are selected.

## Acceptance Criteria

- [ ] Each row in the SBOM list table has a checkbox for selection
- [ ] A "Compare selected" button appears in the page toolbar
- [ ] The "Compare selected" button is disabled unless exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` using React Router navigation
- [ ] Selection state persists across pagination within the same page session
- [ ] A helper text shows the count of selected SBOMs (e.g., "2 of 2 selected")
- [ ] Selecting more than two SBOMs is allowed but the compare button remains disabled with a tooltip explaining "Select exactly 2 SBOMs to compare"

## Test Requirements

- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: "Compare selected" button is disabled with zero or one selection
- [ ] Unit test: "Compare selected" button is enabled with exactly two selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL
- [ ] Unit test: selecting three SBOMs disables the compare button

## Dependencies

- Task 4 (sbom-comparison-page) -- the target page that the navigation routes to

## Figma Design Context

- **Row checkboxes**: Standard PatternFly `Table` row selection checkboxes
- **Toolbar action**: "Compare selected" as a PatternFly `Button` (secondary variant) in the toolbar alongside existing filter controls
- **Selection feedback**: Helper text below the button or in the toolbar showing selection count

## Files to Modify

- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection, "Compare selected" button, and navigation logic

## Implementation Notes

- Use PatternFly composable `Table` row selection (checkbox select) pattern, following the existing table implementation in `src/pages/SbomListPage/SbomListPage.tsx`.
- Add the "Compare selected" button to the existing `FilterToolbar` area from `src/components/FilterToolbar.tsx` or as an adjacent toolbar item.
- Use React Router `useNavigate` hook for programmatic navigation to the comparison page.
- Store selection state using React `useState` with a `Set<string>` of SBOM IDs.
- Use PatternFly `Tooltip` on the disabled compare button to explain the "exactly 2" requirement.

## Conventions

- **Component library**: PatternFly 5 -- all UI components use PF5 equivalents. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's component library scope.
- **State management**: React Query for server state; local React state for UI state. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's state management scope.
