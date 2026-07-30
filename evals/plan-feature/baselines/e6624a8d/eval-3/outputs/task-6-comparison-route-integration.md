## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the SBOM comparison page route in the application router and add a "Compare selected" entry point on the SBOM list page. Users will select two SBOMs via checkboxes on the list page and click a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/routes.tsx` -- add route definition for `/sbom/compare` pointing to `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection column and "Compare selected" toolbar button

## Implementation Notes
Per CONVENTIONS.md PatternFly 5: use PatternFly components for the checkbox column and toolbar button on the SBOM list page.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md Naming conventions: PascalCase for components, camelCase for hooks, kebab-case for directories.
Applies: convention has no file-type restriction (broadly applicable).

**Figma design -- SBOM List Page integration:**
Per UC-1 in the feature description:
1. User navigates to the SBOM list page
2. User selects two SBOMs using checkboxes
3. User clicks "Compare selected"
4. Navigation to `/sbom/compare?left={id1}&right={id2}`

**Route registration** (reference `src/routes.tsx`):
- Add a lazy-loaded route for `/sbom/compare` that imports `SbomComparePage`
- Place the comparison route BEFORE the SBOM detail route (`/sbom/:id`) to prevent route conflicts (React Router v6 matches in order)

**SBOM List Page modifications:**
- Add a checkbox selection column to the existing SBOM table using PatternFly `Table` composable row select pattern
- Track selected SBOM IDs in component state (max 2 selections)
- Add a "Compare selected" `Button` to the list page toolbar (PatternFly `Toolbar` area)
- Button is disabled until exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`

## Reuse Candidates
- `src/routes.tsx` -- existing route definitions; follow the same lazy-loading pattern for the comparison page route
- `src/pages/SbomListPage/SbomListPage.tsx` -- existing list page; add checkbox column and toolbar button to the existing table and toolbar structure
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar button placement patterns

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered and renders `SbomComparePage`
- [ ] SBOM list page has checkbox selection column for each row
- [ ] "Compare selected" button appears in the list page toolbar
- [ ] Button is disabled until exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Comparison route does not conflict with SBOM detail route (`/sbom/:id`)

## Test Requirements
- [ ] Unit test: comparison route renders SbomComparePage component
- [ ] Unit test: SBOM list page renders checkbox column
- [ ] Unit test: "Compare selected" button is disabled with fewer or more than 2 selections
- [ ] Unit test: clicking "Compare selected" with 2 selections navigates to the correct URL
- [ ] E2E test: user flow from SBOM list through selection to comparison page renders correctly

## Verification Commands
- `npx vitest run SbomListPage` -- runs SBOM list page unit tests
- `npx playwright test sbom-list` -- runs E2E tests for the SBOM list page flow

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
