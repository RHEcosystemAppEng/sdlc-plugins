## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison backend endpoint (GET /api/v2/sbom/compare) with structured diff computation, new frontend comparison page with PatternFly diff sections, SBOM list page multi-select integration, and full test coverage including integration and E2E tests.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the TC-9003 feature branch
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes across both trustify-backend and trustify-ui repositories
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify no merge conflicts exist between TC-9003 and main
- [ ] Verify all tests pass on the feature branch (backend integration tests + frontend unit tests + E2E tests)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Create SBOM comparison page with diff section components
- Depends on: Task 6 — Add comparison route and update SBOM list page with multi-select

[sdlc-workflow] Description digest: sha256-md:0923b90cc0803fe3781db411977d7ffbd22e183b85236e0d56f8f1193e9ca2b4
