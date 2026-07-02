## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify the new enum-based status schema. The existing tests in `tests/api/advisory.rs` reference the `advisory_status` lookup table for test setup and assertions. These must be updated to use the `AdvisoryStatusEnum` values directly. Add new tests to cover status filtering via the enum column and verify that the advisory ingestion pipeline writes enum values correctly.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory endpoint integration tests to use enum-based status setup and assertions; add new tests for status filtering by enum value; verify ingestion writes enum values

## Implementation Notes
- In the test setup, replace any code that inserts rows into the `advisory_status` table with direct use of `AdvisoryStatusEnum` values on the `advisory` model. For example, replace:
  ```rust
  // Old: insert into advisory_status, get ID, set advisory.status_id
  let status = advisory_status::ActiveModel { name: Set("Fixed".to_string()), .. }.insert(&db).await?;
  advisory_model.status_id = Set(status.id);
  ```
  with:
  ```rust
  // New: set enum directly
  advisory_model.status = Set(AdvisoryStatusEnum::Fixed);
  ```
- Add a test for each status value to verify filtering: `GET /api/v2/advisory?status=New`, `?status=Analyzing`, `?status=Fixed`, `?status=Rejected`.
- Add a test that verifies an invalid status filter returns 400 Bad Request.
- Add a test that verifies advisory ingestion stores the correct enum value.
- Follow the existing test pattern: tests hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`.
- Per repo Key Conventions: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Reuse Candidates
- `tests/api/advisory.rs` — current advisory tests (pre-modification) showing the existing test setup, request patterns, and assertion style
- `tests/api/sbom.rs` — SBOM endpoint integration tests as a reference for the test structure and database setup patterns

## Acceptance Criteria
- [ ] All existing advisory tests pass with enum-based status setup
- [ ] No references to `advisory_status` table remain in test code
- [ ] Status filtering tests cover all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Invalid status filter test verifies 400 response
- [ ] Ingestion test verifies enum value is written correctly
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test `GET /api/v2/advisory` returns advisories with correct status strings
- [ ] Test `GET /api/v2/advisory?status=Fixed` returns only Fixed advisories
- [ ] Test `GET /api/v2/advisory?status=InvalidValue` returns 400 Bad Request
- [ ] Test `GET /api/v2/advisory/{id}` returns correct status in detail response
- [ ] Test advisory ingestion creates advisory with correct enum status value
- [ ] Test migration + query roundtrip: migrate, insert with enum, query back, verify status

## Verification Commands
- `cargo test --test advisory` — run all advisory integration tests
- `cargo test --workspace` — run full test suite to verify no regressions

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory endpoints to query status enum directly
- Depends on: Task 6 — Update advisory ingestion pipeline for enum status values

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:f396e5a4d7efa33025245f702dabfe2b6f6f52fae61013b09e29f40f42f755bf
