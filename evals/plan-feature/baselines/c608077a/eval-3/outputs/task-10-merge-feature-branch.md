# Task 10 — Merge feature branch TC-9003 to main

**Summary:** Merge feature branch TC-9003 to main
**Epic:** TC-9003: Comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- SBOM diff model and service (Task 2)
- `GET /api/v2/sbom/compare` endpoint (Task 3)
- frontend API types and hook (Task 4)
- `/sbom/compare` page with URL-shareable state (Task 5)
- diff sections with critical highlighting and virtualization (Task 6)
- SBOM list "Compare selected" entry point (Task 7)
- JSON/CSV export (Task 8)
- documentation (Task 9)

Cross-repository note: the `trustify-backend` `TC-9003` branch (Tasks 2–3) must be merged to `trustify-backend` `main` before, or together with, this `trustify-ui` merge. Otherwise the deployed UI will call an endpoint that does not exist. Link the backend merge PR in this PR's description.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` in `trustify-ui` is open and ready for review
- [ ] The PR description summarizes all intermediate task changes and links the corresponding `trustify-backend` `TC-9003` → `main` PR

## Test Requirements
- [ ] Verify that all intermediate task PRs (Tasks 2–9) have been merged into the `TC-9003` feature branches before creating the merge PR
- [ ] Verify that CI on the `TC-9003` branch is green (unit and E2E tests)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison response model and on-the-fly diff computation in SbomService
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint with integration tests
- Depends on: Task 4 — Add SbomComparison types, fetchSbomComparison() and useSbomComparison hook with MSW mocks
- Depends on: Task 5 — Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states
- Depends on: Task 6 — Add six collapsible diff sections (tables, count badges, critical-vulnerability highlight, virtualized rows)
- Depends on: Task 7 — Add row checkboxes and a "Compare selected" action on the SBOM list page
- Depends on: Task 8 — Add Export dropdown (JSON, CSV) to the SBOM comparison toolbar
- Depends on: Task 9 — Document SBOM comparison API endpoint and comparison UI workflow
