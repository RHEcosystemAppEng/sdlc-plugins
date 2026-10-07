## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature, covering both the backend REST API endpoint and the frontend comparison UI.

**Doc impact type:** New Content

**Documentation scope** (from Feature TC-9003 Documentation Considerations):
- API consumers need endpoint reference for `GET /api/v2/sbom/compare?left={id1}&right={id2}`, including request parameters, response shape, error codes, and performance characteristics
- UI users need a workflow guide for the comparison feature: selecting SBOMs, reading the diff view, using the export functionality, and sharing comparison URLs
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers request parameters (`left`, `right`), response shape (all six diff categories), error responses (400, 404), and performance notes (p95 < 1s for up to 2000 packages)
- [ ] UI documentation describes the comparison workflow: selecting SBOMs from the list page, reading diff sections, exporting results, and sharing URLs
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (parameters, response shape, error codes)
- [ ] Verify UI documentation accurately describes the comparison page layout and workflow

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections and export
- Depends on: Task 6 — Add SBOM selection and compare navigation to list page
