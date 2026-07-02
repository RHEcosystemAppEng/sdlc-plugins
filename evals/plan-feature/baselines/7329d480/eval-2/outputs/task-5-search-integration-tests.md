# Task 5: Update search integration tests

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for all search improvements introduced by Tasks 1-4: relevance scoring, entity-type filtering, field-based filtering (severity, date range), and search performance with indexes. These tests extend the existing test suite in `tests/api/search.rs`.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for relevance scoring, entity-type filter, severity filter, date-range filter, filter composition, and backward compatibility

## Implementation Notes
Extend the existing integration tests in `tests/api/search.rs` following the established test patterns:

- Use the existing test infrastructure that hits a real PostgreSQL test database
- Follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern used in existing tests (see `tests/api/sbom.rs` and `tests/api/advisory.rs` for reference)
- Set up test data covering multiple entity types (SBOMs, advisories with varying severities, packages) with known content so relevance ordering can be verified
- Test each new feature independently and in combination

Test categories to cover:
1. **Relevance scoring**: Verify results are ordered by relevance when `sort=relevance` (default). Insert test documents with varying term frequency and confirm ordering.
2. **Entity-type filter**: Test `entity_type=sbom`, `entity_type=advisory`, `entity_type=package`, and multi-value `entity_type=sbom,advisory`. Verify that only the requested entity types appear in results.
3. **Severity filter**: Test `severity=high` with advisory test data at different severity levels. Confirm only matching advisories are returned.
4. **Date-range filter**: Test `from_date` and `to_date` with test data spanning different dates. Confirm only items in range are returned.
5. **Filter composition**: Test combining multiple filters (e.g., `entity_type=advisory&severity=high&sort=relevance`).
6. **Backward compatibility**: Verify existing search behavior (no filters) is preserved.
7. **Error handling**: Test invalid filter values return 400 status codes.

Per CONVENTIONS.md §Testing: Use integration tests in tests/api/ hitting a real PostgreSQL test database with assert_eq!(resp.status(), StatusCode::OK) pattern. Applies: task modifies `tests/api/search.rs` matching the convention's file path scope (tests/api/).

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for test setup patterns, HTTP client configuration, and assertion style
- `tests/api/advisory.rs` — Reference for advisory-specific test data setup and assertion patterns

## Dependencies
- Depends on: Task 1 — Add database indexes for search query performance
- Depends on: Task 2 — Implement relevance scoring in SearchService
- Depends on: Task 3 — Add entity-type filter to search API
- Depends on: Task 4 — Add field-based filters to search API

## Acceptance Criteria
- [ ] Integration tests exist for relevance scoring (default sort order)
- [ ] Integration tests exist for entity-type filtering (single and multi-value)
- [ ] Integration tests exist for severity filtering
- [ ] Integration tests exist for date-range filtering
- [ ] Integration tests exist for filter composition (multiple filters combined)
- [ ] Integration tests verify backward compatibility (no filters = all results)
- [ ] Integration tests verify error handling (invalid filter values return 400)
- [ ] All new tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Minimum 10 new test functions covering the categories listed in Implementation Notes
- [ ] Test data fixtures include at least 3 SBOMs, 3 advisories (with varying severities and dates), and 3 packages
- [ ] Each test is independent and does not rely on execution order

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo test -p tests` — full integration test suite passes (no regressions)
