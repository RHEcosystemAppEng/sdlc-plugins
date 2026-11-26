# Task 8 — Document SBOM comparison endpoint and UI

**Summary:** Document the SBOM comparison endpoint and comparison UI workflow
**Issue type:** Task | **Parent (Epic):** Epic C — TC-9003: Compliance export and documentation
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Feature TC-9003 (SBOM comparison view) adds a side-by-side comparison of two SBOM versions: a new backend endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` returning a structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes), and a new UI page at `/sbom/compare` with collapsible diff sections, critical-vulnerability highlighting, URL-shareable comparisons, a "Compare selected" action on the SBOM list, and JSON/CSV export.

**Doc impact type:** New Content.

Details from the Documentation Considerations section:
- Document the comparison endpoint and the comparison UI.
- User purpose: API consumers need an endpoint reference; UI users need a guide for the comparison workflow (select two SBOMs → Compare selected → review sections → share URL / export).
- Reference material: existing SBOM detail page documentation and package/advisory data model docs.

Reference: Feature TC-9003. The endpoint reference also receives a README update in trustify-backend as part of Task 3; this task produces the user-facing guide and cross-links to the endpoint reference.

## Acceptance Criteria
- [ ] A user guide describes the comparison workflow: selecting two SBOMs on the list page, the comparison page sections, critical-vulnerability highlighting, sharing the URL, and exporting JSON/CSV
- [ ] The endpoint reference documents `GET /api/v2/sbom/compare` parameters (`left`, `right`), response fields for all six sections, and `400`/`404` errors (linked or included)
- [ ] Documentation is consistent with the existing SBOM detail page and package/advisory data model documentation

## Test Requirements
- [ ] Walk through the documented workflow against the implemented feature and confirm every step and screen label matches
- [ ] Verify documented response field names match the actual endpoint response
- [ ] Verify all links (endpoint reference, SBOM detail docs, data model docs) resolve

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Build SBOM comparison page at /sbom/compare
- Depends on: Task 6 — Add "Compare selected" action to SBOM list page
- Depends on: Task 7 — Export comparison as JSON or CSV
