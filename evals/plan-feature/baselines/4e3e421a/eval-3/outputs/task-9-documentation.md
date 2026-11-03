# Task 9 — Document SBOM comparison endpoint and UI workflow

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Write documentation for the SBOM comparison feature delivered under TC-9003 (SBOM comparison view).

**What changed:**
- A new backend endpoint, `GET /api/v2/sbom/compare?left={id1}&right={id2}`, returns a structured diff between two SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.
- A new frontend comparison page at `/sbom/compare` shows a side-by-side layout with collapsible sections per diff category, highlights new critical vulnerabilities, and stores both SBOM IDs in a shareable URL.
- The SBOM list page has a "Compare selected" action.
- The comparison page offers JSON/CSV export.

**Doc impact type:** New Content.

**Details from the Documentation Considerations section:**
- **Audience and purpose**: API consumers need an endpoint reference, and UI users need a guide to the comparison workflow.
- **Reference material**: the existing SBOM detail page documentation and the package/advisory data model docs.
- **Scope**: document the comparison endpoint and the comparison UI.
  - Endpoint: parameters, response fields, and 400/404 errors.
  - UI workflow: select two SBOMs from the list (UC-1), read each diff section, share a comparison URL (UC-2), and export JSON/CSV.

Reference: Feature TC-9003.

## Acceptance Criteria
- [ ] The documentation accurately describes `GET /api/v2/sbom/compare`: the `left`/`right` query params, all six response categories with their fields, and the 400/404 error behavior
- [ ] The documentation includes a user guide for the comparison workflow: selecting two SBOMs on the list page, the "Compare selected" action, the meaning of each diff section, critical-vulnerability highlighting, and the empty/loading/error states
- [ ] The documentation explains that comparison URLs can be shared and bookmarked
- [ ] The documentation covers JSON and CSV export, including the CSV column layout
- [ ] The new content is linked from or consistent with the existing SBOM detail page and package/advisory data model documentation

## Test Requirements
- [ ] Verify every documented endpoint field and error code against the implemented backend response (Task 3)
- [ ] Walk through the documented UI steps against the implemented UI (Tasks 6–8) and confirm every step, label, and section name matches
- [ ] Confirm the documentation is complete with respect to the Documentation Considerations scope (endpoint reference + UI guide) and has no broken links

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 6 — Add SBOM comparison page at /sbom/compare
- Depends on: Task 7 — Add multi-select and "Compare selected" to SBOM list page
- Depends on: Task 8 — Add JSON/CSV export to SBOM comparison page (non-MVP)
