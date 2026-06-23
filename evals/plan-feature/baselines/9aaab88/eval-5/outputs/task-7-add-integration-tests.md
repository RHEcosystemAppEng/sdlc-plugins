## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update and expand the advisory integration tests to verify the enum-based status column works correctly end-to-end. Tests must validate that advisory list and detail endpoints return correct status strings, that status filtering works without the join, and that the ingestion pipeline writes enum values correctly. These tests serve as the safety net before the feature branch is merged to main.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory integration tests to work with enum status column; add new tests for status filtering by each enum value (New, Analyzing, Fixed, Rejected); add test verifying the response shape is unchanged (status is a string, not an object); add test for ingestion-to-query round-trip with enum status

## Implementation Notes
- In `tests/api/advisory.rs`, existing tests likely seed data with `advisory_status` lookup table inserts and FK references. Update seed data to use the enum column directly.
- Follow the existing test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Add a parametric-style test that filters by each of the four status values to verify enum filtering works:
  ```rust
  // Seed advisories with each status, then:
  let resp = client.get("/api/v2/advisory?status=Fixed").await;
  assert_eq!(resp.status(), StatusCode::OK);
  let body: PaginatedResults<AdvisorySummary> = resp.json().await;
  assert!(body.items.iter().all(|a| a.status == "Fixed"));
  ```
- Verify the response JSON shape matches the pre-migration format — `status` is a flat string field, not a nested object.
- Per CONVENTIONS.md §Key Conventions: integration tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust test file scope.

## Acceptance Criteria
- [ ] All existing advisory tests pass with the new enum-based schema
- [ ] Tests cover filtering by each status value: New, Analyzing, Fixed, Rejected
- [ ] Tests verify response shape is unchanged (status is a string)
- [ ] Tests cover the ingestion-to-query round-trip: ingest advisory with status, query it, verify status string
- [ ] All tests pass with `cargo test -p tests`

## Test Requirements
- [ ] Test: list advisories returns status as string (not enum object or integer)
- [ ] Test: filter by status=New returns only New advisories
- [ ] Test: filter by status=Analyzing returns only Analyzing advisories
- [ ] Test: filter by status=Fixed returns only Fixed advisories
- [ ] Test: filter by status=Rejected returns only Rejected advisories
- [ ] Test: get advisory by ID returns correct status string
- [ ] Test: ingest advisory with known status, then retrieve and verify status matches

## Verification Commands
- `cargo test -p tests` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory endpoints for enum status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline for enum status

[sdlc-workflow] Description digest: sha256-md:c559ec24f32d06a7eabf3703f925760dc4f1f803aa1a81f1b7c96cedd2a728a4
