## Repository
trustify-ui

## Target Branch
main

## Description
Register the `/sbom/compare` route in React Router and integrate the comparison workflow into the existing SBOM list page. Users select two SBOMs from the list using checkboxes, click a "Compare selected" button, and navigate to the comparison page with both SBOM IDs encoded in the URL. The URL format `/sbom/compare?left={id1}&right={id2}` enables shareable, bookmarkable comparison links per the feature requirements (TC-9003).

**Figma design context (from figma-context.md):**
- SBOM selectors on the comparison page are pre-populated from URL query params `left` and `right`
- URL encodes both SBOM IDs for bookmarking and sharing (UC-2: Share comparison with compliance team)

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded SbomComparePage component
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table, add "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`, disable button until exactly two SBOMs are selected

## Implementation Notes
- Follow the existing routing pattern in `src/routes.tsx`: add a lazy-loaded route for `/sbom/compare` using React.lazy() and Suspense. The route must be registered BEFORE any `/sbom/:id` route to avoid path conflicts (React Router v6 matches routes in definition order, and `compare` could be mistaken for an `:id` parameter).
- For SBOM list checkbox selection: add a selection column to the SBOM table using PatternFly Table's built-in row selection support. Track selected SBOM IDs with React `useState<string[]>([])`.
- The "Compare selected" button should be added to the SBOM list page's toolbar area (alongside existing filters). Use PatternFly `Button` with `variant="primary"`. Disable the button when `selectedIds.length !== 2`.
- Navigation: use React Router's `useNavigate` hook to navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` when the Compare button is clicked.
- The comparison page (Task 4) reads `left` and `right` from `useSearchParams()` to pre-populate the selectors and optionally auto-trigger the comparison.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route file scope.
- Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions showing the React.lazy() + Suspense lazy-loading pattern
- `src/components/FilterToolbar.tsx` — existing reusable toolbar component; reference for toolbar button placement and PatternFly toolbar layout
- `src/pages/SbomListPage/SbomListPage.tsx` — current SBOM list page with PatternFly Table; add selection column to existing table structure

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered in the router and loads the SbomComparePage component
- [ ] SBOM list page shows a checkbox selection column in the SBOM table
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the selected SBOM IDs
- [ ] Comparison page reads URL query params and pre-populates the SBOM selectors
- [ ] Sharing the comparison URL loads the page with the same SBOM selections (URL-shareable comparison)
- [ ] Route is lazy-loaded (code-split from the main bundle)

## Test Requirements
- [ ] Unit test: SbomListPage renders a checkbox selection column in the table
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 SBOM selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 SBOM selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs as query parameters
- [ ] Unit test: route configuration maps `/sbom/compare` to SbomComparePage
- [ ] E2E test: user selects two SBOMs from the list, clicks Compare, sees the comparison page with results

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run src/pages/SbomListPage` — SBOM list page tests pass with new selection behavior

## Dependencies
- Depends on: Task 4 — Implement SBOM comparison page with diff sections and export
