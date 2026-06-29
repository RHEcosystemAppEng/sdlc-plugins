# Task 4 — Add integration tests for search improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the search improvements introduced by TC-9002.
The tests cover full-text search relevance ranking, filter query parameters, backward
compatibility with existing API consumers, and the interaction between filters and
full-text search. This addresses the non-functional requirement "Don't break existing
functionality" by explicitly verifying backward compatibility.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search relevance ranking, filter parameters (entity_type, severity, license), combined filters, backward compatibility, and edge cases (empty query, malformed input)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`. Examine the existing tests to understand the test harness setup (PostgreSQL test database, HTTP client, data seeding).
- Also examine sibling test files `tests/api/sbom.rs` and `tests/api/advisory.rs` for the established assertion patterns — the project uses `assert_eq!(resp.status(), StatusCode::OK)` style assertions.
- Test categories to implement:
  1. **Relevance ranking**: seed test data with varying relevance to a search term, verify that results are ordered by relevance score (most relevant first)
  2. **Entity type filter**: verify that `?entity_type=sbom` returns only SBOMs, `?entity_type=advisory` returns only advisories, `?entity_type=package` returns only packages
  3. **Severity filter**: verify that `?severity=critical` filters advisory results correctly
  4. **License filter**: verify that `?license=MIT` filters package results correctly
  5. **Combined filters**: verify AND semantics (e.g., `?entity_type=advisory&severity=high`)
  6. **Backward compatibility**: verify that existing endpoint behavior without any new parameters is unchanged — same response shape, same pagination behavior
  7. **Edge cases**: empty search query, search term with no matches, invalid filter values
- Seed test data that includes multiple entity types with varying attributes (different severities for advisories, different licenses for packages) to enable meaningful filter assertions.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9002, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §5.2 (Code Change Rules): inspect existing test code before modifying — follow the established patterns.
- Per docs/constraints.md §5.11: add a doc comment to every test function.
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions (tests with distinct setup, action, and assertion phases).

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests showing the test harness setup, data seeding, and assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrating the HTTP client usage and response assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests with data seeding patterns

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover full-text search relevance ranking (results ordered by score)
- [ ] Tests cover each filter parameter individually (entity_type, severity, license)
- [ ] Tests cover combined filters with AND semantics
- [ ] Tests verify backward compatibility (existing behavior without new parameters)
- [ ] Tests cover edge cases (empty query, no matches, invalid filter values)
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] All new integration tests pass in CI
- [ ] Tests do not depend on external state beyond the test database
- [ ] Test data seeding creates a representative dataset with multiple entity types and varying attributes
- [ ] Tests verify response status codes, result counts, and result ordering

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo test -p tests` — all integration tests pass (no regressions)

## Dependencies
- Depends on: Task 3 — Add filter query parameters to search endpoint (tests exercise the complete search stack including filters)
