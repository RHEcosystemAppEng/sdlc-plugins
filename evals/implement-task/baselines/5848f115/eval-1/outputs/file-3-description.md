# File 3: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all 4 test requirements.

## Pre-implementation analysis

Before creating this file, inspect sibling test files to discover test conventions:
- Read `tests/api/advisory.rs` via `mcp__serena_backend__get_symbols_overview` and then `mcp__serena_backend__find_symbol` on 2-3 test functions with `include_body=true` to understand assertion patterns, test setup, fixture creation, and naming conventions.
- Read `tests/api/sbom.rs` via `mcp__serena_backend__get_symbols_overview` and `find_symbol` to confirm cross-entity test patterns (especially 404 handling and response validation).
- Check `tests/Cargo.toml` via Read to understand test dependencies and any test utility crates.

## Detailed changes

Create the file with 4 test functions:

### Test 1: `test_advisory_summary_with_known_advisories`

```rust
/// Verifies that an SBOM with known advisories returns correct severity counts per level.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test database with SBOM, link advisories with Critical=2, High=1, Medium=3, Low=0)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response contains correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: `test_advisory_summary_sbom_not_found`

```rust
/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let sbom_id = "non-existent-id";

    // When requesting the advisory summary
    let resp = client.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;

    // Then a 404 status is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: `test_advisory_summary_no_advisories`

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    // (set up test database with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: `test_advisory_summary_deduplicates_advisories`

```rust
/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with the same advisory linked multiple times
    // (set up test database with SBOM, link the same Critical advisory twice)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.total, 1);
}
```

## Conventions applied

- Test naming follows `test_<endpoint>_<scenario>` pattern (matching `tests/api/advisory.rs` and `tests/api/sbom.rs`)
- Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling tests
- Value-based assertions on specific field values (per skill Step 7 guidance -- assert on actual values, not just lengths)
- Each test has a `///` doc comment (per skill Step 7 -- document every test function)
- Given-when-then section comments in each test body (per skill Step 7 -- non-trivial tests with distinct phases)
- Individual test functions rather than parameterized tests (matching sibling convention -- no `#[rstest]` usage observed)
- Integration tests hit a real PostgreSQL test database (matching `tests/api/` convention)
