# Task 5: Add integration tests for advisory-summary endpoint

## Repository

trustify-backend

## Target Branch

main

## Description

Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the happy path, 404 for missing SBOMs, caching behavior, and deduplication of advisory counts. These tests exercise the full stack from HTTP request through service layer to database.

## Files to Create

- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify

- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes

- Follow the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, HTTP client usage, database seeding, and assertion style.
- Use the existing test harness to spin up the server, seed test data, and make HTTP requests.
- Seed test data by:
  - Creating an SBOM entry in the database
  - Creating advisory entries with known severity values (e.g., 2 critical, 3 high, 1 medium, 1 low)
  - Linking advisories to the SBOM via the `sbom_advisory` join table entity (`entity/sbom_advisory.rs`)
- For the deduplication test, link the same advisory to the SBOM multiple times (if the schema allows) or create multiple `sbom_advisory` rows for the same advisory ID, and verify the count reflects unique advisories only.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions as established in the codebase.
- Per CONVENTIONS.md §Testing: tests must hit a real PostgreSQL test database using the existing integration test infrastructure. See `tests/api/sbom.rs` for the established pattern.
  Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates

- `tests/api/sbom.rs` — Test setup patterns, HTTP client configuration, SBOM test data seeding
- `tests/api/advisory.rs` — Advisory test data seeding and assertion patterns
- `entity/sbom_advisory.rs` — Join table entity for seeding test relationships
- `common/src/error.rs::AppError` — Expected error response format for 404 assertions

## Acceptance Criteria

- [ ] Happy-path test: seed SBOM with known advisories, verify response matches expected severity counts and total
- [ ] 404 test: request advisory-summary for a non-existent SBOM ID, verify 404 response
- [ ] Deduplication test: seed duplicate advisory links, verify counts reflect unique advisories only
- [ ] Cache test: verify response includes appropriate cache headers (e.g., `Cache-Control: max-age=300`)
- [ ] All tests pass in CI

## Test Requirements

- [ ] Happy path: SBOM with multiple advisories of varying severities returns correct counts and total
- [ ] Not found: non-existent UUID returns 404 status
- [ ] Deduplication: duplicate sbom_advisory rows for the same advisory produce correct unique counts
- [ ] Caching: response headers indicate 5-minute cache

## Dependencies

- Depends on: Task 1 — Add AdvisorySeveritySummary response model
- Depends on: Task 2 — Add advisory summary aggregation to SbomService
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Verification Commands

- `cargo test --test api -- sbom_advisory_summary` — run all advisory-summary integration tests
