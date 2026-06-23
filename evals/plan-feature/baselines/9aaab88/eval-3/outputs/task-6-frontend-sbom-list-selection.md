## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add SBOM selection checkboxes and a "Compare selected" button to the existing SBOM list page, enabling users to select two SBOMs and navigate to the comparison view. This completes the user workflow from UC-1: users select two SBOMs from the list, click "Compare selected", and are navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add selection checkboxes to the SBOM table and a "Compare selected" toolbar action button

## Files to Create
- `src/pages/SbomListPage/SbomListPage.test.tsx` — update existing tests (or add new tests) for the comparison selection behavior

## Implementation Notes
Add row selection to the existing SBOM table in `src/pages/SbomListPage/SbomListPage.tsx`:
- Use PatternFly `Table` row selection (checkbox type) to allow selecting exactly two SBOMs.
- Add a "Compare selected" button to the page toolbar (alongside existing filter controls from `src/components/FilterToolbar.tsx`). The button should be disabled until exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router `useNavigate`.

Follow the existing page structure — `SbomListPage.tsx` already uses PatternFly `Table` for displaying SBOMs. The selection state can be managed with React `useState` tracking selected row IDs.

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.test.tsx` matching the convention's `.tsx` test file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page to extend with selection
- `src/components/FilterToolbar.tsx` — existing toolbar pattern to follow for adding the Compare button

## Acceptance Criteria
- [ ] SBOM list table shows selection checkboxes on each row
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared when navigating away and back

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with zero selections
- [ ] Unit test: "Compare selected" button is disabled with one selection
- [ ] Unit test: "Compare selected" button is enabled with exactly two selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Verification Commands
- `npx vitest run --reporter=verbose -- SbomListPage` — list page tests pass
- `npx tsc --noEmit` — TypeScript compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 5 — Frontend comparison page (navigation target must exist)

sha256-md:8bc527d5059edc60580ccb44590ebd344a06ce0b5c4df701b3c54e80c6ebfd84
