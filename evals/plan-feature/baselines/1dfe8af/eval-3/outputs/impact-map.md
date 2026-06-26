# Impact Map: TC-9003 SBOM Comparison View

## Overview

This feature adds a side-by-side SBOM comparison view spanning two repositories: a new backend diffing endpoint in `trustify-backend` and a comparison page UI in `trustify-ui`. The workflow uses a feature branch (`TC-9003`) to coordinate cross-repo changes.

## Repositories Impacted

| Repository | Impact | Tasks |
|---|---|---|
| trustify-backend | New comparison endpoint with model/service/endpoint layers | Tasks 2, 3 |
| trustify-ui | New comparison page, API layer additions, test infrastructure | Tasks 4, 5, 6 |

## Task Dependency Graph

```
Task 1: Create feature branch TC-9003
  |
  +---> Task 2: Backend - Comparison model and service
  |       |
  |       +---> Task 3: Backend - Comparison endpoint and tests
  |               |
  |               +---> Task 4: Frontend - API types, client, hook
  |                       |
  |                       +---> Task 5: Frontend - Comparison page UI
  |                               |
  |                               +---> Task 6: Frontend - Comparison tests
  |                                       |
  +-------+-------+-------+-------+-------+
  |
  v
Task 7: Merge feature branch TC-9003
```

## Backend Impact (trustify-backend)

### New Files
| File | Purpose | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Comparison result structs (SbomComparison, AddedPackage, etc.) | 2 |
| `modules/fundamental/src/sbom/service/compare.rs` | Comparison diffing logic | 2 |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | GET /api/v2/sbom/compare handler | 3 |
| `tests/api/sbom_compare.rs` | Integration tests for comparison endpoint | 3 |

### Modified Files
| File | Change | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add comparison module export | 2 |
| `modules/fundamental/src/sbom/service/mod.rs` | Add compare module export | 2 |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register comparison route | 3 |

### API Changes
| Endpoint | Method | Status | Description |
|---|---|---|---|
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | NEW | Returns structured diff between two SBOMs |

## Frontend Impact (trustify-ui)

### New Files
| File | Purpose | Task |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | React Query hook for comparison data | 4 |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Main comparison page component | 5 |
| `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` | Header toolbar with selectors | 5 |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Collapsible diff section | 5 |
| `src/pages/SbomComparePage/components/PackageDiffTable.tsx` | Package diff table | 5 |
| `src/pages/SbomComparePage/components/VulnerabilityDiffTable.tsx` | Vulnerability diff table | 5 |
| `src/pages/SbomComparePage/components/LicenseChangeTable.tsx` | License change table | 5 |
| `tests/mocks/fixtures/sbom-comparison.json` | Mock comparison data fixture | 6 |
| `tests/e2e/sbom-compare.spec.ts` | E2E tests for comparison workflow | 6 |

### Modified Files
| File | Change | Task |
|---|---|---|
| `src/api/models.ts` | Add SbomComparison and related TypeScript interfaces | 4 |
| `src/api/rest.ts` | Add fetchSbomComparison() client function | 4 |
| `src/routes.tsx` | Add /sbom/compare route entry | 5 |
| `src/pages/SbomListPage/SbomListPage.tsx` | Add multi-select and "Compare selected" button | 5 |
| `tests/mocks/handlers.ts` | Add MSW handler for comparison endpoint | 6 |

## Cross-Repository Dependencies

The frontend comparison page (Tasks 4-6) depends on the backend comparison endpoint (Tasks 2-3). Specifically:
- Frontend TypeScript interfaces in `src/api/models.ts` must match the backend `SbomComparison` struct serialization from `modules/fundamental/src/sbom/model/comparison.rs`
- Frontend API client function calls `GET /api/v2/sbom/compare` which must be available from the backend endpoint in `modules/fundamental/src/sbom/endpoints/compare.rs`

## Existing Code Reused

### Backend
- `SbomService` (fetch/list methods) for loading SBOM data
- `PackageService` for loading package lists per SBOM
- `AdvisoryService` for loading advisory associations
- `AppError` for consistent error handling
- SeaORM entities (`sbom_package`, `sbom_advisory`, `package_license`) for data access

### Frontend
- `SeverityBadge` component for vulnerability severity display
- `EmptyStateCard` component for initial empty state
- `useSboms` hook for SBOM list in selectors
- `severityUtils` for severity ordering and color mapping
- Existing PatternFly component patterns (Table, ExpandableSection, Select, Badge)

## Risk Areas

| Risk | Mitigation | Severity |
|---|---|---|
| Large SBOM comparison performance (>2000 packages) | Use HashMap-based O(n) diffing in backend; virtualized lists in frontend | Medium |
| Cross-repo API contract drift | TypeScript interfaces must exactly match Rust struct serialization; feature branch isolates changes | Low |
| Browser freezing on large diffs | Frontend uses virtualized rendering for >100 items per Figma spec | Medium |
