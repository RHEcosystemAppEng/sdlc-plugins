# Task 5: Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path with various severity distributions, 404 for missing SBOMs, the optional threshold query parameter, deduplication of advisories, and cache behavior. These tests hit a real PostgreSQL test database following the project's existing integration test patterns.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any new test dependencies if needed (likely none, existing test infrastructure should suffice)

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Key patterns to reuse:

1. Use the project's test harness to set up a PostgreSQL test database and start the Axum server
2. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions
3. Set up test data by ingesting an SBOM and linking advisories with known severity levels
4. Parse response bodies as `AdvisorySeveritySummary` for field-level assertions

Test cases to implement:
- **Happy path**: SBOM with advisories at each severity level returns correct counts
- **Empty advisories**: SBOM with no linked advisories returns all-zero counts
- **Deduplication**: Same advisory linked multiple times is counted once
- **404**: Non-existent SBOM ID returns 404 status
- **Threshold filter**: `?threshold=high` returns only critical and high counts (medium and low are zero)
- **Threshold filter — critical**: `?threshold=critical` returns only critical count
- **Invalid threshold**: Invalid threshold value returns 400 Bad Request
- **Response shape**: Response JSON matches expected field names and types

Per CONVENTIONS.md §Testing: use integration tests in `tests/api/` hitting a real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for test setup, SBOM ingestion fixtures, and assertion patterns
- `tests/api/advisory.rs` — reference for advisory test data creation and linking patterns
- `common/src/model/paginated.rs::PaginatedResults` — not directly used but reference for understanding response wrapper patterns

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover happy path, empty results, deduplication, 404, and threshold filtering
- [ ] Test file follows existing test patterns in `tests/api/`
- [ ] No test relies on hardcoded database state; each test sets up its own fixtures

## Test Requirements
- [ ] Test: SBOM with 3 critical, 2 high, 1 medium, 0 low advisories returns `{ critical: 3, high: 2, medium: 1, low: 0, total: 6 }`
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: duplicate advisory IDs are counted once in the totals
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: `?threshold=high` returns critical and high counts, medium and low are 0
- [ ] Test: `?threshold=critical` returns only critical count, others are 0
- [ ] Test: response content-type is `application/json`

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation on advisory ingestion

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass
- `cargo test --test api sbom_advisory_summary -- --nocapture` — run with output for debugging

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:ce43a43b50229616d3e7fbd9c9c7fbd478c206a414140ce29ecf2591e2be40d1
