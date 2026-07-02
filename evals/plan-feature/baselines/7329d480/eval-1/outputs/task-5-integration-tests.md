# Task 5 — Integration tests for advisory summary endpoint

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests exercise the full request path against a real PostgreSQL test database, covering success cases with various advisory distributions, the 404 case for missing SBOMs, and edge cases like SBOMs with no advisories or duplicate advisory links.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test module for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if test discovery requires explicit registration

## Implementation Notes
Follow the integration testing patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions.

Each test should:
1. Set up test data: insert an SBOM, insert advisories with known severity levels, link them via the `sbom_advisory` join table.
2. Call `GET /api/v2/sbom/{id}/advisory-summary`.
3. Assert the response status and JSON body match expectations.

Test cases to cover:
- SBOM with advisories at all four severity levels (critical, high, medium, low) — verify counts are correct.
- SBOM with advisories at only some severity levels — verify missing levels return 0.
- SBOM with no advisories — verify all counts are 0 and total is 0.
- Non-existent SBOM ID — verify 404 response.
- Duplicate advisory links (same advisory linked to the same SBOM multiple times) — verify deduplication produces correct counts.

Per CONVENTIONS.md §Testing: place integration tests in `tests/api/` and use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests; follow the same test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint tests; reference for how advisory test data is created
- `entity/src/sbom.rs` — SBOM entity for test data insertion
- `entity/src/advisory.rs` — advisory entity for test data insertion
- `entity/src/sbom_advisory.rs` — join table entity for linking test advisories to SBOMs

## Acceptance Criteria
- [ ] All test cases listed above are implemented and pass
- [ ] Tests use real PostgreSQL test database (not mocks)
- [ ] Tests verify both response status codes and JSON body content
- [ ] Deduplication behavior is explicitly tested
- [ ] `cargo test` passes with all new and existing tests

## Test Requirements
- [ ] Test: SBOM with advisories at all severity levels returns correct counts for each level and correct total
- [ ] Test: SBOM with advisories at only some severity levels returns 0 for missing levels
- [ ] Test: SBOM with no advisories returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Test: Non-existent SBOM ID returns HTTP 404
- [ ] Test: Duplicate advisory-SBOM links do not inflate counts (deduplication)

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — run only the new test module
- `cargo test` — run full test suite to verify no regressions

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
