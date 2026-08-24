## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the new SBOM comparison feature covering both the backend API endpoint and the frontend comparison UI workflow. The Feature description's Documentation Considerations indicate New Content is needed.

**Doc impact type:** New Content

**Scope from Documentation Considerations:**
- API consumers need an endpoint reference for `GET /api/v2/sbom/compare` (request parameters, response shape, error codes)
- UI users need a guide for the comparison workflow (selecting SBOMs from the list, interpreting diff sections, sharing comparison URLs)
- Reference existing SBOM detail page documentation and package/advisory data model docs

**Reference:** Feature TC-9003 — SBOM comparison view

## Acceptance Criteria
- [ ] API endpoint reference for `GET /api/v2/sbom/compare` is documented with request parameters (`left`, `right`), response shape (all six diff categories), and error responses (400, 404)
- [ ] UI comparison workflow is documented: selecting two SBOMs from the list, clicking "Compare selected", interpreting the six diff sections, sharing comparison URLs via query params
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in Documentation Considerations (API reference and UI workflow guide)

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented API endpoint behavior
- [ ] Verify documentation covers both API consumer and UI user perspectives
- [ ] Verify all six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes) are described

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service
- Depends on: Task 3 — Add SBOM comparison endpoint with integration tests
- Depends on: Task 4 — Add SBOM comparison API types and React Query hook
- Depends on: Task 5 — Create SBOM comparison page with diff sections
- Depends on: Task 6 — Add multi-select and compare action to SBOM list page
