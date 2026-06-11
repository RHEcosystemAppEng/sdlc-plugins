# File 3: tests/api/advisory_summary.rs

**Action:** CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all test requirements from the task description.

## Detailed Changes

### Test functions

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_get_advisory_summary_with_known_advisories() {
    // Given an SBOM with known advisories at various severity levels
    //   - 2 Critical, 3 High, 1 Medium, 0 Low advisories seeded in the test DB
    let sbom_id = seed_sbom_with_advisories(&db, vec![
        ("ADV-001", Severity::Critical),
        ("ADV-002", Severity::Critical),
        ("ADV-003", Severity::High),
        ("ADV-004", Severity::High),
        ("ADV-005", Severity::High),
        ("ADV-006", Severity::Medium),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary for that ID
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    let sbom_id = seed_sbom_without_advisories(&db).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links for the same advisory are deduplicated in the count.
#[tokio::test]
async fn test_get_advisory_summary_deduplicates() {
    // Given an SBOM linked to the same advisory multiple times via sbom_advisory
    let sbom_id = seed_sbom_with_duplicate_advisory_links(&db, vec![
        ("ADV-100", Severity::High),
        ("ADV-100", Severity::High),  // duplicate link
        ("ADV-101", Severity::Low),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);    // ADV-100 counted once
    assert_eq!(summary.low, 1);     // ADV-101 counted once
    assert_eq!(summary.total, 2);   // 2 unique advisories
}
```

### Design rationale

- **Value-based assertions:** Every test asserts on specific field values (`assert_eq!(summary.critical, 2)`), not just collection lengths. This follows the skill requirement to prefer value-based assertions over length-only checks.
- **Given-When-Then structure:** Each non-trivial test uses `// Given`, `// When`, `// Then` section comments for navigability.
- **Doc comments:** Every test function has a `///` doc comment explaining what it verifies.
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern consistent with siblings `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Assertion pattern:** Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the sibling test convention.
- **Real database:** Tests use the PostgreSQL test database, not mocks, consistent with the project's integration test approach.

### Conventions followed

- Test file location in `tests/api/` matches sibling test files.
- 404 test included for non-existent entity, matching pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Async test functions with `#[tokio::test]` matching the project's async runtime.
