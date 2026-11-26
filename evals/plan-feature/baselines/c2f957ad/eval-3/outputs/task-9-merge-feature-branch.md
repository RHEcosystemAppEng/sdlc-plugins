# Task 9 — Merge feature branch TC-9003 to main

**Summary:** Merge feature branch TC-9003 to main
**Issue type:** Task | **Parent (Epic):** Epic D — TC-9003: Feature branch lifecycle
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- trustify-backend (Tasks 2–3): `SbomComparison` model, `SbomService::compare`, `GET /api/v2/sbom/compare` endpoint, integration tests, README API reference
- trustify-ui (Tasks 4–8): comparison API types/hook, `/sbom/compare` page with six diff sections, shareable URL, critical highlighting, virtualization, "Compare selected" on the SBOM list, JSON/CSV export, documentation

Because the UI depends on the new backend endpoint, the trustify-backend `TC-9003` branch must be merged to `main` before or together with this PR.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes all changes across Tasks 2–8 and references TC-9003

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2–8) have been merged into the feature branch before creating the merge PR
- [ ] Verify the trustify-backend `TC-9003` changes are merged (or have an open merge PR) so `main` is not left with a UI calling a missing endpoint

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add comparison API types, REST function and React Query hook
- Depends on: Task 5 — Build SBOM comparison page at /sbom/compare
- Depends on: Task 6 — Add "Compare selected" action to SBOM list page
- Depends on: Task 7 — Export comparison as JSON or CSV
- Depends on: Task 8 — Document SBOM comparison endpoint and UI
