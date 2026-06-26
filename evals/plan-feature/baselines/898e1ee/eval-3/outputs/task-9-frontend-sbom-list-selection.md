## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enhance the existing SBOM list page to support selecting two SBOMs for comparison. Add checkboxes to the SBOM table rows and a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL query parameters. This implements the UC-1 workflow where users select SBOMs from the list page.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes (PatternFly `Table` select variant) and a "Compare selected" toolbar action button

## Implementation Notes
Modify the existing SBOM list table in `src/pages/SbomListPage/SbomListPage.tsx` to support row selection using PatternFly's composable `Table` with checkboxes.

**Selection State**:
Use React `useState` to track selected SBOM IDs as a `Set<string>`. Limit selection to a maximum of 2 SBOMs — when 2 are already selected, disable additional checkboxes.

**Compare Button**:
Add a "Compare selected" PatternFly `Button` to the toolbar area (alongside existing filters from `FilterToolbar`). The button should:
- Be disabled when fewer than 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
- Use PatternFly `Button` variant "primary"

**Visual Design** (per Figma design context, UC-1 workflow):
- Checkboxes appear as the first column in the SBOM table per PatternFly `Table` selectable rows pattern
- When exactly 2 SBOMs are selected, the "Compare selected" button becomes enabled with a primary style to draw attention
- A PatternFly `Badge` next to the button shows the count of selected SBOMs (e.g., "2 selected")

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar to extend
- `src/components/FilterToolbar.tsx` — toolbar pattern for adding the compare button alongside filters
- `src/routes.tsx` — route path constant for the comparison page

## Acceptance Criteria
- [ ] SBOM list table rows have selection checkboxes
- [ ] Maximum of 2 SBOMs can be selected at once
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection count badge displays next to the compare button

## Test Requirements
- [ ] Unit test: checkboxes render in table rows
- [ ] Unit test: selecting more than 2 SBOMs is prevented
- [ ] Unit test: Compare button is disabled with <2 selections
- [ ] Unit test: Compare button navigates to correct URL with selected SBOM IDs

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run SbomListPage` — component tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 8 — Frontend comparison page (route must exist)

[sdlc-workflow] Description digest: sha256-md:1a5936cd311495541306a6d84edf910c99d51d9a1072a14b895c1ccc7ebd0f31
