# Task 9 — Merge feature branch TC-9006 to main

**Summary:** Merge feature branch TC-9006 to main
**Parent Epic:** TC-9006: trustify-backend (Epic group "trustify-backend")

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9006` into `main`. The PR description should summarize all changes made across the feature's tasks:
- Task 2: new `remediation` module and `GET /api/v2/remediation/summary`
- Task 3: `GET /api/v2/remediation/by-product`
- Task 4: `GET /api/v2/remediation/vulnerabilities`
- Task 8: remediation documentation
- Frontend (trustify-ui, Tasks 5–7): data layer, `/remediation` dashboard page, filterable table. These live on the trustify-ui `TC-9006` branch and need their own merge PR to trustify-ui `main` after this backend merge (see impact map Open questions).

## Acceptance Criteria
- [ ] A PR from `TC-9006` to `main` is open in trustify-backend and ready for review
- [ ] The PR description summarizes all changes from Tasks 2–8

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2, 3, 4, 5, 6, 7, 8) have been merged into the feature branch before creating the merge PR
- [ ] Verify CI on the `TC-9006` branch is green before opening the PR

## Dependencies
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary endpoint
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 4 — Add filterable GET /api/v2/remediation/vulnerabilities list endpoint
- Depends on: Task 5 — Add remediation API client functions, models, and React Query hooks
- Depends on: Task 6 — Add /remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to the remediation dashboard
- Depends on: Task 8 — Document the remediation dashboard and aggregation endpoints
