# Task 10 — Merge feature branch TC-9003 to main

**Summary:** Merge feature branch TC-9003 to main
**Epic:** TC-9003: Delivery and documentation
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks:

- trustify-backend: SBOM comparison model and on-the-fly diff service (Task 2), `GET /api/v2/sbom/compare` endpoint with integration tests (Task 3), documentation (Task 9)
- trustify-ui: comparison API client and `useSbomComparison` hook (Task 4), `/sbom/compare` page with selectors, URL state, empty/loading/error states (Task 5), six diff sections with critical highlighting and virtualization (Task 6), "Compare selected" on the SBOM list page (Task 7), JSON/CSV export (Task 8)

trustify-ui is the bookend repository (majority of tasks). Because the UI depends on the new backend endpoint, the trustify-backend `TC-9003` branch must be merged to its `main` before or together with this PR; note the corresponding backend merge PR in this PR's description.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2–9) have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states
- Depends on: Task 6 — Render collapsible diff sections with tables, critical highlighting, and virtualization
- Depends on: Task 7 — Add "Compare selected" action to the SBOM list page
- Depends on: Task 8 — Export comparison result as JSON or CSV
- Depends on: Task 9 — Document the SBOM comparison endpoint and comparison UI workflow
