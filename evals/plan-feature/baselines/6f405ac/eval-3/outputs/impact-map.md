# Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

### New Files
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison response structs (SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — SbomService comparison logic: load two SBOMs, compute diff across packages, advisories, and licenses
- `modules/fundamental/src/sbom/endpoints/compare.rs` — GET /api/v2/sbom/compare endpoint handler

### Modified Files
- `modules/fundamental/src/sbom/model/mod.rs` — Re-export comparison model types
- `modules/fundamental/src/sbom/service/mod.rs` — Re-export comparison service function
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register comparison route

### New Test Files
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

### Modified Test Files
- `tests/api/mod.rs` or test runner config — Include new sbom_compare test module (if applicable)

## trustify-ui

### New Files
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with SBOM selectors, diff sections, and export functionality
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable expandable diff section component with count badge and data table
- `src/hooks/useSbomComparison.ts` — React Query hook for the comparison endpoint

### Modified Files
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — Add `compareSboms(leftId, rightId)` API client function
- `src/routes.tsx` — Add `/sbom/compare` route definition
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection and "Compare selected" button

### New Test Files
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests for comparison workflow

### Modified Test Files
- `tests/mocks/handlers.ts` — Add MSW handler for GET /api/v2/sbom/compare
