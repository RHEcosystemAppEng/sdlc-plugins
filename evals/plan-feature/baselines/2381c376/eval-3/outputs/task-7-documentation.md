## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature's Documentation Considerations indicate a doc impact type of **New Content**: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting the diff, exporting results).

The documentation should cover:
- The comparison endpoint: path, query parameters, response shape, error codes
- The comparison UI: how to select SBOMs from the list page, how to read the diff sections, how to share a comparison URL, how to export results
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

See Feature TC-9003 for full requirements and Documentation Considerations.

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with request parameters, response shape, and error codes
- [ ] UI workflow documentation covers the end-to-end comparison flow: selecting SBOMs, comparing, interpreting results
- [ ] Documentation explains URL-shareable comparisons
- [ ] Documentation covers the export feature (JSON and CSV)
- [ ] Documentation is consistent with the implemented behavior of the comparison endpoint and UI

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (path, parameters, response shape)
- [ ] Verify UI workflow documentation matches the actual comparison page behavior
- [ ] Verify all documented features are accurate and complete

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add comparison endpoint and integration tests
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM selection on list page and route wiring
