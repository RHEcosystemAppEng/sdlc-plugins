# Task 9 — Document the SBOM comparison endpoint and comparison UI

**Summary:** Document SBOM comparison API endpoint and comparison UI workflow
**Epic:** TC-9003: Documentation
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Write documentation for the SBOM comparison feature delivered by TC-9003.

**What changed:** users can now pick two SBOM versions and see a structured, side-by-side diff:

- added and removed packages
- version changes
- new and resolved vulnerabilities, with new critical vulnerabilities highlighted
- license changes

The diff is served by the new endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` and shown on the new UI page `/sbom/compare`. The comparison URL can be bookmarked and shared. The loaded diff can be exported as JSON or CSV.

**Doc impact type:** New Content.

**Details from the Documentation Considerations section of TC-9003:**
- Document the comparison endpoint and the comparison UI.
- User purpose: API consumers need an endpoint reference; UI users need a guide to the comparison workflow.
- Reference material: the existing SBOM detail page documentation and the package/advisory data model docs.

**Scope to cover:**
- **API reference:** request parameters, the response shape for all six diff categories, error codes (400, 404), and the "computed on the fly" note with the performance expectation for SBOMs of up to 2000 packages.
- **UI guide for UC-1:** select two SBOMs on the list page → Compare selected → read the sections.
- **UI guide for UC-2:** share the comparison URL.
- **Export:** JSON and CSV, if Task 8 ships.

**Repository choice:** no dedicated documentation repository is registered, so this task is placed in `trustify-ui`, alongside the user-facing guide. The API reference addition to `trustify-backend/README.md` is already covered by Task 3's Documentation Updates. This task should cross-link to it rather than duplicate it.

Feature reference: TC-9003.

## Acceptance Criteria
- [ ] The documentation describes `GET /api/v2/sbom/compare`: the `left` and `right` params, all six response categories with their fields, and the 400/404 behaviour, consistent with the implemented endpoint
- [ ] A user guide describes the comparison workflow from the SBOM list page (select two, Compare selected), the six diff sections, and the critical-vulnerability highlight
- [ ] The guide explains that the comparison URL is shareable and opens the same comparison directly
- [ ] The guide covers the JSON/CSV export if Task 8 is merged; otherwise it omits export
- [ ] The documentation links to or extends the existing SBOM detail page and package/advisory data model documentation

## Test Requirements
- [ ] Verify every documented field name and error code against the merged backend implementation (Task 2, Task 3)
- [ ] Walk through the documented UI steps against a running build and confirm that each step and label matches the UI (Task 5, Task 6, Task 7)
- [ ] Verify that the documented example URL `/sbom/compare?left=…&right=…` loads the comparison directly

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint with integration tests
- Depends on: Task 6 — Add six collapsible diff sections
- Depends on: Task 7 — Add "Compare selected" multi-select to SBOM list page
- Depends on: Task 8 — Add Export dropdown (JSON, CSV) to the SBOM comparison toolbar
