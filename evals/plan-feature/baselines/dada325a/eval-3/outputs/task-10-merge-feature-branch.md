# Task 10 — Merge feature branch TC-9003 to main

**Summary:** Merge feature branch TC-9003 to main
**Epic:** TC-9003: Delivery and documentation

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Open a PR that merges the feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Backend (trustify-backend): SBOM comparison model and diff service (Task 2), `GET /api/v2/sbom/compare` endpoint (Task 3)
- Frontend (trustify-ui): comparison API types, client, and hook (Task 4); `/sbom/compare` page with selectors, URL state, and empty/loading/error states (Task 5); the six diff sections with virtualization and critical highlighting (Task 6); "Compare selected" on the SBOM list (Task 7); JSON/CSV export (Task 8)
- Documentation (Task 9)

Note: the backend changes live on `TC-9003` in trustify-backend. Merge that branch to `main` before, or together with, the trustify-ui merge, so the frontend never reaches `main` without the endpoint it calls (see the impact map, "Open questions / scope conflicts").

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] The PR description summarizes all intermediate task changes and links the task PRs

## Test Requirements
- [ ] Verify that all intermediate task PRs (Tasks 2–9) have been merged into the `TC-9003` branch before creating the merge PR
- [ ] Verify that CI passes on the `TC-9003` branch

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states
- Depends on: Task 6 — Render the six collapsible diff sections with virtualization and critical highlighting
- Depends on: Task 7 — Add "Compare selected" multi-select to the SBOM list page
- Depends on: Task 8 — Export comparison as JSON or CSV
- Depends on: Task 9 — Document the SBOM comparison endpoint and comparison UI
