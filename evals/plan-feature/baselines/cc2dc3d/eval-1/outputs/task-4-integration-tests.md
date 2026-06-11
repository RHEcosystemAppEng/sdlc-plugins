## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover: successful severity aggregation with correct counts, 404 response for non-existent SBOM ID, advisory deduplication (same advisory linked multiple times should not inflate counts), threshold query parameter filtering, and cache invalidation after advisory ingestion.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or directly in the database
  2. Create advisories at various severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the sbom_advisory join table
- Test cases to implement:
  - **Happy path**: SBOM with advisories at all four severity levels; verify response contains correct counts and total
  - **Empty advisories**: SBOM with no linked advisories; verify all counts are 0 and total is 0
  - **Not found**: Request with a non-existent SBOM UUID; verify 404 response
  - **Deduplication**: Link the same advisory to the SBOM twice (if possible via the data model); verify it is counted only once
  - **Threshold filter (critical)**: Use `?threshold=critical`; verify only critical count is non-zero in the response (or that medium/low are excluded depending on implementation)
  - **Threshold filter (high)**: Use `?threshold=high`; verify critical and high counts are included
  - **Cache invalidation**: Fetch summary, ingest a new advisory linked to the SBOM, fetch summary again; verify counts are updated (not stale cached values)
- Use the existing test infrastructure for database setup and HTTP client invocation as seen in sibling test files.
- Per docs/constraints.md section 5 (Code Change Rules): changes scoped to listed files, inspect code before modifying, follow referenced patterns.
- Per docs/constraints.md section 5.9-5.10: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs, but only if sibling test files use parameterized patterns. If `tests/api/sbom.rs` and `tests/api/advisory.rs` use individual test functions, follow that pattern instead.
- Per docs/constraints.md section 5.11-5.13: add a doc comment to every test function; add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; may contain helpers for creating test advisories with specific severity levels
- `common/src/model/paginated.rs::PaginatedResults` — if any test needs to verify paginated responses (may not apply here, but available for reference)

## Acceptance Criteria
- [ ] Integration test for successful severity aggregation passes with correct counts
- [ ] Integration test for 404 on non-existent SBOM passes
- [ ] Integration test for advisory deduplication passes
- [ ] Integration test for threshold query parameter filtering passes
- [ ] Integration test for cache invalidation after advisory ingestion passes
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Test: SBOM with 2 critical, 3 high, 1 medium, 4 low advisories returns `{ critical: 2, high: 3, medium: 1, low: 4, total: 10 }`
- [ ] Test: Non-existent SBOM UUID returns HTTP 404
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: `?threshold=critical` returns only critical count (medium and low are 0 or excluded)
- [ ] Test: `?threshold=high` returns critical and high counts
- [ ] Test: After ingesting a new advisory for an SBOM, the summary reflects the updated count
- [ ] Every test function has a doc comment
- [ ] Non-trivial test functions have given-when-then inline comments

## Verification Commands
- `cargo test -p tests --test advisory_summary` — run the advisory summary integration tests
- `cargo test` — verify all tests pass including existing tests

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
