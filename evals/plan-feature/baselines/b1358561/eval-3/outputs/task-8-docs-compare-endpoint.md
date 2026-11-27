# Task 8 — Document the SBOM comparison endpoint

**Summary:** TC-9003: Document GET /api/v2/sbom/compare endpoint
**Issue type:** Task
**Parent (Epic):** Epic 4 — TC-9003: Documentation
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Feature TC-9003 ("SBOM comparison view") adds a new backend endpoint,
`GET /api/v2/sbom/compare?left={id1}&right={id2}`, that returns a structured diff between two
SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved
vulnerabilities and license changes, computed on-the-fly from existing package and advisory data.

**Doc impact type:** New Content — document the comparison endpoint.

From the Feature's Documentation Considerations:
- **User purpose:** API consumers need an endpoint reference.
- **Reference material:** existing SBOM detail page documentation and package/advisory data model docs.

The documentation should cover the request parameters, the response shape and the meaning of
each diff category, error responses (400 missing parameter, 404 unknown SBOM), the recommendation
that both SBOMs belong to the same product, and expected performance limits (SBOMs up to ~2000
packages each). The UI guide is covered by Task 9 (trustify-ui), because each task targets a
single repository.

Reference: TC-9003.

## Acceptance Criteria
- [ ] Documentation describes `GET /api/v2/sbom/compare` with both query parameters and an example request/response
- [ ] Each of the six diff categories is defined consistently with the implemented behavior (e.g. same-name/different-version packages appear only under version changes)
- [ ] Error responses (400, 404) are documented
- [ ] Same-product recommendation and size/performance guidance are included
- [ ] Documentation is consistent with existing SBOM and package/advisory data model docs

## Test Requirements
- [ ] Verify the documented example request returns a response matching the documented shape against a running instance
- [ ] Verify documented field names match the implemented `SbomComparison` serialization
- [ ] Peer review confirms the documentation is accurate and complete relative to the Documentation Considerations scope

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and diff service
- Depends on: Task 2 — Add GET /api/v2/sbom/compare endpoint
