## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the compare workflow entry point to the SBOM list page. Users select two SBOMs using checkboxes in the existing SBOM list table and click a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`. This completes the end-to-end comparison workflow described in UC-1 of the feature specification.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- add row selection checkboxes and "Compare selected" toolbar action
- `tests/mocks/handlers.ts` -- add or update MSW handlers if needed for comparison flow testing

## Files to Create
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- update or create tests for the compare selection workflow (if the existing test file needs a new test file for the compare functionality)

## Implementation Notes
- **Selection state**: Use React `useState` to track selected SBOM IDs (max 2). Use PatternFly `Table` row selection with `isSelected` and `onSelect` props.
- **Selection constraint**: Allow exactly two selections. When two SBOMs are already selected and the user clicks a third, either deselect the oldest selection or show a PatternFly `Alert` indicating the maximum selection of two.
- **Compare button**: Add a "Compare selected" `Button` to the existing toolbar area of `SbomListPage`. The button is disabled when fewer than 2 SBOMs are selected. On click, use React Router's `useNavigate` to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`.
- Per CONVENTIONS.md §Component Library: use PatternFly 5 table selection props (`isSelected`, `onSelect`) and PatternFly `Button` for the compare action. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Naming: use camelCase for state variables and handler functions (e.g., `selectedSbomIds`, `handleSbomSelect`). Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's naming scope.
- Reference the existing `SbomListPage.tsx` for toolbar patterns, table configuration, and PatternFly component usage.
- Use `useNavigate` from React Router v6 for programmatic navigation, consistent with the routing convention.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- existing list page with table and toolbar; extend with selection state
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar action placement

## Acceptance Criteria
- [ ] SBOM list page displays row selection checkboxes
- [ ] Users can select exactly two SBOMs using checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] The comparison page loads with both SBOMs pre-populated from the URL parameters

## Test Requirements
- [ ] Unit test: checkboxes appear in the SBOM list table rows
- [ ] Unit test: "Compare selected" button is disabled with fewer than 2 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Verification Commands
- `npx vitest run src/pages/SbomListPage` -- list page unit tests pass
- `npx tsc --noEmit` -- TypeScript compilation succeeds

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Add SBOM comparison page with header toolbar and diff sections
