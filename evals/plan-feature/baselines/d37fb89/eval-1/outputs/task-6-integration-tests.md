## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the happy path with multiple advisories at various severity levels, the 404 response for non-existent SBOMs, deduplication of advisories linked via multiple paths, the optional `threshold` query parameter filtering, and correct JSON response shape. These tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration test module for the advisory severity summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any additional test dependencies if needed (though likely none beyond what existing tests already use)

## Implementation Notes
Follow the established integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests:
1. Set up a test database with fixture data (SBOMs, advisories, and their relationships via the `sbom_advisory` join table)
2. Spin up the Axum server using a test configuration
3. Send HTTP requests using an HTTP client (likely `reqwest` or Axum's `TestServer`)
4. Assert on response status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern
5. Deserialize response bodies and assert on field values

Test fixture setup should:
- Create a test SBOM
- Create advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 0 low)
- Link them via the `sbom_advisory` join table
- For the deduplication test: link the same advisory to the SBOM via multiple paths (if the data model supports this)

Specific test cases:

1. **Happy path**: SBOM with advisories at known severity levels returns correct counts `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
2. **Empty SBOM**: SBOM with no linked advisories returns all zeros `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
3. **Not found**: Non-existent SBOM ID returns 404
4. **Deduplication**: Same advisory linked twice counts only once in the total
5. **Threshold filter — critical**: `?threshold=critical` returns only critical count, others are zero
6. **Threshold filter — high**: `?threshold=high` returns critical and high counts, medium and low are zero
7. **Cache header**: Response includes `Cache-Control` header with `max-age=300`

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint test patterns: test setup, fixture creation, response assertions
- `tests/api/advisory.rs` — Advisory endpoint test patterns: advisory fixture creation, severity field setup
- `entity/src/sbom_advisory.rs` — join table entity used to create test fixtures linking SBOMs to advisories
- `entity/src/advisory.rs` — advisory entity used to create test advisories with specific severity levels

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: happy path, empty SBOM, 404, deduplication, threshold filtering, cache headers
- [ ] Tests follow the existing `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- [ ] Test module is properly registered and discoverable by `cargo test`

## Test Requirements
- [ ] Test: SBOM with mixed-severity advisories returns correct counts
- [ ] Test: SBOM with no advisories returns all-zero counts
- [ ] Test: Non-existent SBOM ID returns 404 status
- [ ] Test: Duplicate advisory links are deduplicated in counts
- [ ] Test: `?threshold=critical` returns only critical counts
- [ ] Test: `?threshold=high` returns critical and high counts
- [ ] Test: Response includes `Cache-Control: public, max-age=300` header

## Verification Commands
- `cargo test -p trustify-tests -- advisory_summary` — all advisory summary integration tests pass

## Dependencies
- Depends on: Task 4 — Advisory summary caching (tests verify cache headers, so caching must be in place)

[sdlc-workflow] Description digest: sha256-md:009e816aae18401b2b3b1debda2c3d870c888fef261898e3d025be3148c9f193
