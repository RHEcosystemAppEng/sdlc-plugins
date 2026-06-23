# Task 5 — Add integration tests for SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. Tests hit a real PostgreSQL test database following the existing test pattern, covering happy path comparisons, edge cases (identical SBOMs, empty SBOMs, large diffs), error cases (missing parameters, non-existent IDs), and performance characteristics for the p95 < 1s requirement.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for GET /api/v2/sbom/compare

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a test module registry exists (check existing test structure)

## Implementation Notes
- Follow the existing integration test pattern from `tests/api/sbom.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting two SBOM versions with known package differences
- Test data setup should create two SBOMs with controlled differences:
  - Some packages only in the left SBOM (to test removed packages)
  - Some packages only in the right SBOM (to test added packages)
  - Some packages in both with different versions (to test version changes)
  - Some advisories affecting only one SBOM (to test vulnerability diff)
  - Some packages with different licenses (to test license changes)
- Include a performance-oriented test that creates SBOMs with ~100 packages each and asserts the response completes within a reasonable time bound (not a hard p95 test, but a sanity check).
- Per docs/constraints.md §5.11: Add a doc comment to every test function.
- Per docs/constraints.md §5.12: Add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the same test setup pattern, assertion style, and test database configuration
- `tests/api/advisory.rs` — Reference for advisory-related test data setup

## Acceptance Criteria
- [ ] Happy path test: comparison of two SBOMs with known differences returns correct diff
- [ ] Edge case test: comparison of identical SBOMs returns empty diff
- [ ] Error test: missing query parameters return 400
- [ ] Error test: non-existent SBOM IDs return 404
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: two SBOMs with added/removed packages produce correct added_packages and removed_packages lists
- [ ] Test: two SBOMs with version changes produce correct version_changes with upgrade/downgrade direction
- [ ] Test: two SBOMs with different advisory associations produce correct new/resolved vulnerability lists
- [ ] Test: two SBOMs with license changes produce correct license_changes list
- [ ] Test: identical SBOMs produce empty diff (all lists have zero length)
- [ ] Test: missing left parameter returns 400
- [ ] Test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom_compare` — Run comparison-specific integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint

sha256-md:fcf8c7ac5fab59188aabad194f5392a26459346ddb13130b6b437cf711479794
