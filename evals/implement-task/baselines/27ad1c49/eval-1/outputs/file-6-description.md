# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Pre-Implementation Inspection

1. `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` to see the existing advisory test patterns:
   - Test function signatures and attributes (`#[tokio::test]`, `#[test]`)
   - Test database setup and teardown patterns
   - HTTP client creation and request building
   - Response assertion patterns
2. `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` for cross-domain test pattern comparison.
3. Check `tests/Cargo.toml` for test dependencies (HTTP client, assertion libraries, test utilities).
4. Verify whether `tests/api/mod.rs` exists and needs a `mod advisory_summary;` declaration.

## Test Module Registration

If `tests/api/mod.rs` exists, add `mod advisory_summary;` to register the new test module. This would be an out-of-scope file modification -- flag for user approval in Step 9 scope containment check.

Similarly, if `tests/Cargo.toml` needs modification to include the new test file, flag as out-of-scope.

## File Contents

```rust
//! Integration tests for the advisory severity summary endpoint.

use common::model::SeveritySummary; // or the correct import path
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_returns_correct_counts() {
    // Given an SBOM with known advisories at specific severity levels
    let app = /* test app setup following sibling pattern */;
    let sbom_id = /* create test SBOM with linked advisories:
        2 Critical, 3 High, 1 Medium, 0 Low */;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 2, "expected 2 critical advisories");
    assert_eq!(body.high, 3, "expected 3 high advisories");
    assert_eq!(body.medium, 1, "expected 1 medium advisory");
    assert_eq!(body.low, 0, "expected 0 low advisories");
    assert_eq!(body.total, 6, "expected 6 total advisories");
}

/// Verifies that requesting a non-existent SBOM ID returns a 404 status.
#[tokio::test]
async fn test_severity_summary_returns_404_for_missing_sbom() {
    // Given a non-existent SBOM ID
    let app = /* test app setup following sibling pattern */;
    let nonexistent_id = /* UUID or ID that does not exist in the test DB */;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_returns_zeros_for_empty_sbom() {
    // Given an SBOM with no linked advisories
    let app = /* test app setup following sibling pattern */;
    let sbom_id = /* create test SBOM with no advisory links */;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = /* test app setup following sibling pattern */;
    let sbom_id = /* create test SBOM */;
    let advisory_id = /* create one Critical advisory */;
    /* link the advisory to the SBOM twice (duplicate sbom_advisory rows) */;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 1, "duplicate advisory should be counted once");
    assert_eq!(body.total, 1, "total should reflect deduplicated count");
}
```

## Test Conventions Applied

### From sibling analysis:
- Integration tests hit a real PostgreSQL test database (following `tests/api/advisory.rs` pattern)
- Status assertion: `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::NOT_FOUND`
- Response body parsed via `.json()` into the expected struct
- Test function naming: `test_<feature>_<scenario>` pattern

### From skill guidance (overrides sibling patterns where applicable):
- **Value-based assertions**: All tests assert on specific field values (`assert_eq!(body.critical, 2)`), not just collection lengths. This satisfies the skill's preference for value-based assertions.
- **Documentation comments**: Every test function has a `///` doc comment explaining what it verifies, regardless of whether sibling tests have them.
- **Given-When-Then comments**: All tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases.
- **Parameterized tests**: Not used here because each test case has different setup requirements (different SBOM/advisory configurations) and different assertion structures. They do not share the same algorithm with different data, so individual tests are appropriate per the Meszaros heuristic.

## Module-Level Test Execution

After writing tests, resolve the test crate name:

```bash
cargo metadata --no-deps --format-version 1
```

Find the package whose manifest or target source contains `tests/api/advisory_summary.rs`. Run:

```bash
cargo test -p <resolved-test-crate-name>
```

Hard stop on failure.
