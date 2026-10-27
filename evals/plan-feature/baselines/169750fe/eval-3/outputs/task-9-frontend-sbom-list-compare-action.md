## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Modify the SBOM list page to add checkbox selection for SBOMs and a "Compare selected" action button. When two SBOMs are selected and the user clicks "Compare selected", navigate to `/sbom/compare?left={id1}&right={id2}`. This provides the primary entry point for users to initiate comparisons from the existing SBOM list.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox column to SBOM table, add "Compare selected" toolbar action button

## Implementation Notes
Modify the existing SBOM list page to add multi-select capability:

1. Add a checkbox column to the existing SBOM table using PatternFly `Table` select functionality. Use PatternFly's built-in row selection with `onSelect` handler per the Figma design — users select exactly two SBOMs via checkboxes.

2. Add a "Compare selected" button to the page toolbar. The button should:
   - Be disabled when fewer than 2 or more than 2 SBOMs are selected
   - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`

3. Track selected SBOM IDs in component state (`useState<string[]>`)

Reference the existing table implementation in `src/pages/SbomListPage/SbomListPage.tsx` for the current table structure and toolbar layout. Reference `src/components/FilterToolbar.tsx` for toolbar action button placement patterns.

Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript React component scope.

Per CONVENTIONS.md §Routing: React Router v6 for navigation.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript route file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page being modified
- `src/components/FilterToolbar.tsx` — existing toolbar component for action button placement patterns

## Acceptance Criteria
- [ ] SBOM table includes a checkbox column for row selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than 2 or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selected state is visually indicated in the table rows
- [ ] Existing SBOM list functionality (filtering, pagination, sorting) is not broken

## Test Requirements
- [ ] Component test: checkbox selection tracks selected SBOM IDs
- [ ] Component test: "Compare selected" button is disabled with <2 or >2 selections
- [ ] Component test: button click navigates to correct comparison URL
- [ ] Regression: existing SBOM list page tests continue to pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Frontend comparison page
