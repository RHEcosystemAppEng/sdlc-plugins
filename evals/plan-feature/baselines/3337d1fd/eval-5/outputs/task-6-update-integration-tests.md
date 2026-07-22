## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. The existing tests in `tests/api/advisory.rs` reference the `advisory_status` lookup table for test data setup and assertions. These must be updated to use the `AdvisoryStatusEnum` values directly. Test data setup must insert advisories with enum status values instead of creating lookup table rows and foreign key references.

## Files to Modify
- `tests/api/advisory.rs` — update test data setup to use enum status values instead of lookup table inserts; update assertions to compare against enum string values; remove any test helpers that create `advisory_status` rows

## Implementation Notes
- In test setup code, replace any `advisory_status` table inserts with direct `advisory.status` enum column assignments when creating test advisory records
- Update status filter assertions: instead of joining to verify status, assert directly on the `status` field in the JSON response (which remains a string value like `"Fixed"`)
- Follow the testing convention: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.
- Reference existing test patterns in `tests/api/sbom.rs` for endpoint integration test structure without lookup table dependencies

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns (setup, request, assertion) that do not use lookup tables

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Status filtering tests verify correct behavior with the enum column
- [ ] Test data setup uses `AdvisoryStatusEnum` values directly

## Test Requirements
- [ ] Run `cargo test` for the advisory integration tests and verify all pass
- [ ] Verify status filter endpoint test correctly filters by enum values
- [ ] Verify advisory list endpoint test returns status as a string in the response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service, model, and endpoint layers
- Depends on: Task 5 — Update advisory ingestion pipeline
