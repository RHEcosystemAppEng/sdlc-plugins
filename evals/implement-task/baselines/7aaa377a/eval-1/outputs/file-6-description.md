# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all test requirements from the task description.

## Content

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds an SBOM with advisories at known severity levels and asserts the response
/// contains the expected count for each severity.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories:
    //   - 2 Critical, 3 High, 1 Medium, 0 Low
    let sbom_id = seed_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "High"),
        ("adv-5", "High"),
        ("adv-6", "Medium"),
    ]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404.
///
/// Uses a UUID that does not correspond to any seeded SBOM and asserts the
/// endpoint responds with HTTP 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
///
/// Seeds an SBOM with no linked advisories and asserts every severity field
/// and total are zero.
#[tokio::test]
async fn test_advisory_summary_empty_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = seed_sbom_with_advisories(vec![]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
///
/// Seeds an SBOM with the same advisory linked multiple times and asserts
/// the advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links
    //   - adv-1 (Critical) linked twice
    //   - adv-2 (High) linked three times
    let sbom_id = seed_sbom_with_duplicate_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-1", "Critical"),  // duplicate
        ("adv-2", "High"),
        ("adv-2", "High"),      // duplicate
        ("adv-2", "High"),      // duplicate
    ]);

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then counts reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);  // adv-1 counted once
    assert_eq!(body["high"], 1);      // adv-2 counted once
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);     // 2 unique advisories
}
```

## Pattern Compliance

- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Response validation**: deserializes body to `serde_json::Value` and asserts on specific field values (not just counts/lengths)
- **Error cases**: includes 404 test for non-existent SBOM, consistent with existing endpoint test patterns
- **Test naming**: follows `test_<endpoint>_<scenario>` convention (e.g., `test_advisory_summary_valid_sbom`)
- **Test organization**: all tests for this endpoint in a single file under `tests/api/`
- **Documentation**: every test function has a `///` doc comment explaining what it verifies, per skill requirements
- **Given-when-then**: each test with non-trivial setup uses `// Given`, `// When`, `// Then` section comments
- **No parameterized tests**: sibling test files do not use `#[rstest]`, so individual test functions are used
- **Value assertions**: asserts on specific severity count values (e.g., `assert_eq!(body["critical"], 2)`) rather than just checking length, per skill requirement for value-based assertions

## Test Coverage Matrix

| Test Requirement | Test Function | Covered |
|---|---|---|
| Valid SBOM with known advisories returns correct severity counts | `test_advisory_summary_valid_sbom` | Yes |
| Non-existent SBOM ID returns 404 | `test_advisory_summary_nonexistent_sbom` | Yes |
| SBOM with no advisories returns all zeros | `test_advisory_summary_empty_advisories` | Yes |
| Duplicate advisory links are deduplicated | `test_advisory_summary_deduplicates` | Yes |

## Impact

- New file, no existing code affected
- Tests require the same PostgreSQL test database setup used by sibling test files
- `tests/Cargo.toml` may need a `mod advisory_summary;` addition or the test file may be auto-discovered depending on the test harness configuration
