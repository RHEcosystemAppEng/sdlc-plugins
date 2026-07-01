## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria: correct severity counts, 404 for unknown SBOMs, threshold filtering, advisory deduplication, and cache header behavior. These tests complement any unit tests added in earlier tasks and provide end-to-end validation against a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation.
- Test data setup: create an SBOM, create advisories at different severity levels, and link them via the `sbom_advisory` relationship. Use the existing test helper infrastructure visible in sibling test files.
- Test cases to implement:
  1. **Happy path**: SBOM with advisories at all four severity levels returns correct counts and total
  2. **Empty SBOM**: SBOM with no linked advisories returns all zeros
  3. **404**: Non-existent SBOM ID returns 404
  4. **Deduplication**: SBOM with duplicate advisory links returns deduplicated counts
  5. **Threshold filtering**: `?threshold=critical` returns only critical count; `?threshold=high` returns critical and high; etc.
  6. **Cache headers**: Response includes cache-control headers with 5-minute TTL
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM-related test setup patterns, HTTP client configuration, and assertion style
- `tests/api/advisory.rs` — reference for advisory-related test data creation and endpoint testing patterns
- `tests/api/search.rs` — additional reference for integration test structure

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] Tests cover: happy path, empty SBOM, 404, deduplication, threshold filtering, cache headers
- [ ] All tests pass against a PostgreSQL test database
- [ ] Test patterns are consistent with existing tests in `tests/api/`

## Test Requirements
- [ ] Happy path test: SBOM with known advisories returns expected severity counts
- [ ] Empty SBOM test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] 404 test: request with non-existent SBOM ID returns 404 status
- [ ] Deduplication test: SBOM with duplicate advisory links does not double-count
- [ ] Threshold test: `?threshold=high` returns zero for medium and low
- [ ] Cache header test: response includes cache-control with 300-second max-age

## Verification Commands
- `cargo test -p trustify-tests --test advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256-md:6b88aa9521a86f65a8b92375c726958e3798731968c2335b7ad74c346a703d5f
