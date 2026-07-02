# Task 6: Update advisory integration tests for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the schema change from lookup table join to direct enum column. Test fixtures and assertions that reference the `advisory_status` table or `status_id` foreign key must be updated to use the `advisory_status_enum` column. Add test coverage for status filtering with enum values.

## Files to Modify
- `tests/api/advisory.rs` — update test fixtures to insert advisories with `status` enum values instead of `status_id` FK references; update assertions to verify status enum serialization; add tests for status filtering with each enum value

## Implementation Notes
- Update advisory test fixture setup to insert advisory rows with `status: AdvisoryStatusEnum::Fixed` (or other variants) instead of inserting into `advisory_status` and referencing via `status_id`.
- Remove any test helper code that sets up `advisory_status` lookup table rows.
- Add a test case that filters the advisory list by each enum value (New, Analyzing, Fixed, Rejected) and verifies correct results.
- Verify that the API response shape is unchanged — status should serialize as a string (e.g., `"Fixed"`) in the JSON response.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/` directory scope.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` — use for constructing test fixtures with type-safe enum values
- `common/src/model/paginated.rs::PaginatedResults` — deserialize list endpoint responses in tests

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references `advisory_status` table or `status_id` column
- [ ] Test coverage exists for filtering advisories by each status enum value
- [ ] API response JSON contains status as a string (unchanged response shape)

## Test Requirements
- [ ] GET /api/v2/advisory returns advisories with correct status strings
- [ ] GET /api/v2/advisory?status=Fixed filters correctly using enum value
- [ ] GET /api/v2/advisory/{id} returns the correct status string for a single advisory
- [ ] Status filtering with each enum value (New, Analyzing, Fixed, Rejected) returns correct results

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service, model, and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum writes
