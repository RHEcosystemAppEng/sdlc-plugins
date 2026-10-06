# Task 6 — Update advisory integration tests for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify that all advisory operations work correctly with the new enum-based status column. The tests must exercise the advisory list endpoint with status filtering, the advisory detail endpoint, and the advisory ingestion pipeline — all using the `advisory_status_enum` column instead of the `advisory_status` lookup table join. These integration tests run against a real PostgreSQL test database and serve as the primary verification that the migration and code changes are correct end-to-end.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory integration tests to work with enum status; add new test cases for status filtering by enum value; remove any test setup code that inserts into the `advisory_status` lookup table; add tests verifying the migration path (enum values match expected status strings)

## Implementation Notes
- Update test fixtures: remove any setup code that creates rows in the `advisory_status` table. Instead, insert advisory rows with `status` enum values directly.
- Add test cases for each status filter value: verify `GET /api/v2/advisory?status=New`, `?status=Fixed`, etc. return correctly filtered results.
- Verify the API response shape is unchanged: the `status` field in the response body should still be a string (e.g., `"Fixed"`), not a numeric ID.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

### Constraints (from docs/constraints.md)
- §2.1: Every commit MUST reference Jira issue ID in the footer
- §2.2: Commit messages MUST follow Conventional Commits (`test(advisory): ...`)
- §2.3: Every commit MUST include `--trailer="Assisted-by: Claude Code"`
- §5.1: Changes MUST be scoped to the files listed in Files to Modify
- §5.11: MUST add a doc comment to every test function created
- §5.12: MUST add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating the project's test structure, fixture setup, and assertion patterns
- `tests/api/advisory.rs` — current advisory tests to understand the existing test structure before modification

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] Status filtering tests verify each of the four enum values: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Tests verify the API response `status` field is a string, not a numeric ID
- [ ] No test code references the `advisory_status` lookup table
- [ ] Tests verify advisory ingestion produces correct enum status values
- [ ] All test functions have doc comments

## Test Requirements
- [ ] `GET /api/v2/advisory` returns a list with string status values
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status "Fixed"
- [ ] `GET /api/v2/advisory?status=InvalidValue` returns an appropriate error response
- [ ] `GET /api/v2/advisory/{id}` returns a single advisory with correct string status
- [ ] Advisory ingestion followed by `GET /api/v2/advisory` shows the ingested advisory with correct status

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
- Depends on: Task 4 — Update advisory service and endpoints for enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
