# Task 10 — Merge feature branch TC-9006 to main

**Parent Epic:** TC-9006: trustify-backend (<EPIC-BE>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Open a PR that merges the feature branch `TC-9006` into `main`. The PR description should summarize every change made across the feature's tasks:
- The new `remediation` module with `/api/v2/remediation/summary`, `/by-product`, and `/vulnerabilities`
- Performance validation at 10,000 tracked vulnerabilities
- Documentation

It should also reference the companion trustify-ui changes (API hooks, `/remediation` dashboard page, filterable table), which go to the trustify-ui `TC-9006` branch.

## Acceptance Criteria
- [ ] A PR from `TC-9006` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2–9

## Test Requirements
- [ ] Before the merge PR is created, verify that every intermediate task PR (Tasks 2, 3, 4, 5, 6, 7, 8, 9) has been merged into the `TC-9006` feature branch

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product
- Depends on: Task 4 — Add GET /api/v2/remediation/vulnerabilities (filterable list)
- Depends on: Task 5 — Validate remediation aggregation performance
- Depends on: Task 6 — Add remediation API models, REST functions and React Query hooks
- Depends on: Task 7 — Add /remediation dashboard page with summary cards and progress chart
- Depends on: Task 8 — Add filterable vulnerability table to remediation dashboard
- Depends on: Task 9 — Document remediation dashboard and aggregation endpoints
