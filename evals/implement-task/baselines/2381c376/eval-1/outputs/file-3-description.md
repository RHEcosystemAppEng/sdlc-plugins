# File 3: tests/api/advisory_summary.rs

## Operation: CREATE

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Sibling Reference

Follows the test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` for test setup, HTTP request construction, response assertion, and database seeding patterns.

## Detailed Changes

### Imports

```rust
use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;
// Additional imports for test helpers, app setup, database seeding
// (exact imports confirmed by inspecting sibling test files)
```

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisories at various severity levels.
#[tokio::test]
async fn test_severity_summary_returns_correct_counts() {
    // Given an SBOM with 2 critical, 1 high, 3 medium, and 0 low advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("adv-1", "critical"),
        ("adv-2", "critical"),
        ("adv-3", "high"),
        ("adv-4", "medium"),
        ("adv-5", "medium"),
        ("adv-6", "medium"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts for each severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a test app with no matching SBOM
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for a non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
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
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the sbom_advisory join table
/// are deduplicated when counting severity levels.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("adv-1", "critical"),
        ("adv-1", "critical"),  // duplicate link
        ("adv-2", "high"),
    ]).await;

    // When requesting the advisory severity summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // adv-1 counted once despite two links
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);  // 2 unique advisories, not 3 links
}
```

## Design Decisions

- **Value-based assertions**: Every test asserts on specific field values, not just collection lengths (skill guidance).
- **Given-when-then structure**: Each test has `// Given`, `// When`, `// Then` section comments (skill guidance for non-trivial tests).
- **Doc comments on every test**: `///` doc comment before each test function (skill standard, overrides sibling absence).
- **Separate test functions**: Each test case exercises different behavior (missing SBOM vs. empty advisories vs. duplicates), so individual functions are preferred over parameterization per Meszaros heuristic.
- **Status code assertions**: `assert_eq!(resp.status(), StatusCode::OK)` matches the sibling test pattern.
- **JSON deserialization**: `resp.json::<SeveritySummary>()` for strongly-typed response parsing.

## Conventions Applied

- `test_` prefix on all test function names
- `#[tokio::test]` async test annotation
- `assert_eq!` for all assertions (no `.any()` or length-only checks)
- Test file name matches domain concept: `advisory_summary.rs`
- Uses shared test setup helpers (e.g., `setup_test_app`) from sibling tests

## Note on Test Registration

The test file `tests/api/advisory_summary.rs` may need to be registered in `tests/api/mod.rs` (if one exists) or in `tests/Cargo.toml` depending on the project's test module structure. This would be identified during the scope containment check in Step 9 and flagged as an out-of-scope file for user approval.
