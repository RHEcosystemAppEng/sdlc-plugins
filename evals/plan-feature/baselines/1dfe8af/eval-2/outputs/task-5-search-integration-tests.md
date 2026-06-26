## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search integration test suite to cover the new search performance, relevance ranking, and filtering capabilities added in Tasks 1-4. The existing tests in `tests/api/search.rs` cover basic search functionality; this task adds comprehensive coverage for the new features and verifies backward compatibility.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for: relevance-ranked result ordering, filter parameter application (severity, date range, package name, license), filter combination (AND semantics), invalid filter parameter handling, and performance baseline assertions

## Implementation Notes
Follow the existing integration test pattern in `tests/api/search.rs` and the other test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the project conventions.

Test scenarios to add:

**Relevance ranking tests:**
- Search for a term that matches one entity exactly and another partially; verify the exact match appears first in the response
- Search for advisories with equal text relevance but different severities; verify higher severity ranks first

**Filter tests:**
- Apply severity filter and verify only matching advisories are returned
- Apply date range filter and verify only entities within the range are returned
- Apply package name filter with a partial string and verify case-insensitive matching
- Apply license filter and verify exact match behavior
- Combine multiple filters and verify AND semantics (all conditions must match)
- Submit invalid filter values (e.g., non-ISO-8601 date) and verify 400 response

**Backward compatibility tests:**
- Verify that search requests without any filter parameters return the same results as before
- Verify that the response schema has not changed (PaginatedResults wrapper from `common/src/model/paginated.rs`)

**Assumption (pending clarification):** Performance assertions (e.g., "search completes within 500ms") are included as soft assertions with generous timeouts, since no specific performance target was provided in TC-9002.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests to follow as pattern for setup, assertion style, and test database interaction
- `tests/api/sbom.rs` — Example of entity-specific integration test patterns
- `tests/api/advisory.rs` — Example of advisory-specific test data setup

## Acceptance Criteria
- [ ] At least 2 integration tests for relevance ranking behavior
- [ ] At least 4 integration tests for individual filter parameters
- [ ] At least 1 integration test for combined filters with AND semantics
- [ ] At least 1 integration test for invalid filter parameter handling (400 response)
- [ ] At least 1 backward compatibility test (no filters = same behavior as before)
- [ ] All new tests pass against the test database
- [ ] All existing tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] All new tests follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern
- [ ] Test data setup creates entities with known, deterministic values for reliable assertions
- [ ] Tests are independent and can run in any order

## Verification Commands
- `cargo test --test api -- search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database search index for full-text search performance
- Depends on: Task 2 — Implement search result ranking and relevance scoring
- Depends on: Task 4 — Implement filter logic in SearchService

[sdlc-workflow] Description digest: sha256-md:b5f0e8d2a4c716359012abcdef7654321098fedc7654321098fedcba76543210
