# File 6: Create `tests/api/advisory_summary.rs`

## Action: CREATE

## Purpose

Write integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all four test requirements.

## Detailed Changes

Create a new test file following the patterns in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Sets up an SBOM linked to advisories with known severity levels and asserts
/// that each severity count and the total match expectations.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM linked to advisories with known severities:
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories
    // (Set up test SBOM and advisory records in the test database,
    //  create sbom_advisory join records linking them)

    // When requesting the advisory summary for this SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 3);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for this ID
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_advisories() {
    // Given an SBOM with no linked advisories
    // (Set up test SBOM with no sbom_advisory join records)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
///
/// When the same advisory is linked to an SBOM multiple times (e.g., through
/// different vulnerability paths), it should only be counted once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with the same advisory linked twice
    // (Create one advisory with "High" severity, then create two
    //  sbom_advisory join records pointing to the same advisory)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.high, 1);  // Not 2, despite two join records
    assert_eq!(body.total, 1);
}
```

## Key Implementation Details

1. **Test database setup**: each test sets up its own test data in the PostgreSQL test database, following the pattern in sibling test files. The exact fixture creation API would be determined by reading the setup code in `tests/api/sbom.rs` and `tests/api/advisory.rs`.

2. **HTTP client**: uses the test HTTP client pattern from sibling tests to make requests against the test server.

3. **Value-based assertions**: asserts on specific field values (not just `items.len()`), following the skill instruction to "prefer value-based assertions over length-only checks."

4. **All four test requirements covered**:
   - Valid SBOM with known advisories -> correct severity counts
   - Non-existent SBOM ID -> 404
   - SBOM with no advisories -> all zeros
   - Duplicate advisory links -> deduplicated count

5. **Registration**: the test file may also need to be registered in `tests/api/mod.rs` or `tests/Cargo.toml` depending on how the test suite is structured. Inspect sibling test files for the registration pattern.

## Conventions Applied

- **Test naming**: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests.
- **Error case**: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` consistent with sibling tests.
- **Documentation**: every test function has a `///` doc comment explaining what it verifies.
- **Given-When-Then**: non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **Async tests**: uses `#[tokio::test]` for async test functions, consistent with the Axum-based async runtime.
