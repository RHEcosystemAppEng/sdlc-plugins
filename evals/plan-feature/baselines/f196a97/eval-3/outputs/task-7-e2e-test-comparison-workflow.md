# Task 7 — Add Playwright E2E test for SBOM comparison workflow

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a Playwright end-to-end test covering the full SBOM comparison workflow: navigating to the SBOM list, selecting two SBOMs, clicking "Compare selected", verifying the comparison page loads with correct diff sections, and verifying URL shareability by navigating directly to a comparison URL.

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
- Follow the existing E2E test pattern in `tests/e2e/sbom-list.spec.ts` for test structure, page navigation, and assertion style.
- Use the test setup from `tests/setup.ts` for MSW handlers and render helpers.
- Test scenarios should cover:
  1. UC-1: Navigate to SBOM list, select two SBOMs via checkboxes, click "Compare selected", verify all six diff sections render
  2. UC-2: Navigate directly to `/sbom/compare?left={id1}&right={id2}`, verify the comparison auto-loads
  3. Verify empty state renders when navigating to `/sbom/compare` without query params
- Add MSW handlers in `tests/mocks/handlers.ts` for the comparison endpoint if not already added by Task 5.

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test demonstrating the test setup, navigation, and assertion patterns
- `tests/setup.ts` — test setup configuration with MSW handlers
- `tests/mocks/handlers.ts` — existing MSW request handlers to extend with comparison endpoint mock

## Acceptance Criteria
- [ ] E2E test for UC-1 (select and compare) passes
- [ ] E2E test for UC-2 (URL shareability) passes
- [ ] E2E test for empty state passes
- [ ] Tests do not flake due to loading state timing

## Test Requirements
- [ ] E2E test: full comparison workflow from SBOM list selection to diff rendering
- [ ] E2E test: direct URL navigation loads comparison automatically
- [ ] E2E test: empty state renders when no query params are provided

## Verification Commands
- `npx playwright test sbom-compare` — all E2E comparison tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add SBOM selection and "Compare selected" action to SbomListPage
