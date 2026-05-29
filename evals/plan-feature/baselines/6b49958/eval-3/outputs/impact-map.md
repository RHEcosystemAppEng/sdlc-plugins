# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) to the sbom model module
  - Add comparison service method to SbomService that computes a structured diff between two SBOMs by comparing their packages, advisories, and licenses
  - Add GET /api/v2/sbom/compare endpoint that accepts left and right SBOM ID query parameters and returns the structured diff
  - Register the new comparison endpoint route in the sbom endpoints module
  - Add integration tests for the comparison endpoint covering normal diff, identical SBOMs, and missing SBOM ID cases

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types in the API models module
  - Add API client function to call the comparison endpoint in the REST client module
  - Add React Query hook for the comparison API call
  - Create the SbomCompare page with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per the Figma design
  - Create page-specific components: DiffSection (expandable section with count badge and data table), CompareToolbar (SBOM selectors and action buttons)
  - Add route definition for /sbom/compare to the routes module
  - Add selection UI on the SBOM list page (checkboxes and "Compare selected" button) to navigate to the comparison page
  - Add unit tests for the comparison page and components, and E2E test for the comparison workflow

## Workflow Mode

**Mode**: `feature-branch`

**Rationale**: Atomicity indicator #4 (Tightly coupled feature components) is present — the frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not yet exist. Merging the frontend without the backend would result in a broken UI calling a non-existent endpoint. Atomicity indicator #2 (Breaking API changes) also applies — the frontend depends on a new API contract that must be available for the feature to function.

**Interdependent tasks**: All frontend implementation tasks depend on the backend comparison endpoint task. The backend must provide the API before the frontend can integrate against it.
