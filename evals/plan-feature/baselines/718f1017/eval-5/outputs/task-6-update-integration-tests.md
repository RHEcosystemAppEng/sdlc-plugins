# Task 6 — Update advisory integration tests for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema where status is an enum column on the `advisory` table instead of a joined lookup table. Test fixtures and setup code that insert rows into the `advisory_status` table must be replaced with direct enum column usage. Verify that API response shapes remain unchanged to confirm backward compatibility.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use `advisory_status_enum` values instead of `advisory_status` table inserts; update assertions to verify status values come from the enum column; remove any test helpers that create `advisory_status` rows

## Implementation Notes
- Existing advisory tests in `tests/api/advisory.rs` likely set up test data by inserting into the `advisory_status` table before creating advisory records. This setup code must be updated to use the enum column directly
- Follow the integration test patterns in `tests/api/sbom.rs` for reference on test setup, HTTP request construction, and assertion patterns
- Test data setup should create advisory records with `status: AdvisoryStatusEnum::New` (or other variants) directly on the model
- Verify that the response JSON still contains the same status string values — this confirms backward compatibility
- Per docs/constraints.md section 5.9-5.13: prefer parameterized tests when multiple test cases exercise the same behavior with different status values; add doc comments to every test function; add given-when-then comments to non-trivial tests
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing test patterns before modifying

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns (setup, request, assertion)
- `tests/api/advisory.rs` — the existing test file being modified; inspect current patterns before changing

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No remaining references to `advisory_status` lookup table in test code
- [ ] Test setup creates advisory records with enum status values directly
- [ ] Tests verify that API response status field still returns the expected string values
- [ ] Tests cover filtering by each status value (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] Advisory list endpoint test with status filter for each enum variant
- [ ] Advisory detail endpoint test verifying status field in response
- [ ] Advisory list endpoint test without status filter (all statuses returned)
- [ ] Each test function has a doc comment explaining the scenario

## Verification Commands
- `cargo test -p trustify-tests` — all integration tests pass
- `grep -r "advisory_status" tests/` — returns no results (confirming lookup table references removed)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly

[sdlc-workflow] Description digest: sha256-md:d6964c4cc7a88f8ecadf6483c8a80ee40cc7266c723f35deb9da4567c4ea5184
