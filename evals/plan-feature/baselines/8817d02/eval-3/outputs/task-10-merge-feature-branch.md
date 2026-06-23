# Task 10 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison backend endpoint with diff logic (trustify-backend), and new comparison UI page with selectors, diff sections, and tests (trustify-ui).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes across both repositories

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model types
- Depends on: Task 3 — Implement SBOM comparison service logic
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 6 — Add SBOM comparison API types and client function
- Depends on: Task 7 — Add React Query hook for SBOM comparison
- Depends on: Task 8 — Implement SBOM comparison page with diff sections
- Depends on: Task 9 — Add tests and MSW mocks for SBOM comparison page

sha256-md:7e276cf637296b6dc751f49da6d53e793055c47114f5ca9d2ef48ce2978de788
