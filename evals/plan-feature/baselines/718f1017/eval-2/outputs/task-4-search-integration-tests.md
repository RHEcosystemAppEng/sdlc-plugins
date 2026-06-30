## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search ranking, filter query parameters, and backward compatibility with the existing search API contract. This task ensures the search improvements from TC-9002 are verified end-to-end against a real PostgreSQL test database, following the project's established integration test patterns.

## Files to Modify
- `tests/api/search.rs` — extend existing search integration tests with new test cases for full-text ranking, filter parameters, and backward compatibility

## Implementation Notes
- The existing integration tests in `tests/api/search.rs` follow the project's test pattern: they hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response validation.
- Follow the test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test structure, test data setup, and assertion style.
- Test data setup: ingest test SBOMs, advisories, and packages with known content so that search queries produce deterministic results. Use the ingestor service (`modules/ingestor/src/service/mod.rs`) to set up test data.
- For relevance ranking tests: create entities with the search term in the title vs. only in the description, then verify that the title match appears first in results.
- For filter tests: create entities of different types and with different severity/license values, then verify that filters correctly narrow results.
- For backward compatibility: verify that existing search queries (without filter parameters) continue to return the same result shape.
- Per CONVENTIONS.md (repo-level): integration tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Follow this consistently.
  Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests; extend rather than rewrite
- `tests/api/sbom.rs` — SBOM integration test patterns for test data setup, HTTP request construction, and response assertion
- `tests/api/advisory.rs` — advisory integration test patterns; similar structure to follow
- `modules/ingestor/src/service/mod.rs::IngestorService` — service for ingesting test SBOM and advisory data during test setup

## Acceptance Criteria
- [ ] Integration tests verify that full-text search returns results ranked by relevance
- [ ] Integration tests verify that entity type filter narrows results to the specified type
- [ ] Integration tests verify that severity filter narrows advisory results
- [ ] Integration tests verify that license filter narrows package results
- [ ] Integration tests verify backward compatibility — queries without filters return the same response shape as before
- [ ] All existing search tests continue to pass (no regressions)

## Test Requirements
- [ ] Test: search for a term present in advisory title and SBOM description — advisory appears first (relevance ranking)
- [ ] Test: search with `entity_type=advisory` excludes SBOM and package results
- [ ] Test: search with `entity_type=package` excludes SBOM and advisory results
- [ ] Test: search with `severity=critical` returns only critical-severity advisories
- [ ] Test: search with `license=MIT` returns only MIT-licensed packages
- [ ] Test: search with multiple filters applied simultaneously returns correctly intersected results
- [ ] Test: search without any filter parameters returns results from all entity types
- [ ] Test: search with empty query string and filters applied returns filtered results without errors
- [ ] Test: pagination with filters returns consistent ordering across pages

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo test -p tests` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search (tests depend on the new search implementation)
- Depends on: Task 3 — Add search filter support (tests cover filter functionality)

<!-- [sdlc-workflow] Description digest: sha256-md:347d6d1b0c0cd2c7693dacc94914e352b41268f5715b771a93fa03e822e09eda -->
