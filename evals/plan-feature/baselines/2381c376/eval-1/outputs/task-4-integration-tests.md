## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the happy path, 404 for missing SBOMs, threshold filtering, advisory deduplication, and cache invalidation after advisory ingestion. These tests validate the end-to-end behavior of the advisory severity aggregation feature defined in TC-9001.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Set up test data by ingesting an SBOM and linking advisories with known severity levels (Critical, High, Medium, Low) using the ingestion pipeline from `modules/ingestor/`.
- Test advisory deduplication by linking the same advisory to an SBOM multiple times and verifying that the count reflects unique advisories only.
- Test the `?threshold` query parameter by calling the endpoint with each severity level and verifying the filtered response shape.
- Test the 404 case by calling the endpoint with a UUID that does not correspond to any ingested SBOM.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the test setup, database fixture, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for how advisory test data is created and linked

## Acceptance Criteria
- [ ] Test for happy path: SBOM with advisories at all severity levels returns correct counts
- [ ] Test for 404: nonexistent SBOM ID returns 404 status
- [ ] Test for deduplication: same advisory linked twice is counted once
- [ ] Test for `?threshold=critical`: only critical count and total are non-zero
- [ ] Test for `?threshold=high`: critical and high counts and total are non-zero
- [ ] Test for `?threshold=medium`: critical, high, and medium counts and total are non-zero
- [ ] Test for `?threshold=low`: all counts returned (equivalent to no threshold)
- [ ] Test for cache invalidation: ingesting a new advisory and calling the endpoint returns updated counts
- [ ] All tests pass in CI with `cargo test --test api`

## Test Requirements
- [ ] Each test function has a doc comment explaining what it validates
- [ ] Tests use the established test database setup and teardown pattern from `tests/api/sbom.rs`
- [ ] Tests cover all severity levels (Critical, High, Medium, Low) and the total field
- [ ] Tests verify the exact JSON response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
