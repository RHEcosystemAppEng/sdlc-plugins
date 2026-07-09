## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison feature, covering both the backend REST API endpoint and the frontend comparison UI workflow. The feature's Documentation Considerations section specifies this as "New Content" -- new documentation pages or sections are needed for both the API endpoint reference and a user guide for the comparison workflow.

**Doc impact type**: New Content

**Details**:
- API consumers need an endpoint reference for `GET /api/v2/sbom/compare?left={id1}&right={id2}` including request parameters, response shape, error codes, and performance characteristics
- UI users need a guide for the comparison workflow: selecting SBOMs, interpreting the diff sections, sharing comparison URLs, and exporting results
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers request parameters (left, right), response body shape, HTTP status codes (200, 400, 404), and performance constraints (p95 < 1s for SBOMs up to 2000 packages)
- [ ] User guide documents the comparison workflow: navigating to the comparison page, selecting SBOMs, interpreting each diff section, sharing URLs, and exporting results
- [ ] Documentation references the feature issue TC-9003 for traceability
- [ ] Documentation is consistent with the implemented behavior of the comparison endpoint and UI

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (parameters, response shape, error codes)
- [ ] Verify user guide accurately describes the UI workflow including all six diff sections
- [ ] Verify exported file format descriptions match the actual export output

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison diff model and service
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 -- Add SBOM comparison API types and data-fetching hook
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add export functionality for comparison results
- Depends on: Task 7 -- Add tests for SBOM comparison page
