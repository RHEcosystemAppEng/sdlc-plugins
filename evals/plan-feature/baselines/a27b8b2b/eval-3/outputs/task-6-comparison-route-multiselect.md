# Task 6: Add comparison route and SbomListPage multi-select

**Summary**: Add /sbom/compare route and SBOM list multi-select

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router to render the SbomComparePage (Task 5). Update the SbomListPage to support selecting two SBOMs via checkboxes and provide a "Compare selected" action button that navigates to the comparison page with the selected SBOM IDs as URL query parameters. This enables the primary user workflow: select two SBOMs from the list, click Compare, and navigate to the side-by-side diff view.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to lazy-loaded SbomComparePage
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table for multi-select and a "Compare selected" action button in the toolbar

## Implementation Notes
- Follow the existing route registration pattern in `src/routes.tsx` — use React Router v6 lazy-loaded page components. Register the `/sbom/compare` route at the same level as existing SBOM routes.
- **Important**: register the `/sbom/compare` route before any `/sbom/:id` route to avoid React Router matching "compare" as an `:id` parameter.
- For SbomListPage multi-select:
  - Add a checkbox column as the first column in the SBOM table. Use PatternFly's `Table` selection pattern (row-level `onSelect` with `isSelected` state).
  - Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`).
  - Add a "Compare selected" button in the toolbar (next to existing actions). Disable the button unless exactly 2 SBOMs are selected.
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
- Reference `src/pages/SbomListPage/SbomListPage.tsx` for the existing toolbar and table structure.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions; follow the same lazy-loading pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page with table and filters; add selection functionality here
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar action button placement

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and renders SbomComparePage
- [ ] SbomListPage displays checkboxes in the first column of the SBOM table
- [ ] Users can select exactly two SBOMs using the checkboxes
- [ ] "Compare selected" button appears in the toolbar and is disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] The comparison page loads and auto-triggers comparison from the URL parameters

## Test Requirements
- [ ] Unit test: `/sbom/compare` route renders SbomComparePage component
- [ ] Unit test: SbomListPage renders checkboxes in the SBOM table
- [ ] Unit test: "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Unit test: "Compare selected" button navigates to the correct comparison URL with selected SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SbomComparePage with diff sections UI
