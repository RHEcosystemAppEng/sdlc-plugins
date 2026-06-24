# Impact Map: TC-9003 — SBOM Comparison View

## Overview

This feature adds a side-by-side SBOM comparison view, requiring a new backend diffing endpoint in trustify-backend and a dedicated comparison UI in trustify-ui. Users select two SBOMs and see structured diffs across packages, vulnerabilities, and licenses.

## Workflow Mode

**Feature-branch mode**: The frontend comparison page depends on the new backend endpoint. All intermediate work targets the `TC-9003` feature branch, with bookend tasks to create and merge the branch.

---

## trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Structs for SBOM comparison result: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` |
| `modules/fundamental/src/sbom/service/compare.rs` | `SbomService::compare()` — loads two SBOMs, computes diff across packages, advisories, and licenses |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | `GET /api/v2/sbom/compare?left={id}&right={id}` handler |
| `tests/api/sbom_compare.rs` | Integration tests for the comparison endpoint |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod comparison;` declaration |
| `modules/fundamental/src/sbom/service/mod.rs` | Add `pub mod compare;` declaration |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register `/compare` route in the SBOM endpoint router |
| `modules/fundamental/src/sbom/mod.rs` | Re-export comparison types if needed |
| `tests/api/sbom.rs` | Import shared test helpers used by comparison tests (or reference from new test file) |

---

## trustify-ui

### New Files

| File | Purpose |
|---|---|
| `src/api/models/sbom-comparison.ts` | TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` |
| `src/hooks/useSbomComparison.ts` | React Query hook wrapping `GET /api/v2/sbom/compare` |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Main comparison page component with header toolbar and diff sections |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Unit tests for the comparison page |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Reusable collapsible diff section (PatternFly `ExpandableSection` + `Table`) |
| `src/pages/SbomComparePage/components/CompareToolbar.tsx` | Header toolbar with SBOM selectors, Compare button, Export dropdown |
| `tests/mocks/fixtures/sbom-comparison.json` | Mock comparison response data for MSW handlers |

### Modified Files

| File | Change |
|---|---|
| `src/api/rest.ts` | Add `fetchSbomComparison(leftId, rightId)` function |
| `src/routes.tsx` | Add route `/sbom/compare` mapped to `SbomComparePage` |
| `src/pages/SbomListPage/SbomListPage.tsx` | Add checkbox selection and "Compare selected" button to enable comparison workflow |
| `tests/mocks/handlers.ts` | Add MSW handler for `GET /api/v2/sbom/compare` |

---

## Dependency Flow

```
Task 1 (create branch)
  -> Task 2 (backend model + service)
    -> Task 3 (backend endpoint + tests)
      -> Task 4 (frontend API types + client)
        -> Task 5 (frontend hook)
          -> Task 6 (frontend comparison page)
            -> Task 7 (frontend routing + list page integration)
              -> Task 8 (merge branch)
```

Backend tasks (2-3) must complete before frontend API-layer tasks (4-5), which must complete before UI tasks (6-7).
