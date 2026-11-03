# Task 10 — Merge feature branch TC-9003 to main

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR that merges the feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:
- The SBOM comparison diff service and `GET /api/v2/sbom/compare` endpoint (trustify-backend, Tasks 2–3)
- The comparison API client and hook (Task 4)
- The diff section components (Task 5)
- The `/sbom/compare` page (Task 6)
- "Compare selected" on the SBOM list (Task 7)
- JSON/CSV export (Task 8)
- Documentation (Task 9)

The PR should note that the corresponding `TC-9003` -> `main` merge in trustify-backend must land first or at the same time, so the UI never reaches `main` without its endpoint.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify that all intermediate task PRs (Tasks 2–9) have been merged into the `TC-9003` feature branch before you create the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add comparison API client, types, and React Query hook
- Depends on: Task 5 — Add comparison diff section components
- Depends on: Task 6 — Add SBOM comparison page at /sbom/compare
- Depends on: Task 7 — Add multi-select and "Compare selected" to SBOM list page
- Depends on: Task 8 — Add JSON/CSV export to SBOM comparison page (non-MVP)
- Depends on: Task 9 — Document SBOM comparison endpoint and UI workflow
