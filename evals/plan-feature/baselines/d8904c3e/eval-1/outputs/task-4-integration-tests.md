## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the success path with multiple severity levels, the 404 case for non-existent SBOMs, deduplication behavior, and the response shape contract. These tests follow the established integration test pattern in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/api/mod.rs` — add `mod sbom_advisory_summary;` to register the new test module (if a mod.rs exists; otherwise the test runner auto-discovers)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  1. Set up test data by ingesting an SBOM and linking advisories at various severity levels
  2. Call the endpoint via the test HTTP client
  3. Assert response status code and JSON body shape using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test scenarios to implement:
  1. **Happy path**: SBOM with advisories at critical (2), high (3), medium (1), low (0) — verify exact counts and total
  2. **Empty advisories**: SBOM with no linked advisories — verify all counts are 0 and total is 0
  3. **Not found**: non-existent SBOM UUID — verify 404 status code
  4. **Deduplication**: same advisory linked twice to the SBOM — verify it is counted once
  5. **Response shape**: verify JSON keys match `{ "critical", "high", "medium", "low", "total" }`
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test for SBOM endpoints; copy test setup patterns for SBOM creation
- `tests/api/advisory.rs` — reference integration test for advisory endpoints; copy test setup patterns for advisory creation and linking

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: success with multiple severities, empty advisories, SBOM not found (404), deduplication
- [ ] Tests verify the JSON response shape matches the API contract

## Test Requirements
- [ ] Integration test: happy path with advisories at multiple severity levels returns correct counts
- [ ] Integration test: SBOM with no advisories returns all-zero counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: duplicate advisory links are deduplicated in the count
- [ ] Integration test: response JSON shape matches `{ critical, high, medium, low, total }`

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
