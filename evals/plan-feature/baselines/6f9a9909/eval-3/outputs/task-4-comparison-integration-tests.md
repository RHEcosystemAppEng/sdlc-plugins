## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint (`GET /api/v2/sbom/compare`). Tests validate the full request-response cycle against a real PostgreSQL test database, covering successful comparisons, error cases, and edge cases like identical SBOMs and large diffs.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the comparison endpoint to the existing SBOM test module

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs`. The existing tests demonstrate the pattern: set up test data in the database, make HTTP requests to the endpoint, and assert on the response status and body.

Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the existing tests. Set up test SBOMs with known package sets, advisory associations, and license values so the diff results are deterministic and verifiable.

Test scenarios should cover:
1. Two SBOMs with distinct packages (verifies added/removed detection)
2. Two SBOMs with overlapping packages at different versions (verifies version change detection with upgrade/downgrade)
3. Two SBOMs where one has advisories the other does not (verifies new/resolved vulnerability detection)
4. Two SBOMs where a shared package changed license (verifies license change detection)
5. Two identical SBOMs (verifies empty diff result)
6. Invalid SBOM IDs (verifies 404 handling)
7. Missing query parameters (verifies 400 handling)

Per CONVENTIONS.md (Key Conventions) -- Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests; follow the same test setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory tests; reference for test data setup involving advisories

## Acceptance Criteria
- [ ] Integration test for successful comparison with added/removed packages passes
- [ ] Integration test for version changes (upgrade and downgrade) passes
- [ ] Integration test for new/resolved vulnerabilities passes
- [ ] Integration test for license changes passes
- [ ] Integration test for identical SBOMs returns empty diff in all categories
- [ ] Integration test for non-existent SBOM ID returns 404
- [ ] Integration test for missing query parameters returns 400
- [ ] All tests follow the existing test patterns in `tests/api/sbom.rs`

## Test Requirements
- [ ] All integration tests pass against a real PostgreSQL test database
- [ ] Tests use deterministic test data with known expected outcomes
- [ ] Tests cover both success and error paths
- [ ] Test function names follow the existing naming convention in the test module

## Verification Commands
- `cargo test -p trustify-tests -- api::sbom::compare` — comparison integration tests pass
- `cargo test -p trustify-tests -- api::sbom` — all SBOM tests pass (no regressions)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
