# File 6: tests/api/advisory_summary.rs

## Action: CREATE

## Pre-implementation Inspection

Before creating, would inspect sibling test files for convention conformance:

1. Read `tests/api/advisory.rs` -- understand test setup (database initialization, test client creation, fixture loading), assertion patterns, error case testing
2. Read `tests/api/sbom.rs` -- understand SBOM-related test setup, how test SBOMs and advisories are created
3. Check `tests/Cargo.toml` -- verify test dependencies and ensure the test module is registered

### Test module registration

Would check if `tests/api/` has a `mod.rs` or if tests are registered in `tests/Cargo.toml` as separate test targets. If a `mod.rs` exists, would need to add `mod advisory_summary;` -- this would be flagged as an out-of-scope file in Step 9's scope containment check and presented to the user for approval.

## File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

// Imports matching sibling test file patterns (determined by inspection)
// e.g., reqwest, StatusCode, test helpers, fixture utilities

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (e.g., 2 Critical, 1 High, 3 Medium, 1 Low)
    // Set up test database with SBOM, advisories, and sbom_advisory links

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And the response body contains correct severity counts
    // Parse JSON response as SeveritySummary
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 3);
    // assert_eq!(body.low, 1);
    // assert_eq!(body.total, 7);
}

/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    // (use a UUID/ID that does not exist in the test database)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // Set up test database with SBOM but no sbom_advisory links

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in severity counts.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links
    // (same advisory linked multiple times via sbom_advisory join table)
    // e.g., 1 Critical advisory linked twice, 1 High advisory linked once

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK
    // assert_eq!(resp.status(), StatusCode::OK);

    // And the duplicate advisory is counted only once
    // assert_eq!(body.critical, 1);  // not 2
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 2);  // not 3
}
```

## Design Decisions

### Test structure

- Each test follows given-when-then structure with `// Given`, `// When`, `// Then` section comments (skill guidance for non-trivial tests)
- Each test function has a `///` doc comment explaining what it verifies (skill guidance, overrides sibling pattern if siblings lack doc comments)
- Tests use `#[tokio::test]` for async test execution (matching Axum's async runtime)

### Assertion style

- **Value-based assertions**: Each test asserts on specific field values (`assert_eq!(body.critical, 2)`) rather than length checks. This follows the skill's explicit guidance to prefer value-based assertions over length-only checks.
- **Status code assertions**: `assert_eq!(resp.status(), StatusCode::OK)` matching the sibling test pattern documented in the repository conventions.

### Test coverage

Maps directly to the 4 test requirements from the task:

| # | Requirement | Test function |
|---|-------------|--------------|
| 1 | Valid SBOM with known advisories returns correct severity counts | `test_severity_summary_with_known_advisories` |
| 2 | Non-existent SBOM ID returns 404 | `test_severity_summary_nonexistent_sbom_returns_404` |
| 3 | SBOM with no advisories returns all zeros | `test_severity_summary_no_advisories_returns_zeros` |
| 4 | Duplicate advisory links are deduplicated | `test_severity_summary_deduplicates_advisories` |

### Parameterized tests

Considered but not used: the four test cases have different setup requirements (different fixture data, different assertions). They do not share the same algorithm with different data -- each has distinct setup and assertion logic. Per the Meszaros heuristic from the skill guidance, individual tests are more appropriate here.

### Test database setup

Tests use the same test database setup pattern found in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`). The exact setup mechanism (test fixtures, helper functions, database initialization) would be determined during sibling inspection in Step 4. Tests hit a real PostgreSQL test database, consistent with the repository's testing convention.

## Convention conformance

- File location: `tests/api/` directory, matching sibling test file placement
- File name: `advisory_summary.rs` -- snake_case, matches the domain feature name
- Test function names: `test_` prefix with descriptive snake_case names
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` matching repository convention
- Async tests: `#[tokio::test]` matching the async runtime
- Integration-style: hits HTTP endpoint through test client, not unit-testing internal methods

## Crate name resolution for running tests

To run these tests, would resolve the test crate name via:

```bash
cargo metadata --no-deps --format-version 1
```

Parse the JSON output and find the package whose `manifest_path` is `tests/Cargo.toml`. Use that package's `name` field (NOT the directory name) as the argument to:

```bash
cargo test -p <tests-crate-name>
```

This ensures the correct crate is targeted even if the `Cargo.toml` `[package]` name differs from the directory name, and avoids incorrectly using a virtual workspace manifest.
