# Task 9 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison diff service and endpoint (Tasks 2-4), frontend API types/client/hooks (Task 5), comparison page UI with Figma-aligned diff sections (Task 6), SBOM list page selection integration (Task 7), and comprehensive tests (Tasks 4, 8).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-8
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-8) have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service
- Depends on: Task 3 — Add SBOM comparison REST endpoint
- Depends on: Task 4 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 5 — Add API types and client function for SBOM comparison
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM selection and comparison trigger on list page
- Depends on: Task 8 — Add tests for SBOM comparison frontend components

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:c1f5b9d3e8a4027f6c2d5a7e9b1c3f6a8d0e4b6c8f2a4d7e9b1c3f5a8d0e2b4c
