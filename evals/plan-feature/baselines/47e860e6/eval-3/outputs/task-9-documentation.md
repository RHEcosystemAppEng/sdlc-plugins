# Task 9 — Documentation: SBOM comparison endpoint and UI guide

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the SBOM comparison capability delivered by Feature TC-9003 (SBOM comparison view).

**What changed:** a new `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint returns a structured diff between two SBOMs. The diff covers added packages, removed packages, version changes (with upgrade/downgrade direction), new vulnerabilities, resolved vulnerabilities and license changes, all computed on the fly from existing package and advisory data. A new frontend comparison page at `/sbom/compare` provides side-by-side SBOM selectors and collapsible diff sections, with critical new vulnerabilities highlighted. The URL is shareable (it encodes both SBOM IDs), and a "Compare selected" action is available on the SBOM list page. The UI also offers JSON/CSV export of the diff (non-MVP; document it if Task 8 ships).

**Doc impact type:** New Content

**Details from Documentation Considerations:**
- Document the comparison endpoint and the comparison UI
- User purpose: API consumers need an endpoint reference (params, response shape, error codes 400/404); UI users need a guide to the comparison workflow (select two SBOMs on the list page, then Compare selected; or use the selectors on `/sbom/compare`; share the URL with others)
- Reference material: existing SBOM detail page documentation, and the package/advisory data model docs

Note: no dedicated documentation repository is in the Repository Registry, so this task targets `trustify-backend` (the API reference). Redirect it to the product documentation repository if the docs live elsewhere (open question 5 in the impact map).

Reference: Feature TC-9003.

## Acceptance Criteria
- [ ] The API reference documents `GET /api/v2/sbom/compare`, including the `left`/`right` query params, the full response shape for all six categories, and the `400`/`404` error responses
- [ ] The user guide describes the comparison workflow (UC-1: compare from the list page; UC-2: share a comparison URL), including the six diff sections and the critical-vulnerability highlight
- [ ] Documentation states that both SBOMs should come from the same product for a meaningful comparison
- [ ] Documentation matches the implemented behavior (field names, section names, route `/sbom/compare`)
- [ ] Export (JSON/CSV) is documented only if Task 8 has been delivered

## Test Requirements
- [ ] Check the documented request and response examples against a real call to the implemented endpoint; field names and error codes must match
- [ ] Follow the UI guide step by step against the implemented comparison page and confirm every step and label matches
- [ ] Confirm all internal links to the existing SBOM detail and data model docs resolve

## Dependencies
- Depends on: Task 2 — Backend: SBOM comparison model and diff service
- Depends on: Task 3 — Backend: GET /api/v2/sbom/compare endpoint and integration tests
- Depends on: Task 4 — Frontend: comparison API types, client function, React Query hook and mocks
- Depends on: Task 5 — Frontend: comparison diff section components
- Depends on: Task 6 — Frontend: SBOM comparison page and /sbom/compare route
- Depends on: Task 7 — Frontend: multi-select and "Compare selected" on SBOM list page
- Depends on: Task 8 — Frontend: export comparison as JSON / CSV (non-MVP)
