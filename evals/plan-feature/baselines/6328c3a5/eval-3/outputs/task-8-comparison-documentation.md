## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature, including the new backend comparison endpoint (`GET /api/v2/sbom/compare`) and the frontend comparison UI workflow. The Feature description indicates "New Content" documentation impact: API consumers need an endpoint reference, and UI users need a guide for the comparison workflow.

**Doc impact type:** New Content

**Documentation scope:**
- API endpoint reference for `GET /api/v2/sbom/compare` with request parameters, response shape, and error codes
- UI user guide covering: selecting SBOMs for comparison, reading the diff view, understanding each diff section, sharing comparison URLs, and exporting results
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

**Feature reference:** TC-9003 — SBOM Comparison View

## Acceptance Criteria
- [ ] API endpoint documentation covers request format (`left` and `right` query parameters), response shape (six diff categories), and error responses (400, 404)
- [ ] UI documentation covers the end-to-end comparison workflow: selecting SBOMs, interpreting diff sections, and sharing URLs
- [ ] Documentation references existing SBOM and advisory data model documentation
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation examples match the actual endpoint behavior
- [ ] Verify UI workflow documentation steps match the actual comparison page UI
- [ ] Verify all response field names in documentation match the API response shape

## Dependencies
- Depends on: Task 2 — Implement SBOM comparison service and model
- Depends on: Task 3 — Create SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add SBOM comparison API client, types, and React Query hook
- Depends on: Task 5 — Create SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM comparison selection to SBOM list page
- Depends on: Task 7 — Add export functionality for SBOM comparison diff
