# Impact Map: TC-9003 — SBOM Comparison View

## Workflow Mode

**Feature-branch** — cross-repo atomicity required. The frontend comparison page depends on the backend comparison endpoint; neither side functions independently. All intermediate tasks target branch `TC-9003`.

## trustify-backend

### New Files
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparison response struct and sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — Diff computation logic: loads packages and advisories for two SBOMs via SeaORM, computes set differences
- `modules/fundamental/src/sbom/endpoints/compare.rs` — GET /api/v2/sbom/compare handler: extracts `left`/`right` query params, delegates to compare service, returns JSON

### Modified Files
- `modules/fundamental/src/sbom/model/mod.rs` — re-export comparison module
- `modules/fundamental/src/sbom/service/mod.rs` — re-export compare module
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register `/compare` route
- `tests/api/sbom.rs` — add integration tests for comparison endpoint

### API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns structured diff with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## trustify-ui

### New Files
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping compareSboms() client function
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, Export dropdown
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable expandable section with count badge and data table
- `src/pages/SbomComparePage/components/PackageDiffTable.tsx` — table for added/removed packages
- `src/pages/SbomComparePage/components/VersionChangeTable.tsx` — table for version changes
- `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` — table for new/resolved vulnerabilities with SeverityBadge and critical row highlighting
- `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` — table for license changes
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response fixture
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for comparison flow

### Modified Files
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add compareSboms() client function
- `src/routes.tsx` — add /sbom/compare route with lazy loading
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection and "Compare selected" navigation button
- `tests/mocks/handlers.ts` — add MSW handler for GET /api/v2/sbom/compare
