## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint, covering valid diffs, edge cases (empty diff, large SBOMs), and error conditions. Tests hit a real PostgreSQL test database following the existing test patterns in `tests/api/`.

## Files to Create
- `tests/api/sbom_compare.rs` -- Integration tests for `GET /api/v2/sbom/compare`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs`: set up test data in PostgreSQL, make HTTP requests to the running test server, assert on response status and body.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions.
- Test data setup: ingest two SBOMs with known differences (added packages, removed packages, version changes, different advisories, different licenses).
- Verify the response JSON structure matches `SbomComparison` with all six diff categories.
- Include an edge case test with two identical SBOMs to verify empty diff arrays.
- Include error case tests for missing query params and non-existent SBOM IDs.

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM endpoint tests; reuse test setup patterns and helper functions for ingesting test SBOMs
- `tests/api/advisory.rs` -- Advisory test patterns; reuse for setting up advisory test data linked to SBOMs

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover: valid diff with all six categories, empty diff, missing query params, non-existent SBOM IDs
- [ ] Test assertions validate both response status codes and response body structure

## Test Requirements
- [ ] Integration test: compare two SBOMs with added and removed packages, verify correct counts and package names
- [ ] Integration test: compare two SBOMs with version changes, verify direction field (upgrade/downgrade)
- [ ] Integration test: compare two SBOMs with different advisory associations, verify new and resolved vulnerabilities
- [ ] Integration test: compare two SBOMs with license changes, verify left and right licenses
- [ ] Integration test: compare identical SBOMs, verify all diff arrays are empty
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom_compare` -- all comparison integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- SBOM comparison REST endpoint

[sdlc-workflow] Description digest: sha256-md:87727b3f3b6ece52564223137468bf92a8c8b3af5959a10ac57f7d8c0f4419d0
