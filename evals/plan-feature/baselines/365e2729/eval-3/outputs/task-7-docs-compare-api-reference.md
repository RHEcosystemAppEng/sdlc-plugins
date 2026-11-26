## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison endpoint for API consumers (TC-9003).

- **What changed:** a new endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns a structured diff between two SBOMs: added packages, removed packages, version changes (with upgrade/downgrade direction), new vulnerabilities, resolved vulnerabilities and license changes. The diff is computed on-the-fly from existing package and advisory data.
- **Doc impact type:** New Content — document the comparison endpoint (this task) and the comparison UI (Task 8, trustify-ui).
- **User purpose:** API consumers need an endpoint reference (parameters, response schema, error codes 400/404, performance expectations for SBOMs up to 2000 packages).
- **Reference material:** existing SBOM detail page documentation, package/advisory data model docs.
- Feature reference: TC-9003 (SBOM comparison view).

## Acceptance Criteria
- [ ] The endpoint reference documents path, query parameters, full response schema for all six diff categories, and 400/404 error responses
- [ ] The documented field names and `direction` values match the implemented response exactly
- [ ] The documentation links to or is consistent with the existing SBOM and package/advisory data model docs
- [ ] A worked request/response example is included

## Test Requirements
- [ ] Execute the documented example request against a running backend and confirm the response matches the documented schema
- [ ] Review that every field in `modules/fundamental/src/sbom/model/compare.rs` is documented and no undocumented fields are returned

## Dependencies
- Depends on: Task 1 — Add SBOM comparison diff model and service
- Depends on: Task 2 — Add GET /api/v2/sbom/compare endpoint
