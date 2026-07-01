## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all integration tests that reference the `advisory_status` lookup table or use `status_id` to work with the new `AdvisoryStatusEnum` column. Test fixtures must stop inserting into the lookup table and instead use enum values directly. Response assertions must validate that status is returned as a string matching the enum variants.

## Files to Modify
- `tests/api/advisory.rs` — update test fixtures to insert advisories with `status: AdvisoryStatusEnum` instead of `status_id` FK; update response assertions to check status as a string enum value; remove any setup code that creates `advisory_status` lookup table rows; add tests for status enum filtering
- `tests/api/search.rs` — if search tests filter by advisory status or assert on status values in search results, update them to use enum string values instead of integer IDs

## Implementation Notes
- Existing tests likely set up the test database by inserting rows into `advisory_status` and then referencing those IDs when creating advisory fixtures — remove all `advisory_status` setup
- When creating test advisory entities, set `status` directly with the enum variant:
  ```rust
  advisory::ActiveModel {
      status: Set(AdvisoryStatusEnum::New),
      // ... other fields
  }
  ```
- Response assertions should check: `assert_eq!(json["status"], "New")` (string, not integer)
- Follow the existing test pattern in `tests/api/sbom.rs` for test structure: setup database, make HTTP request, assert response
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions
- Add test cases for each enum value to ensure comprehensive coverage
- Verify pagination still works correctly with the enum-based filtering

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test pattern: database setup, HTTP request, response assertion, cleanup
- `tests/api/advisory.rs` — current tests to understand existing fixture creation and assertion patterns before modifying

## Acceptance Criteria
- [ ] All advisory integration tests pass without referencing the `advisory_status` table
- [ ] Tests cover filtering by each of the four status values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify that status is returned as a string in JSON responses
- [ ] No test code imports or references `advisory_status` entity
- [ ] Search tests pass if they involve advisory status filtering

## Test Requirements
- [ ] `cargo test -p tests --test advisory` — all advisory tests pass
- [ ] `cargo test -p tests --test search` — all search tests pass (if status-related)
- [ ] Test coverage includes: list with no filter, list with each status filter, get by ID, status in response shape

## Verification Commands
- `cargo test -p tests` — all integration tests pass
- `cargo test -p tests --test advisory` — advisory-specific tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and models
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update ingestion pipeline
