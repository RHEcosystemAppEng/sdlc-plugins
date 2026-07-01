## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria: correct severity aggregation, deduplication, 404 for missing SBOMs, cache headers, and response time validation. These tests hit a real PostgreSQL test database following the established integration test pattern.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
- Test data setup: create an SBOM, create advisories at each severity level (Critical, High, Medium, Low), and link them to the SBOM via the `sbom_advisory` relationship. Use the existing test data creation patterns from `tests/api/sbom.rs`.
- Test deduplication: link the same advisory to the SBOM multiple times and verify it is counted only once.
- Test 404: use a non-existent SBOM ID and verify `StatusCode::NOT_FOUND`.
- Test cache headers: verify the response includes `Cache-Control` headers with `max-age=300`.
- Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database; use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test structure, setup, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; shows how to create test advisories with severity data
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for test data setup

## Acceptance Criteria
- [ ] Integration test verifying 200 response with correct severity counts for an SBOM with advisories at each severity level
- [ ] Integration test verifying advisory deduplication (same advisory counted once)
- [ ] Integration test verifying 404 for non-existent SBOM ID
- [ ] Integration test verifying cache control headers in response
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: SBOM with 4 advisories (one per severity) returns `{ critical: 1, high: 1, medium: 1, low: 1, total: 4 }`
- [ ] Test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: SBOM with duplicate advisory links returns correct deduplicated counts
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: response contains `Cache-Control: max-age=300` header

## Verification Commands
- `cargo test --test api advisory_summary` — run the advisory summary integration tests

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
