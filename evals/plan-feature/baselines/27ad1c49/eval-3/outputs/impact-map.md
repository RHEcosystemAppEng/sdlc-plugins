# Repository Impact Map — TC-9003: SBOM comparison view

## Inherited Field Values

The following field values propagate from the feature (TC-9003) to all child tasks:

| Field | Value |
|---|---|
| Priority | Critical |
| Fix Versions | RHTPA 1.5.0 |

All tasks created for TC-9003 inherit these values unless explicitly overridden.

## trustify-backend

### Impacted Areas

| Module / Path | Impact | Notes |
|---|---|---|
| `modules/fundamental/src/sbom/model/` | New file | Add comparison result model types: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange |
| `modules/fundamental/src/sbom/service/` | New file | Add comparison diff computation service |
| `modules/fundamental/src/sbom/endpoints/` | New file + Modify | Add GET /api/v2/sbom/compare endpoint; register route in mod.rs |
| `modules/fundamental/Cargo.toml` | Potential modify | Add dependencies if needed |
| `tests/api/` | New file | Integration tests for comparison endpoint |

### Existing Reuse Points

- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM data and associated packages
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — model struct pattern reference
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — model struct pattern reference
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories for vulnerability correlation
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field for vulnerability diff
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package data
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field for license change detection
- `common/src/error.rs::AppError` — error handling enum, implements IntoResponse
- `common/src/db/query.rs` — shared query builder helpers
- `entity/src/sbom_package.rs` — SBOM-Package join table for package resolution
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for advisory correlation
- `entity/src/package_license.rs` — Package-License mapping for license change detection

## trustify-ui

### Impacted Areas

| Module / Path | Impact | Notes |
|---|---|---|
| `src/api/models.ts` | Modify | Add TypeScript interfaces for comparison response types |
| `src/api/rest.ts` | Modify | Add fetchSbomComparison() client function |
| `src/hooks/` | New file | Add useSbomComparison React Query hook |
| `src/pages/SbomComparePage/` | New directory | Comparison page component with toolbar and diff sections |
| `src/pages/SbomListPage/SbomListPage.tsx` | Modify | Add selection checkboxes and "Compare selected" action |
| `src/routes.tsx` | Modify | Add /sbom/compare route |

### Existing Reuse Points

- `src/hooks/useSboms.ts` — SBOM list hook for selector dropdowns
- `src/hooks/useSbomById.ts` — React Query hook pattern with ID parameter
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/components/SeverityBadge.tsx` — severity display in vulnerability sections
- `src/components/EmptyStateCard.tsx` — empty state pattern
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/FilterToolbar.tsx` — toolbar pattern for action placement
- `src/utils/severityUtils.ts` — severity ordering and color mapping
