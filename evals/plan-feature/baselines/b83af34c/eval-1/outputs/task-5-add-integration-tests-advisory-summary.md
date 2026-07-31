## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path with correct severity counts, 404 for nonexistent SBOM, deduplication of advisories, threshold query parameter filtering, and cache header presence. Tests run against a real PostgreSQL test database following the project's integration test patterns.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if needed for test binary configuration

## Implementation Notes
Create integration tests in `tests/api/sbom_advisory_summary.rs` following the patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Each test should:
1. Set up test data by ingesting an SBOM and linking advisories with known severities
2. Call `GET /api/v2/sbom/{id}/advisory-summary`
3. Assert on the response status code and JSON body

Test cases to implement:
- **Happy path**: Ingest SBOM with advisories at multiple severity levels, verify counts match
- **Empty result**: SBOM exists but has no linked advisories, verify all counts are zero
- **404**: Request summary for a nonexistent SBOM ID, verify 404 status
- **Deduplication**: Link the same advisory to an SBOM twice, verify it is counted only once
- **Threshold filter**: Use `?threshold=high`, verify only critical and high counts are non-zero
- **Cache header**: Verify `Cache-Control: max-age=300` header is present in the response

Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns per project conventions.

Per CONVENTIONS.md §Framework: use Axum test utilities for HTTP request construction. Applies: task modifies `tests/api/sbom_advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Module pattern: place tests in the `tests/api/` directory following existing test module structure. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: assert correct error responses (404 status) for invalid inputs. Applies: task modifies `tests/api/sbom_advisory_summary.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom_advisory_summary.rs` matching the convention's `tests/api/` directory scope.

Per CONVENTIONS.md §Caching: verify cache-control headers are correctly set on the endpoint response. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests to follow as a pattern for test setup and assertions
- `tests/api/advisory.rs` — existing advisory endpoint tests for advisory data setup patterns

## Acceptance Criteria
- [ ] All test cases pass against a PostgreSQL test database
- [ ] Tests cover: happy path, empty result, 404, deduplication, threshold filter, cache header
- [ ] Tests follow existing integration test patterns in `tests/api/`
- [ ] No test data pollution — each test cleans up or uses isolated data

## Test Requirements
- [ ] Happy path test with multiple severity levels returns correct counts
- [ ] Empty advisory set returns all-zero counts
- [ ] Nonexistent SBOM returns 404 status
- [ ] Duplicate advisory linking produces correct deduplicated count
- [ ] Threshold query parameter filters counts correctly
- [ ] Cache-Control header has max-age=300

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
