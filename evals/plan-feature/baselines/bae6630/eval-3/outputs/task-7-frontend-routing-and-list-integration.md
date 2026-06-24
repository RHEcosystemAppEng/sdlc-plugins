# Task 7 — Frontend route registration and SBOM list page comparison integration

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route to render the new comparison page, and update the SBOM list page to support selecting two SBOMs and navigating to the comparison view. This connects the comparison feature into the existing application navigation flow.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` that lazy-loads `SbomComparePage` from `src/pages/SbomComparePage/SbomComparePage.tsx`
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection to the SBOM list table rows. Add a "Compare selected" PatternFly `Button` (variant="secondary") to the page toolbar, enabled only when exactly two SBOMs are selected. On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router `useNavigate`.

## Implementation Notes
- **Figma: SBOM List Integration** — The "Compare selected" button sits in the existing toolbar area of `SbomListPage`. Use a PatternFly `Button` with `variant="secondary"`. The button is disabled unless exactly two checkboxes are checked. Checkbox selection uses PatternFly `Table` built-in row selection (composable `Td` with `select` prop).
- Follow the existing route registration pattern in `src/routes.tsx` — use `React.lazy()` for code splitting the comparison page.
- The route should be placed before the `/sbom/:id` route to avoid path conflicts (React Router matches in order).
- Use `useNavigate` from React Router v6 to programmatically navigate to the comparison URL with query parameters.
- The existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` should remain functional alongside the new selection + compare button.

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered in `src/routes.tsx` and renders `SbomComparePage`
- [ ] Route is lazy-loaded for code splitting
- [ ] SBOM list page shows checkbox selection on each table row
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Existing SBOM list functionality (filtering, pagination) is not broken

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with zero selections
- [ ] Unit test: "Compare selected" button is disabled with one selection
- [ ] Unit test: "Compare selected" button is enabled with exactly two selections
- [ ] Unit test: clicking the button navigates to the correct comparison URL
- [ ] Unit test: route `/sbom/compare` renders the comparison page component
- [ ] Existing SbomListPage tests continue to pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 6 — Frontend SBOM comparison page with Figma-based UI

## Digest
[sdlc-workflow] Description digest: sha256-md:48fdcce242a35eef9e9a279ced5c6451d8571646748e20bbc147f538c728cd87
