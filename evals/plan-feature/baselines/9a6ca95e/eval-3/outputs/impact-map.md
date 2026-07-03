# Impact Map: TC-9003 SBOM Comparison View

## trustify-backend

### New Files

| File | Task | Purpose |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Task 1 | `SbomComparisonResult` and supporting diff structs (`PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, `LicenseChangeEntry`) |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Task 2 | `GET /api/v2/sbom/compare` endpoint handler with query parameter extraction and validation |
| `tests/api/sbom_compare.rs` | Task 2 | Integration tests for the comparison endpoint against PostgreSQL test database |

### Modified Files

| File | Task | Change |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 1 | Add `pub mod comparison;` re-export for the new comparison model module |
| `modules/fundamental/src/sbom/service/sbom.rs` | Task 1 | Add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to `SbomService` |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 2 | Register `GET /api/v2/sbom/compare` route alongside existing SBOM routes |

### API Changes

| Method | Path | Task | Description |
|---|---|---|---|
| GET | `/api/v2/sbom/compare?left={id1}&right={id2}` | Task 2 | Returns structured diff between two SBOMs including added/removed packages, version changes, new/resolved vulnerabilities, and license changes |

---

## trustify-ui

### New Files

| File | Task | Purpose |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | Task 3 | React Query hook for fetching SBOM comparison results |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Task 4 | Main comparison page with header toolbar and diff sections |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Task 4 | Unit tests for the comparison page |
| `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` | Task 4 | Header toolbar with SBOM selectors, compare button, and export dropdown |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Task 4 | Reusable collapsible diff section with count badge and data table |

### Modified Files

| File | Task | Change |
|---|---|---|
| `src/api/models.ts` | Task 3 | Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, `LicenseChangeEntry` |
| `src/api/rest.ts` | Task 3 | Add `compareSboms(leftId: string, rightId: string)` API client function |
| `src/routes.tsx` | Task 4 | Add lazy-loaded route for `/sbom/compare` pointing to `SbomComparePage` |
| `src/pages/SbomListPage/SbomListPage.tsx` | Task 5 | Add checkbox selection, "Compare selected" toolbar button, and navigation to comparison page |

### Reused Existing Components

| Component | File | Used By |
|---|---|---|
| `SeverityBadge` | `src/components/SeverityBadge.tsx` | Task 4 -- severity display in vulnerability diff sections |
| `EmptyStateCard` | `src/components/EmptyStateCard.tsx` | Task 4 -- empty state when no comparison is active |
| `useSboms` | `src/hooks/useSboms.ts` | Task 4 -- populates SBOM selector dropdowns |
| `FilterToolbar` | `src/components/FilterToolbar.tsx` | Task 5 -- toolbar area for the compare button |
