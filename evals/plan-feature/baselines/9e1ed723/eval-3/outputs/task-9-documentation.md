# Task 9 — Document the SBOM comparison endpoint and comparison UI workflow

**Summary:** Document the SBOM comparison API endpoint and comparison UI workflow
**Epic:** TC-9003: Delivery and documentation
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Feature TC-9003 (SBOM comparison view) adds a new backend endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that returns a structured diff between two SBOMs (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes), and a new frontend comparison page at `/sbom/compare` with side-by-side SBOM selectors, collapsible diff sections, highlighting of new critical vulnerabilities, URL-shareable comparisons, and JSON/CSV export.

**Doc impact type:** New Content — document the comparison endpoint and the comparison UI.

**Details from Documentation Considerations:**
- User purpose: API consumers need an endpoint reference; UI users need a guide for the comparison workflow (select two SBOMs on the SBOM list → "Compare selected", or use the selectors on `/sbom/compare`; share the URL with others).
- Reference material: existing SBOM detail page documentation and the package/advisory data model docs.

The endpoint reference should cover query parameters, the response schema, error responses (`400` for missing parameters, `404` for unknown SBOM IDs), and the computed-on-the-fly behavior (vulnerability sections reflect current advisory correlation). The UI guide should cover both entry points, how to read each diff section, critical-vulnerability highlighting, sharing comparison URLs, and exporting results.

Reference: TC-9003.

## Acceptance Criteria
- [ ] Documentation for `GET /api/v2/sbom/compare` accurately describes parameters, response fields for all six diff sections, and error responses as implemented
- [ ] A user guide describes the comparison workflow from the SBOM list page and from `/sbom/compare`, including URL sharing and JSON/CSV export
- [ ] Documentation links to or builds on the existing SBOM detail page and package/advisory data model documentation
- [ ] Content covers the full scope identified in the Documentation Considerations section (endpoint reference + UI guide)

## Test Requirements
- [ ] Verify every documented request/response example against the implemented endpoint (field names, status codes)
- [ ] Walk through the documented UI workflow against the implemented UI and confirm each step matches
- [ ] Review that the documentation is complete and consistent with the implemented feature behavior (no undocumented sections, no stale field names)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states
- Depends on: Task 6 — Render collapsible diff sections with tables, critical highlighting, and virtualization
- Depends on: Task 7 — Add "Compare selected" action to the SBOM list page
- Depends on: Task 8 — Export comparison result as JSON or CSV
