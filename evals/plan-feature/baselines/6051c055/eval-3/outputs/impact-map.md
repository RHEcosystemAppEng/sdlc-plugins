# Repository Impact Map -- TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison result data model struct (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
  - Add comparison diff service logic in SbomService to compute structured diff between two SBOMs on-the-fly from existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters returning the structured diff
  - Add integration tests for the comparison endpoint covering normal diff, empty diff, missing parameters, non-existent SBOM IDs, and large SBOM performance

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response shape
  - Add API client function fetchSbomComparison() to call GET /api/v2/sbom/compare
  - Add React Query hook (useSbomComparison) for the comparison endpoint
  - Add SbomComparePage component at /sbom/compare with SBOM selector dropdowns, Compare button, Export dropdown, and six ExpandableSection diff sections with composable Tables per Figma design
  - Add MSW mock handlers and fixtures for the comparison endpoint, plus unit tests for comparison page and components
  - Add route definition for /sbom/compare with URL query parameter support
  - Add checkbox selection and "Compare selected" action to existing SbomListPage

## Field Inheritance

- **Priority:** Critical (inherited from Feature TC-9003, propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from Feature TC-9003, propagated to all tasks -- default scope "both" applies)

## Task Summary

| # | Summary | Repository | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | SBOM comparison data model | trustify-backend | main | None |
| 2 | SBOM comparison service | trustify-backend | main | Task 1 |
| 3 | SBOM comparison endpoint | trustify-backend | main | Task 1, Task 2 |
| 4 | Backend integration tests | trustify-backend | main | Task 3 |
| 5 | Frontend API types and client | trustify-ui | main | Task 3 |
| 6 | SBOM comparison page component | trustify-ui | main | Task 5 |
| 7 | MSW mocks and tests | trustify-ui | main | Task 5, Task 6 |
| 8 | SBOM list selection with compare action | trustify-ui | main | Task 6 |

## Cross-repo Dependencies

- Task 5 (trustify-ui: frontend API types/hook) depends on Task 3 (trustify-backend: comparison endpoint) -- the frontend data layer requires the backend comparison endpoint API contract.
- Backend tasks (1-4) have lower task numbers than all frontend tasks (5-8), ensuring the API contract is established before UI integration begins.
