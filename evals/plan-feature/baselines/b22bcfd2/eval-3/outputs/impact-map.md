# Impact Map: TC-9003 — SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view with a backend diffing endpoint and a frontend comparison UI built from Figma mockups. Priority: Critical. Fix Versions: RHTPA 1.5.0.

## Workflow Mode

**Feature-branch** (TC-9003) — This feature requires tightly coupled backend and frontend changes across two repositories. The backend comparison endpoint must exist before the frontend can integrate against it, and the feature should ship atomically to avoid partial user-facing functionality.

**Label decision**: Apply `workflow:feature-branch` to TC-9003.

## Field Propagation

- **Priority**: Critical — inherited from TC-9003, propagated to all tasks via `additional_fields.priority`.
- **Fix Versions**: RHTPA 1.5.0 — inherited from TC-9003, propagated to all tasks via `additional_fields.fixVersions` (fixVersion scope defaults to 'both' since no explicit scope configured in CLAUDE.md).

## Repositories

trustify-backend:
  changes:
    - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
    - Add comparison service method to SbomService that computes on-the-fly diff between two SBOMs by querying existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/
    - Add integration tests for the comparison endpoint in tests/api/sbom.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for comparison API response types in src/api/models.ts
    - Add API client function fetchSbomComparison() in src/api/rest.ts
    - Add React Query hook useSbomComparison() in src/hooks/
    - Create SbomComparePage with PatternFly Select dropdowns, ExpandableSection diff panels, Badge count indicators, Table composable for each diff section, EmptyState for initial load, and Skeleton loading states — all per Figma design context
    - Add route /sbom/compare in src/routes.tsx
    - Add SeverityBadge integration for vulnerability rows with critical row highlighting
    - Add unit tests with MSW mocks and E2E Playwright tests for the comparison flow
