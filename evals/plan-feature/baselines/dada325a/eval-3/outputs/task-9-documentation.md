# Task 9 — Document the SBOM comparison endpoint and comparison UI

**Summary:** Document the SBOM comparison API endpoint and comparison UI workflow
**Epic:** TC-9003: Delivery and documentation

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Write the documentation for feature TC-9003 (SBOM comparison view).

**What changed:** a new `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint returns a structured diff between two SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. A new frontend page at `/sbom/compare` shows the diff side by side, with collapsible sections, highlighted critical vulnerabilities, URL-shareable state, and JSON/CSV export. Users reach it from the SBOM list page by selecting two SBOMs and clicking "Compare selected".

**Doc impact type:** New Content.

**Details from Documentation Considerations:**
- Document the comparison endpoint and the comparison UI.
- User purpose: API consumers need an endpoint reference; UI users need a guide to the comparison workflow (select → compare → share URL → export).
- Reference material: the existing SBOM detail page documentation and the package/advisory data model docs.

The project registry has no dedicated documentation repository, so this task is assigned to trustify-backend, which owns the API reference. If the product's user documentation lives elsewhere, publish the UI workflow guide there and link to it from here.

Feature issue: TC-9003.

## Acceptance Criteria
- [ ] The endpoint reference documents `GET /api/v2/sbom/compare`: the `left`/`right` query params, the full response schema for all six diff categories, error codes (400 for missing params, 404 for an unknown SBOM), and the unpaginated response
- [ ] The UI guide documents the workflow: selecting two SBOMs on the list page, "Compare selected", reading each diff section, the critical-vulnerability highlight, sharing the comparison URL, and exporting JSON/CSV
- [ ] The docs state that both SBOMs should belong to the same product for a meaningful comparison
- [ ] The docs link to the existing SBOM detail page and package/advisory data model documentation

## Test Requirements
- [ ] Verify that the documented request/response examples match the actual output of the implemented endpoint
- [ ] Verify that the UI guide steps match the implemented UI (labels "Compare selected", "Compare", "Export JSON", "Export CSV", and the section titles)
- [ ] Verify that all links resolve

## Dependencies
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states
- Depends on: Task 6 — Render the six collapsible diff sections with virtualization and critical highlighting
- Depends on: Task 7 — Add "Compare selected" multi-select to the SBOM list page
- Depends on: Task 8 — Export comparison as JSON or CSV
