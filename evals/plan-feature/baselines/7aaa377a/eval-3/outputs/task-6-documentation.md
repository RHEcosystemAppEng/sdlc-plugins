# Task 6 — Document SBOM comparison endpoint and UI

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison feature for both API consumers and UI users. The Feature's Documentation Considerations indicate New Content is needed: the comparison endpoint needs API reference documentation, and the comparison UI needs a user guide for the comparison workflow.

Documentation scope (from Feature TC-9003 Documentation Considerations):
- **Doc impact type:** New Content
- **User purpose:** API consumers need endpoint reference; UI users need a guide for the comparison workflow
- **Reference material:** Existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API reference documentation for `GET /api/v2/sbom/compare?left={id1}&right={id2}` is complete, including request parameters, response shape, error codes, and example response
- [ ] User guide for the SBOM comparison workflow is complete, covering: selecting SBOMs from the list page, using the comparison view, interpreting diff sections, and sharing comparison URLs
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (request/response shapes, error codes)
- [ ] Verify user guide steps can be followed end-to-end against the running application
- [ ] Verify documentation is consistent with existing SBOM detail page documentation style

## Dependencies
- Depends on: Task 1 — Add SBOM comparison diff endpoint
- Depends on: Task 2 — Add comparison API types, client function, and React Query hook
- Depends on: Task 3 — Build SBOM comparison page with diff sections
- Depends on: Task 4 — Add SBOM selection and compare navigation on list page
- Depends on: Task 5 — Add export functionality for comparison results
