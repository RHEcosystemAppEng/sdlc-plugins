# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. The backend change is a new additive `GET` endpoint that does not break any existing functionality. The frontend change is a new page and route. Each repository's changes can land independently on `main` without leaving the codebase in a broken state. The backend endpoint can be deployed first (additive, no consumers affected), and the frontend page can follow once the endpoint is available. No coordinated schema migrations, no breaking API changes, no cross-cutting refactors.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison model structs for the diff response (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add comparison service method in SbomService to compute on-the-fly diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint handler with left/right query parameters
    - Register the compare route in the sbom endpoints module
    - Add integration tests for the comparison endpoint in tests/api/sbom.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response in api/models.ts
    - Add compareSboms() API client function in api/rest.ts
    - Add useSbomComparison React Query hook in hooks/
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
    - Add route registration for /sbom/compare in routes.tsx
    - Add unit tests for SbomComparePage with MSW mocking
    - Add MSW handler and fixture data for the comparison endpoint
```
