# Task 8 -- SBOM list selection with compare action

## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox selection to the existing SBOM list page and a "Compare selected" toolbar action that navigates to the comparison page with the two selected SBOMs pre-populated as query parameters. This provides a natural entry point for the comparison workflow directly from the SBOM list, per the Figma design.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add row checkbox selection using PatternFly Table's select variant, add "Compare selected" action button to the toolbar that is enabled when exactly 2 SBOMs are selected, and navigate to /sbom/compare?left={id1}&right={id2} on click

## Implementation Notes
- **PatternFly components (per Figma design)**: Use `Table` composable select variant for row checkboxes, `Button` (secondary) for the "Compare selected" action in the toolbar, `Badge` to show the count of selected items.
- **SeverityBadge**: The existing component from `src/components/SeverityBadge.tsx` may be present in the SBOM list for advisory severity display.
- **Selection state**: Use React state to track selected SBOM IDs. The "Compare selected" button should be disabled unless exactly 2 SBOMs are selected. Show a Badge with the selection count.
- **Navigation**: Use React Router's `useNavigate` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` when the Compare button is clicked.
- **Empty state**: Use PatternFly EmptyState with CodeBranchIcon if the list page has no SBOMs (existing behavior, not new).
- **Loading state**: Skeleton loading is handled by existing list page infrastructure.
- Follow the existing toolbar action pattern in `src/components/FilterToolbar.tsx` for toolbar button placement.
- Per CONVENTIONS.md Component naming: use PascalCase for all component files. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` scope.

## Acceptance Criteria
- [ ] Each row in the SBOM list has a checkbox for selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] "Compare selected" button is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to /sbom/compare?left={id1}&right={id2}
- [ ] Selection state is cleared when navigating away and returning
- [ ] Existing SBOM list functionality (filtering, sorting, pagination) is not broken

## Test Requirements
- [ ] Unit test: checkboxes render on each SBOM list row
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL

## Verification Commands
- `npx vitest run src/pages/SbomListPage` -- all SBOM list page tests pass
- `npx tsc --noEmit` -- no TypeScript compilation errors

## Dependencies
- Depends on: Task 6 -- SBOM comparison page component (comparison page must exist to navigate to)
