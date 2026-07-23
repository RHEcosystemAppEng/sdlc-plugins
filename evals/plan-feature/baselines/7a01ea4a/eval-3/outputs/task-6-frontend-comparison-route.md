## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the `/sbom/compare` route to the application's route configuration and integrate a "Compare selected" workflow into the existing SBOM list page. Users will be able to select two SBOMs via checkboxes on the list page and click a "Compare selected" button that navigates to the comparison page with the selected SBOM IDs as URL query parameters.

## Files to Modify
- `src/routes.tsx` -- add lazy-loaded route for SbomComparePage at path /sbom/compare
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection column to the SBOM table and a "Compare selected" toolbar button

## Implementation Notes
- Follow the existing route definition pattern in `src/routes.tsx` using React Router v6 with lazy-loaded page components. Add the `/sbom/compare` route, ensuring it is defined before any parameterized SBOM routes (e.g., `/sbom/:id`) to avoid path conflicts.
- In `SbomListPage.tsx`:
  - Add a checkbox column to the SBOM table using PatternFly Table's built-in row selection support
  - Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`)
  - Add a "Compare selected" button to the page toolbar, disabled until exactly 2 SBOMs are selected
  - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
  - Show a count indicator (e.g., "2 selected") when SBOMs are selected
- The URL encodes both SBOM IDs for bookmarking and sharing per UC-2 (share comparison with compliance team).

## Reuse Candidates
- `src/routes.tsx` -- existing route definitions; follow the lazy-loading pattern for page components
- `src/pages/SbomListPage/SbomListPage.tsx` -- the page being modified; understand its current table setup and toolbar structure
- `src/components/FilterToolbar.tsx` -- existing toolbar component; reference for toolbar patterns in the SBOM list page

## Acceptance Criteria
- [ ] Route /sbom/compare is defined in routes.tsx and renders SbomComparePage
- [ ] SbomComparePage is lazy-loaded
- [ ] SBOM list page has checkbox selection on each row
- [ ] "Compare selected" button appears in the list page toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to /sbom/compare?left={id1}&right={id2}
- [ ] Navigation preserves selected SBOM IDs in URL query parameters

## Test Requirements
- [ ] Unit test: /sbom/compare route renders SbomComparePage component
- [ ] Unit test: SbomListPage renders checkbox column on each row
- [ ] Unit test: "Compare selected" button is disabled with 0 selections
- [ ] Unit test: "Compare selected" button is disabled with 1 selection
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both IDs

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 5 -- Frontend: Build SBOM comparison page with diff sections
