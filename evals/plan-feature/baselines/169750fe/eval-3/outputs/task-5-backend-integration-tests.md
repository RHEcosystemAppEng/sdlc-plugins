## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint covering the main diff scenarios: normal comparison with mixed changes, comparison of identical SBOMs (empty diff), and error cases (missing parameters, non-existent SBOM IDs). Tests hit a real PostgreSQL test database following the established integration test pattern.

## Files to Create
- `tests/api/sbom_compare.rs` — integration tests for GET /api/v2/sbom/compare

## Files to Modify
- `tests/api/sbom.rs` — optionally add compare-related test helpers if the existing SBOM test setup can be extended

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` for test setup, database fixtures, and assertion style. Tests should use `assert_eq!(resp.status(), StatusCode::OK)` pattern per conventions.

Test scenarios:
1. **Normal comparison**: seed two SBOMs with overlapping but different package sets; verify all six diff categories contain expected entries
2. **Identical SBOMs**: seed two identical SBOMs; verify all diff categories are empty arrays
3. **Missing parameters**: call without `left` or `right` query param; verify 400 response
4. **Non-existent SBOM**: call with a non-existent SBOM ID; verify 404 response
5. **Large diff**: seed SBOMs with many packages to verify performance characteristics

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — advisory integration tests for reference on testing advisory-related queries

## Acceptance Criteria
- [ ] Integration tests cover normal comparison with all six diff categories
- [ ] Integration tests cover identical SBOM comparison (empty diff)
- [ ] Integration tests cover missing query parameter (400 response)
- [ ] Integration tests cover non-existent SBOM ID (404 response)
- [ ] All tests pass with `cargo test --test api`

## Test Requirements
- [ ] Test data seeds at least two SBOMs with known package, advisory, and license differences
- [ ] Assertions verify the exact count and content of each diff category
- [ ] Tests are isolated — each test uses its own database fixtures

## Verification Commands
- `cargo test --test api sbom_compare` — run only the comparison integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Backend comparison endpoint
