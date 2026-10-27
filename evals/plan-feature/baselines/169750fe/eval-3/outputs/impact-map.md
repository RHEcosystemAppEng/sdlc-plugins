# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The feature exhibits tightly coupled feature components — the new frontend comparison page (`/sbom/compare`) requires the new backend endpoint (`GET /api/v2/sbom/compare`) to function. Merging either side independently would leave `main` in a broken state. Additionally, the frontend SBOM list page modification (adding selection checkboxes and "Compare selected" button) depends on the comparison page existing. These are atomicity indicators that mandate coordinated delivery via a feature branch.

**Interdependent tasks:**
- The backend comparison endpoint (Task 4) must exist before the frontend API client (Task 6) can call it
- The frontend comparison page (Task 7) renders data from the backend comparison endpoint
- The SBOM list page compare action (Task 8) navigates to the comparison page with selected SBOM IDs

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

## Impact Map

trustify-backend:
  changes:
    - Add SbomComparison model struct with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add SbomComparisonService with diff computation logic operating on existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint accepting left and right SBOM ID query parameters
    - Add integration tests for the comparison endpoint covering normal diff, identical SBOMs, and missing SBOM error cases

trustify-ui:
  changes:
    - Add TypeScript interfaces for SbomComparison response type and API client function for the comparison endpoint
    - Add SbomComparePage component with PatternFly ExpandableSection diff sections, Select dropdowns, and EmptyState
    - Add route definition for /sbom/compare with query parameter support
    - Modify SbomListPage to add checkbox selection and "Compare selected" action button
    - Add MSW handlers and component tests for the comparison page
    - Add React Query hook for the comparison endpoint

## Excluded Requirements

- **Export diff as JSON or CSV** — marked as non-MVP in the feature requirements. Can be planned as a follow-up feature once the core comparison view is delivered.

## Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks | Rationale |
|---|---|---|---|
| Priority | Critical | Yes | Feature has a defined priority (not "Undefined") |
| Fix Versions | RHTPA 1.5.0 | Yes | Feature has non-empty fixVersions; fixVersion scope defaults to "both" (no Jira Field Defaults section in CLAUDE.md) |

## Task-to-Epic Assignment

No level-1 issue type (Epic) discovery was performed in this eval context. Tasks are created directly under the Feature (Feature → Task hierarchy).

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Document the comparison endpoint and comparison UI; API consumers need endpoint reference; UI users need a guide for the comparison workflow
- A documentation task will be generated (Task 10).
