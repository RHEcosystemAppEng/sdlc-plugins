# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint,
covering all 4 test requirements from the task description.

## Pre-implementation inspection

Before creating, inspect sibling test files to understand test patterns:
```
Read tests/api/advisory.rs
Read tests/api/sbom.rs
```

Understand:
- How test database setup/teardown works
- How test entities (SBOMs, advisories) are created
- How HTTP requests are made to the test server
- Assertion patterns for status codes and response bodies
- Whether `#[tokio::test]` or another async test macro is used
- Whether tests need explicit database cleanup or use transactions

Also check if `tests/api/mod.rs` exists and whether this new test file needs to
be registered there (e.g., `mod advisory_summary;`).

Additionally, check `tests/Cargo.toml` to understand test dependencies.

### Crate name resolution

To run tests, resolve the correct crate name:
```bash
cargo metadata --no-deps --format-version 1
```
From the output, find the package whose manifest path or target source directory
contains `tests/api/`. Use that package's `name` field for `cargo test -p <crate-name>`.
Do NOT derive the crate name from the nearest `Cargo.toml`, which may be a virtual
workspace manifest.

## Content

```rust
//! Integration tests for the advisory severity summary endpoint.

// Imports -- match sibling test file patterns
// (axum test utilities, status codes, test database helpers, entity creation helpers)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_valid_sbom_returns_correct_severity_counts() {
    // Given an SBOM linked to advisories with known severities:
    //   - 2 Critical, 1 High, 3 Medium, 0 Low
    // (Create SBOM and advisory entities in the test database,
    //  link them via sbom_advisory join table)

    // When requesting the advisory summary for that SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And the response body contains the correct severity counts
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 3);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 6);
}

/// Verifies that requesting a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID (e.g., a random UUID)

    // When requesting the advisory summary for that SBOM ID
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero counts.
#[tokio::test]
async fn test_sbom_with_no_advisories_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    // (Create an SBOM but do not link any advisories)

    // When requesting the advisory summary for that SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_duplicate_advisory_links_are_deduplicated() {
    // Given an SBOM linked to the same advisory twice via sbom_advisory
    //   - 1 Critical advisory linked twice
    // (Create SBOM and a single Critical advisory, insert two sbom_advisory rows)

    // When requesting the advisory summary for that SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And the critical count is 1, not 2 (deduplicated)
    // assert_eq!(body.critical, 1);
    // assert_eq!(body.total, 1);
}
```

## Design decisions

- **Value-based assertions**: Every test asserts on specific field values (`assert_eq!(body.critical, 2)`) rather than length-only checks. This is per skill guidance which overrides sibling patterns if siblings use `.len()` or `.any()`.
- **Doc comments**: Every test function has a `///` doc comment per skill guidance, even if sibling tests lack them.
- **Given-when-then**: All tests use `// Given`, `// When`, `// Then` section comments for readability. All four tests are non-trivial (distinct setup, action, assertion phases).
- **No parameterized tests**: The four test cases exercise different behaviors and setups (valid SBOM, non-existent SBOM, empty SBOM, deduplication) -- they do not share the same algorithm with different data. Individual test functions are appropriate per the Meszaros heuristic.
- **Test database**: Tests create entities in the test database and make real HTTP requests, matching the sibling test pattern.
- **Test module registration**: If `tests/api/mod.rs` exists, add `mod advisory_summary;` to it. If tests are auto-discovered (no mod.rs), no registration needed.

## Convention conformance

- File naming: `advisory_summary.rs` matches the snake_case pattern of siblings (`advisory.rs`, `sbom.rs`)
- Async test macro: `#[tokio::test]` matches sibling pattern
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` matches sibling pattern
- Test function naming: `test_` prefix with descriptive name matches sibling pattern
- Response body parsed as JSON and individual fields asserted
