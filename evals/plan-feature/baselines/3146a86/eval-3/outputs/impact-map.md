# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison model structs (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) to `modules/fundamental/src/sbom/model/`
- Add SBOM comparison service logic (`compare` method on `SbomService`) to `modules/fundamental/src/sbom/service/`
- Add comparison endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` to `modules/fundamental/src/sbom/endpoints/`
- Add integration tests for the comparison endpoint to `tests/api/`

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response to `src/api/models.ts`
- Add API client function `compareSboms(leftId, rightId)` to `src/api/rest.ts`
- Add React Query hook `useSbomComparison` to `src/hooks/`
- Add `SbomComparePage` page component with header toolbar (SBOM selectors, Compare button, Export dropdown), collapsible diff sections, empty state, and loading state to `src/pages/SbomComparePage/`
- Add page-specific components: `DiffSection`, `AddedPackagesTable`, `RemovedPackagesTable`, `VersionChangesTable`, `NewVulnerabilitiesTable`, `ResolvedVulnerabilitiesTable`, `LicenseChangesTable` to `src/pages/SbomComparePage/components/`
- Add route `/sbom/compare` to `src/routes.tsx`
- Add SBOM selection checkboxes and "Compare selected" button to the existing `SbomListPage`
- Add unit tests for the comparison page and components
- Add MSW mock handlers and fixtures for the comparison endpoint

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page depends on the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Merging the frontend to main without the backend endpoint would result in a broken comparison page. Additionally, the SbomListPage changes (selection checkboxes, "Compare selected" button) navigate to the comparison page, creating a further dependency. Both repositories must deliver their changes together for the feature to function.

**Interdependent tasks:**
- Backend comparison endpoint task must be complete before the frontend can make real API calls
- Frontend comparison page and SbomListPage selection changes depend on the comparison endpoint existing
