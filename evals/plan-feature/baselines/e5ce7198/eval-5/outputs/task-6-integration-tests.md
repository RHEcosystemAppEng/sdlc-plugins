## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to validate the new enum-based status column. Tests must verify that advisory list and detail endpoints return correct status values, that status filtering works with enum values, and that the advisory ingestion pipeline correctly writes enum status values. Remove any test code that references the `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` -- update advisory endpoint integration tests to validate status enum behavior; remove any test setup code that seeds the `advisory_status` lookup table; add tests for status filtering with enum values

## Implementation Notes
In `tests/api/advisory.rs`, update the existing integration tests:
1. Remove any test setup/fixture code that inserts rows into the `advisory_status` table
2. Update advisory creation in tests to set the `status` field using `AdvisoryStatusEnum` values directly
3. Add or update test cases that verify:
   - `GET /api/v2/advisory` returns advisories with correct string status values in the response
   - `GET /api/v2/advisory` with status filter parameter correctly filters by enum value
   - `GET /api/v2/advisory/{id}` returns the correct status string for a single advisory
4. Verify response status assertions follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern used throughout the test suite

Follow the existing test patterns in `tests/api/sbom.rs` for test structure, database setup, and assertion style. Tests hit a real PostgreSQL test database per the project's testing conventions.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test structure, database setup patterns, and assertion conventions
- `tests/api/advisory.rs` -- existing advisory tests to be modified; inspect current test setup for `advisory_status` references

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Tests cover advisory list, detail, and status filter endpoints
- [ ] Tests verify correct status string values in API responses

## Test Requirements
- [ ] Test advisory list endpoint returns correct status strings for multiple advisories with different statuses
- [ ] Test status filter parameter on advisory list endpoint with each enum value
- [ ] Test advisory detail endpoint returns correct status string
- [ ] Test that advisory creation via ingestion produces correct status values in subsequent API reads

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Advisory service/endpoints update (tests depend on updated endpoint behavior)
- Depends on: Task 5 -- Ingestion pipeline update (tests verify end-to-end ingestion with enum status)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:df22fbab2928f43e4fcbab0b7b727cd30656dc333ce98884bdd4921490bd3b03
