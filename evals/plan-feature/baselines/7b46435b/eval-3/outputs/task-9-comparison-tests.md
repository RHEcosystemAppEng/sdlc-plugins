## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add comprehensive tests and mock fixtures for the SBOM comparison feature. This includes MSW request handlers for the comparison endpoint, test fixtures with representative comparison data, unit tests for the comparison page components, and updates to the existing SBOM list page tests to cover the new checkbox selection and "Compare selected" button behavior.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison response data with all six diff categories populated
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Unit tests for the comparison page

## Files to Modify
- `tests/mocks/handlers.ts` -- Add MSW handler for `GET /api/v2/sbom/compare` that returns the fixture data
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- Add tests for checkbox selection and "Compare selected" button

## Implementation Notes
- Follow the existing test patterns in `src/pages/SbomDetailPage/SbomDetailPage.test.tsx` for component tests.
- Use Vitest + React Testing Library for unit tests per project convention.
- **MSW handler:** add a handler in `tests/mocks/handlers.ts` that intercepts `GET */api/v2/sbom/compare*` and returns the fixture data from `sbom-comparison.json`. Follow the pattern of existing handlers for `sbom` and `advisory` endpoints.
- **Test fixture (`sbom-comparison.json`):** create a realistic comparison result with:
  - 2-3 added packages (varied licenses and advisory counts)
  - 2-3 removed packages
  - 2-3 version changes (mix of upgrades and downgrades)
  - 2-3 new vulnerabilities (include at least one with severity "critical" to test highlighting)
  - 1-2 resolved vulnerabilities
  - 1-2 license changes
- **Comparison page tests (`SbomComparePage.test.tsx`):**
  - Empty state rendering (no URL params)
  - Comparison results rendering (with URL params triggering auto-comparison)
  - SBOM selector interaction and Compare button click
  - Diff section expansion/collapse behavior
  - Critical vulnerability row highlighting
  - URL parameter encoding on Compare click
  - Error state handling when API call fails
- **SBOM list page test updates (`SbomListPage.test.tsx`):**
  - Checkbox selection on table rows
  - "Compare selected" button enable/disable state based on selection count
  - Navigation to comparison page with correct URL parameters
  - No regression of existing list page tests
- Per CONVENTIONS.md (Key Conventions) -- Testing: Vitest + React Testing Library for unit tests; MSW for API mocking. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's test file scope.
- Per CONVENTIONS.md (Key Conventions) -- Naming: PascalCase for component files. Applies: task creates `SbomComparePage.test.tsx` matching the convention's naming scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer.

## Reuse Candidates
- `tests/mocks/handlers.ts` -- existing MSW handlers to follow as pattern for new comparison handler
- `tests/mocks/fixtures/sboms.json` -- existing fixture format reference for SBOM data shape
- `tests/mocks/fixtures/advisories.json` -- existing fixture format reference for advisory data shape
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- existing test file being extended; study test setup and render helpers
- `tests/setup.ts` -- test setup with render helpers and MSW server configuration

## Acceptance Criteria
- [ ] MSW handler intercepts comparison endpoint requests and returns fixture data
- [ ] Test fixture contains representative data for all six diff categories
- [ ] All comparison page tests pass
- [ ] All SBOM list page tests pass (existing and new)
- [ ] No regressions in existing test suite

## Test Requirements
- [ ] Empty state test: page shows "Select two SBOMs to compare" empty state when no URL params
- [ ] Results test: page renders all six diff sections with correct data from fixture
- [ ] Selector test: SBOM selectors load and display available SBOMs
- [ ] Compare button test: clicking Compare triggers API call and renders results
- [ ] Critical highlight test: critical vulnerability rows have danger/highlighted styling
- [ ] URL params test: comparison auto-triggers when left and right params are present in URL
- [ ] Error state test: page handles API error gracefully
- [ ] List page selection test: checkbox selection works correctly on SBOM table rows
- [ ] List page compare button test: button enables only with exactly 2 selections
- [ ] List page navigation test: Compare button navigates to correct URL

## Verification Commands
- `npx vitest run` -- expected: all tests pass
- `npx vitest run src/pages/SbomComparePage` -- expected: comparison page tests pass
- `npx vitest run src/pages/SbomListPage` -- expected: list page tests pass (including new tests)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 6 -- Implement SBOM comparison page with diff sections
- Depends on: Task 7 -- Add comparison selection to SBOM list page
