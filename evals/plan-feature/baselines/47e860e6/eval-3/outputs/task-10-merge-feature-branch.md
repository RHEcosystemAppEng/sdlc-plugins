# Task 10 — Merge feature branch TC-9003 to main

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the SBOM comparison page at `/sbom/compare`, diff section components, the comparison API client and hook, "Compare selected" on the SBOM list page, JSON/CSV export, and docs. It should reference the backend `GET /api/v2/sbom/compare` endpoint delivered in `trustify-backend`.

Note: the backend `TC-9003` branch in `trustify-backend` (Tasks 2, 3, 9) must be merged to `main` before or together with this PR, so the UI never ships against a missing endpoint. See the cross-repo caveat in the workflow mode decision comment.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes the changes from all intermediate tasks and links TC-9003

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2–9) have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the `TC-9003` branch

## Dependencies
- Depends on: Task 2 — Backend: SBOM comparison model and diff service
- Depends on: Task 3 — Backend: GET /api/v2/sbom/compare endpoint and integration tests
- Depends on: Task 4 — Frontend: comparison API types, client function, React Query hook and mocks
- Depends on: Task 5 — Frontend: comparison diff section components
- Depends on: Task 6 — Frontend: SBOM comparison page and /sbom/compare route
- Depends on: Task 7 — Frontend: multi-select and "Compare selected" on SBOM list page
- Depends on: Task 8 — Frontend: export comparison as JSON / CSV (non-MVP)
- Depends on: Task 9 — Documentation: SBOM comparison endpoint and UI guide
