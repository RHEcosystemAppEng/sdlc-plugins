## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the `/sbom/compare` route to the application router, wire up URL query parameter support for shareable comparison links (`?left={id1}&right={id2}`), and add a "Compare selected" action to the SbomListPage that allows users to select two SBOMs via checkboxes and navigate to the comparison view.

## Files to Modify
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to SbomComparePage (lazy-loaded)
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection for two SBOMs and "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
- **Route registration** in `src/routes.tsx`:
  - Follow the existing lazy-loading pattern (React Router v6 with `React.lazy` or equivalent).
  - Add the route for `/sbom/compare` before `/sbom/:id` to prevent route parameter conflicts.
  - The route renders `SbomComparePage` from Task 7.
- **URL query parameter support** in `SbomComparePage`:
  - Use `useSearchParams()` from React Router to read `left` and `right` query params on page load.
  - Pre-populate the SBOM selectors from query params if present.
  - When the Compare button is clicked, update the URL query params using `setSearchParams()` so the URL is always shareable.
  - This enables UC-2 (share comparison with compliance team) — opening a URL with `?left=X&right=Y` loads and triggers the comparison automatically.
- **SBOM selection on list page** in `SbomListPage.tsx`:
  - Add a PatternFly checkbox column to the existing SBOM table for row selection.
  - Limit selection to exactly two SBOMs — disable additional checkboxes once two are selected.
  - Add a "Compare selected" toolbar action button (PatternFly `Button`, variant `secondary`) that is disabled until exactly two SBOMs are selected.
  - On click, navigate to `/sbom/compare?left={selectedId1}&right={selectedId2}` using `useNavigate()`.
- Follow the existing routing pattern in `src/routes.tsx` and navigation patterns in existing pages.

**Figma design reference:**
- The SBOM selectors in the comparison page are PatternFly `Select` (single, typeahead) — pre-populate from URL params `left` and `right`.
- Empty state renders when page loads without query params (handled in Task 7).

## Reuse Candidates
- `src/routes.tsx` — existing route definitions showing lazy-loading pattern and route ordering
- `src/pages/SbomListPage/SbomListPage.tsx` — existing page with table that will be extended with selection
- `src/App.tsx` — root component showing router setup

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered and renders SbomComparePage
- [ ] URL `?left={id1}&right={id2}` query params pre-populate the SBOM selectors and trigger comparison
- [ ] Clicking Compare updates the URL with current selector values
- [ ] SbomListPage has checkbox selection limited to two SBOMs
- [ ] "Compare selected" button appears in SbomListPage toolbar and navigates to comparison view
- [ ] "Compare selected" button is disabled until exactly two SBOMs are selected

## Test Requirements
- [ ] Unit test: route renders SbomComparePage for path `/sbom/compare`
- [ ] Unit test: SBOM selectors pre-populate from URL query params
- [ ] Unit test: "Compare selected" button is disabled when fewer or more than two SBOMs are selected
- [ ] E2E test: select two SBOMs on list page, click "Compare selected", verify comparison page loads with correct URL params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 7 — Add comparison page with diff sections UI

## Description Digest
sha256-md:903b355c496f3bc5dae4aaca575151b8604c3db381f3646532f6c8124ddf4caf
