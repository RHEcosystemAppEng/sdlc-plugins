## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature: the new backend comparison endpoint (`GET /api/v2/sbom/compare`) and the frontend comparison UI workflow. The feature description's Documentation Considerations section indicates "New Content" is needed — API consumers need endpoint reference documentation, and UI users need a guide for the comparison workflow.

Doc impact type: **New Content**

This documentation should cover:
- The comparison endpoint's request parameters, response shape, and error codes
- The comparison UI workflow: selecting SBOMs, triggering comparison, reading results, sharing URLs, exporting data
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers GET /api/v2/sbom/compare with request parameters (left, right), response shape (SbomComparisonResult), and error codes (400, 404)
- [ ] UI workflow documentation describes how to select two SBOMs and compare them
- [ ] URL sharing workflow is documented (comparison URL encodes both SBOM IDs)
- [ ] Export functionality (JSON/CSV) is documented
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation is consistent with existing SBOM detail page documentation style

## Test Requirements
- [ ] Verify documentation accurately describes the comparison endpoint request/response format
- [ ] Verify documentation covers the complete comparison workflow (select, compare, review, share, export)
- [ ] Verify documentation is consistent with existing documentation style and structure

## Dependencies
- Depends on: Task 3 — Add SBOM comparison REST endpoint (backend must be finalized for API docs)
- Depends on: Task 7 — Add SBOM comparison route and SbomListPage integration (UI must be finalized for workflow docs)
