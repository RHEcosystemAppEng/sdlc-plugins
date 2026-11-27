# Task 9 — Document the SBOM comparison UI workflow

**Summary:** TC-9003: Document the SBOM comparison UI workflow
**Issue type:** Task
**Parent (Epic):** Epic 4 — TC-9003: Documentation
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Feature TC-9003 ("SBOM comparison view") adds a comparison page at `/sbom/compare` where users
select two SBOMs (from the comparison page selectors or via "Compare selected" on the SBOM list)
and see collapsible sections for Added Packages, Removed Packages, Version Changes, New
Vulnerabilities (critical ones highlighted), Resolved Vulnerabilities and License Changes. The
comparison URL encodes both SBOM IDs and can be bookmarked or shared, and the diff can be
exported as JSON or CSV.

**Doc impact type:** New Content — document the comparison UI.

From the Feature's Documentation Considerations:
- **User purpose:** UI users need a guide for the comparison workflow.
- **Reference material:** existing SBOM detail page documentation.

The guide should walk through UC-1 (compare two SBOM versions) and UC-2 (share a comparison URL
with the compliance team), explain each diff section and the critical-vulnerability highlight,
and describe export. The API endpoint reference is covered by Task 8 (trustify-backend).

Reference: TC-9003.

## Acceptance Criteria
- [ ] Guide covers starting a comparison from the SBOM list ("Compare selected") and from the comparison page selectors
- [ ] Guide explains each of the six diff sections and the critical highlight
- [ ] Guide explains sharing via URL and JSON/CSV export (noting export availability if Task 7 ships later)
- [ ] Guide is consistent with the existing SBOM detail page documentation style

## Test Requirements
- [ ] Walk through the documented steps against a running build and confirm every step and label matches the UI
- [ ] Verify screenshots/labels match the implemented PatternFly components and section titles
- [ ] Peer review confirms accuracy and completeness relative to the Documentation Considerations scope

## Dependencies
- Depends on: Task 4 — Add /sbom/compare page with SBOM selectors and URL-shareable state
- Depends on: Task 5 — Render collapsible diff sections, count badges and critical highlighting
- Depends on: Task 6 — Add SBOM multi-select and "Compare selected" action to SBOM list
- Depends on: Task 7 — Export SBOM comparison as JSON or CSV
