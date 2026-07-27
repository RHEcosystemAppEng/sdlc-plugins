# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all four test requirements from the task description.

## Pre-implementation inspection

Before creating, inspect sibling test files to understand test conventions:
1. `tests/api/advisory.rs` -- Advisory endpoint integration tests: test setup, assertion patterns, response deserialization, 404 handling.
2. `tests/api/sbom.rs` -- SBOM endpoint integration tests: test setup for SBOM-related tests, data seeding patterns.
3. `tests/api/search.rs` -- Search endpoint integration tests: additional pattern confirmation.

Also check `tests/Cargo.toml` to understand test dependencies and `tests/api/mod.rs` (if it exists) to see if the new test module needs to be registered.

## File contents

```rust
use reqwest::StatusCode;
use serde::Deserialize;

/// Response struct for deserializing the advisory summary endpoint response in tests.
#[derive(Debug, Deserialize)]
struct SeveritySummaryResponse {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    //   - Seed test database with an SBOM
    //   - Create advisories: 2 critical, 3 high, 1 medium, 0 low
    //   - Link advisories to the SBOM via sbom_advisory join table

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummaryResponse = resp.json().await
        .expect("Failed to deserialize response");

    assert_eq!(summary.critical, 2, "Expected 2 critical advisories");
    assert_eq!(summary.high, 3, "Expected 3 high advisories");
    assert_eq!(summary.medium, 1, "Expected 1 medium advisory");
    assert_eq!(summary.low, 0, "Expected 0 low advisories");
    assert_eq!(summary.total, 6, "Expected 6 total advisories");
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for the non-existent SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    //   - Seed test database with an SBOM but no advisory links

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 200 OK with all zero counts
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummaryResponse = resp.json().await
        .expect("Failed to deserialize response");

    assert_eq!(summary.critical, 0, "Expected 0 critical advisories");
    assert_eq!(summary.high, 0, "Expected 0 high advisories");
    assert_eq!(summary.medium, 0, "Expected 0 medium advisories");
    assert_eq!(summary.low, 0, "Expected 0 low advisories");
    assert_eq!(summary.total, 0, "Expected 0 total advisories");
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    //   - Seed test database with an SBOM
    //   - Create 1 critical advisory
    //   - Link the same advisory to the SBOM multiple times in sbom_advisory

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should count the advisory only once
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: SeveritySummaryResponse = resp.json().await
        .expect("Failed to deserialize response");

    assert_eq!(summary.critical, 1, "Duplicate advisory should be counted only once");
    assert_eq!(summary.total, 1, "Total should reflect deduplicated count");
}
```

## Design decisions

- **Separate test functions (not parameterized):** Sibling test files in `tests/api/` use individual test functions, not `#[rstest]` parameterized tests. Following the established project convention.
- **`tokio::test` attribute:** Integration tests are async, matching the pattern in sibling test files.
- **Value-based assertions:** Each test asserts on specific field values (not just response status or body length), following SKILL.md guidance to "prefer value-based assertions over length-only checks."
- **Assertion messages:** Each `assert_eq!` includes a descriptive message string for clear failure diagnostics.
- **Given-When-Then comments:** Non-trivial tests include `// Given`, `// When`, `// Then` section comments for structure clarity.
- **Doc comments on every test:** `///` doc comment before each test function explaining what it verifies.
- **Local response struct:** `SeveritySummaryResponse` is defined locally in the test file for deserialization, avoiding coupling test compilation to the main crate's model (matching how sibling tests handle response types).

## Conventions applied

- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization -- matching sibling tests
- **Error cases:** 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` -- matching sibling tests
- **Test naming:** `test_severity_summary_<scenario>` pattern -- matching `test_<endpoint>_<scenario>` convention
- **Test setup:** Seed test database with fixtures before assertions -- matching sibling test setup patterns
