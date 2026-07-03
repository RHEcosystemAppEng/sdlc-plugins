## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. Tests should cover the full range of diff scenarios including added/removed packages, version changes, new/resolved vulnerabilities, and license changes. Tests hit a real PostgreSQL test database following the project's existing test patterns.

## Files to Create
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify
- `tests/Cargo.toml` -- Register the new test module if needed based on test framework setup

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` -- use the same test database setup and teardown approach.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions per project convention.
- Test data setup strategy:
  1. Ingest two SBOMs with known, controlled package sets
  2. Ensure some packages overlap with different versions (for version change detection)
  3. Ensure some packages are unique to each side (for add/remove detection)
  4. Associate advisories with packages in only one SBOM (for vulnerability change detection)
  5. Set different licenses on overlapping packages (for license change detection)
- Performance test (optional): create SBOMs with ~2000 packages each and verify the comparison completes within the p95 < 1s requirement.
- Per CONVENTIONS.md (Key Conventions) -- Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow the same test setup pattern, assertions, and helper utilities
- `tests/api/advisory.rs` -- advisory test patterns for setting up advisory test data

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover all six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes
- [ ] Tests cover error cases: non-existent SBOM IDs (404), missing parameters (400)
- [ ] Tests cover edge case: identical SBOMs producing empty diff
- [ ] No regressions in existing test suite

## Test Requirements
- [ ] Test added packages scenario: right SBOM has packages not in left
- [ ] Test removed packages scenario: left SBOM has packages not in right
- [ ] Test version changes with correct upgrade/downgrade direction
- [ ] Test new vulnerability detection across SBOMs
- [ ] Test resolved vulnerability detection across SBOMs
- [ ] Test license change detection for overlapping packages
- [ ] Test empty comparison result when SBOMs are identical
- [ ] Test 404 response for invalid SBOM IDs
- [ ] Test 400 response for missing query parameters

## Verification Commands
- `cargo test --test api sbom_compare` -- expected: all comparison tests pass
- `cargo test --test api` -- expected: all existing and new tests pass (no regressions)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison service and REST endpoint
