## Repository
trustify-ui

## Target Branch
main

## Description
Document the SBOM comparison workflow for UI users (TC-9003).

- **What changed:** users can select two SBOMs on the SBOM list page and click "Compare selected", or open `/sbom/compare` directly, to see a side-by-side diff organized into six collapsible sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes). New vulnerabilities with Critical severity are highlighted. The comparison URL encodes both SBOM IDs and can be bookmarked or shared. Results can be exported as JSON or CSV.
- **Doc impact type:** New Content — document the comparison UI (this task) and the comparison endpoint (Task 7, trustify-backend).
- **User purpose:** UI users (security analysts, compliance officers) need a guide for the comparison workflow, including sharing a comparison URL (UC-2) and exporting a diff for compliance documentation.
- **Reference material:** existing SBOM detail page documentation.
- Feature reference: TC-9003 (SBOM comparison view).

## Acceptance Criteria
- [ ] The guide covers both entry points (list page selection and direct URL)
- [ ] The guide explains each of the six diff sections and the critical-vulnerability highlight
- [ ] The guide explains URL sharing and JSON/CSV export
- [ ] Screenshots or descriptions match the implemented UI

## Test Requirements
- [ ] Walk through the documented workflow in a running UI and confirm every step and label matches
- [ ] Confirm a shared URL from the guide's example loads the comparison directly

## Dependencies
- Depends on: Task 4 — Build SBOM comparison page at /sbom/compare
- Depends on: Task 5 — Add "Compare selected" to the SBOM list page
- Depends on: Task 6 — Implement JSON/CSV export of the comparison
