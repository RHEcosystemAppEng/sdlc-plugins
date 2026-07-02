# Repository Impact Map — TC-9003: SBOM Comparison View

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison result model types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) in modules/fundamental/src/sbom/model/
    - Add comparison service logic to compute structured diff between two SBOMs by querying existing package, advisory, and license data in modules/fundamental/src/sbom/service/
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint handler with route registration in modules/fundamental/src/sbom/endpoints/
    - Add integration tests for the comparison endpoint in tests/api/

trustify-ui:
  changes:
    - Add TypeScript interfaces for SBOM comparison API response types in src/api/models.ts
    - Add fetchSbomComparison() API client function in src/api/rest.ts
    - Add useSbomComparison React Query hook in src/hooks/
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections using PatternFly ExpandableSection, Badge, Table, Select, EmptyState, and Skeleton components in src/pages/SbomComparePage/
    - Register /sbom/compare route in src/routes.tsx and add "Compare selected" checkbox action to SbomListPage
    - Add unit tests, MSW mock handlers, and test fixtures for the comparison page
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** -- Not present. The feature requirement explicitly states "No new database tables -- compute diff on-the-fly from existing package and advisory data." No schema changes are needed.
2. **Breaking API changes** -- Not present. The backend adds a new endpoint (`GET /api/v2/sbom/compare`); it does not modify any existing endpoints. Existing API contracts are unchanged.
3. **Cross-cutting refactors** -- Not present. No existing code structure is being reorganized. The feature adds new modules and components alongside existing ones.
4. **Tightly coupled feature components** -- Not present in the single-repo sense. While the frontend comparison page requires the backend endpoint, these are in separate repositories. The backend endpoint can be merged and deployed first (it is purely additive), and the frontend PRs can be merged afterward. Cross-repo coordination is handled through task dependency ordering (backend tasks have lower numbers), not through feature branches.

All tasks target `main`.

## Task Summary

| Task | Repository | Summary |
|---|---|---|
| 1 | trustify-backend | Add SBOM comparison model and service |
| 2 | trustify-backend | Add SBOM comparison endpoint and integration tests |
| 3 | trustify-ui | Add API types, client function, and hook for SBOM comparison |
| 4 | trustify-ui | Add SBOM comparison page with diff sections |
| 5 | trustify-ui | Add route registration, list page integration, and tests |

## Inherited Fields

- **Priority:** Critical (propagated from Feature TC-9003 to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (propagated from Feature TC-9003 to all tasks)
