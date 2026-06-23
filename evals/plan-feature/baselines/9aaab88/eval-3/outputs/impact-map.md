# Impact Map: TC-9003 — SBOM Comparison View

## Workflow Mode Decision

**Mode**: feature-branch
**Label**: workflow:feature-branch

**Rationale**: This feature requires tightly coupled changes across two repositories (trustify-backend and trustify-ui). The frontend comparison UI depends on the new backend `GET /api/v2/sbom/compare` endpoint. Deploying the frontend without the backend would result in a broken comparison page. Feature-branch mode ensures all changes are coordinated and merged atomically.

## Changes by Repository

### trustify-backend

1. **New comparison diff models** — Create `SbomComparisonDiff` response struct with sub-structs for added/removed packages, version changes, new/resolved vulnerabilities, and license changes. Located in `modules/fundamental/src/sbom/model/`.

2. **New comparison service method** — Add `compare(left_id, right_id)` method to `SbomService` that loads both SBOMs' package lists and advisory associations, computes the diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes), and returns the `SbomComparisonDiff` struct. Located in `modules/fundamental/src/sbom/service/`.

3. **New comparison endpoint** — Register `GET /api/v2/sbom/compare?left={id1}&right={id2}` in the SBOM endpoints module. The handler validates both IDs, calls the comparison service, and returns the JSON diff response. Located in `modules/fundamental/src/sbom/endpoints/`.

4. **Integration tests** — Add integration tests for the comparison endpoint covering: valid comparison, missing SBOM ID, identical SBOMs, and large diff performance. Located in `tests/api/`.

### trustify-ui

1. **API layer additions** — Add TypeScript interfaces for the comparison response (`SbomComparisonDiff`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) to `src/api/models.ts`. Add `fetchSbomComparison(leftId, rightId)` function to `src/api/rest.ts`. Add `useSbomComparison` React Query hook to `src/hooks/`.

2. **Comparison page and components** — Create `src/pages/SbomComparePage/` with the main `SbomComparePage.tsx` and page-specific components: `DiffSection.tsx` (reusable expandable section with count badge and data table), `CompareToolbar.tsx` (header with SBOM selectors, Compare button, Export dropdown). Uses PatternFly `ExpandableSection`, `Select`, `Badge`, `Table`, `EmptyState`, and `Dropdown` components per Figma design context.

3. **Route registration and SBOM list page integration** — Add `/sbom/compare` route to `src/routes.tsx`. Add selection checkboxes and "Compare selected" button to the existing `SbomListPage` to enable users to select two SBOMs and navigate to the comparison view.

4. **Tests** — Unit tests for the comparison page components using Vitest + React Testing Library. MSW handler for the comparison endpoint in `tests/mocks/handlers.ts`. Mock fixture for comparison response in `tests/mocks/fixtures/`.

## Cross-Repository Dependencies

- Frontend API types and client function (Task 4) depend on backend endpoint (Task 3) being defined and merged to the feature branch
- Frontend comparison page (Task 5) depends on frontend API layer (Task 4)
- Frontend SBOM list page integration (Task 6) depends on comparison page (Task 5) existing to navigate to
