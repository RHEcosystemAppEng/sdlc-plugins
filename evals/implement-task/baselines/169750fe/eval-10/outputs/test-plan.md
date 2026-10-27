# Test Plan — TC-9208: Package License Summary Tests

## Assertion Approach

Following the implement-task skill's Step 7 guidance, this test plan uses **value-based assertions** rather than the sibling `.filter().any()` / `.filter().count() > 0` existence-check patterns found in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

The skill's explicit quality standard states: "Prefer value-based assertions over length-only checks [...] Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*."

This means each test asserts on **specific license identifiers** and **exact counts** per category, not merely that a category is non-empty.

## Sibling Conventions Followed (Non-Conflicting)

- **Test naming**: `test_<verb>_<noun>_<scenario>` (from `advisory.rs`, `sbom.rs`)
- **Setup/teardown**: shared test database with per-test transaction rollback
- **Status assertions**: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Response parsing**: `.json::<LicenseSummaryResponse>()` deserialization
- **Test file location**: `tests/api/package_license.rs`
- **Test documentation**: every test function gets a `///` doc comment (skill standard, applied regardless of sibling practice)
- **Given/When/Then**: section comments inside non-trivial tests (skill standard)

## Sibling Convention Overridden

- **Assertion style**: siblings use `.filter().any()` and `.count() > 0`. This test plan uses `assert_eq!` on specific values. See `conventions.md` for conflict analysis.

## Test Cases

### Test 1: `test_get_license_summary_with_known_packages`

```rust
/// Verifies that the license summary endpoint returns correct categorized counts and identifiers for an SBOM with known package licenses.
#[test]
fn test_get_license_summary_with_known_packages() {
    // Given an SBOM with packages having known licenses:
    //   - "MIT" (permissive)
    //   - "Apache-2.0" (permissive)
    //   - "GPL-3.0-only" (copyleft)
    // (set up via test database fixtures)

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummaryResponse = resp.json().await;

    // Then permissive category has exactly 2 licenses
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Then copyleft category has exactly 1 license
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0-only".to_string()]);

    // Then unknown category is empty
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Why value-based**: asserts exact count (2 permissive, 1 copyleft, 0 unknown) and specific license identifiers ("MIT", "Apache-2.0", "GPL-3.0-only"). A regression that miscategorizes "MIT" as copyleft would be caught — the sibling `.any()` pattern would not catch this.

### Test 2: `test_get_license_summary_nonexistent_sbom`

```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
#[test]
fn test_get_license_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = uuid::Uuid::new_v4();

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Why value-based**: direct status code comparison with `assert_eq!` (consistent with sibling pattern — no conflict here).

### Test 3: `test_get_license_summary_empty_sbom`

```rust
/// Verifies that an SBOM with no packages returns all-zero counts and empty license lists.
#[test]
fn test_get_license_summary_empty_sbom() {
    // Given an SBOM with no associated packages

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", empty_sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummaryResponse = resp.json().await;

    // Then all categories have zero counts and empty license lists
    assert_eq!(summary.permissive.count, 0);
    assert!(summary.permissive.licenses.is_empty());
    assert_eq!(summary.copyleft.count, 0);
    assert!(summary.copyleft.licenses.is_empty());
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Why value-based**: asserts exact zero counts and empty vectors for all three categories, not merely that the response exists.

### Test 4: `test_get_license_summary_deduplicates_licenses`

```rust
/// Verifies that duplicate licenses within a category are counted only once.
#[test]
fn test_get_license_summary_deduplicates_licenses() {
    // Given an SBOM with multiple packages sharing the same license:
    //   - package-a: "MIT"
    //   - package-b: "MIT"
    //   - package-c: "Apache-2.0"

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", dedup_sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummaryResponse = resp.json().await;

    // Then permissive has exactly 2 unique licenses (MIT appears once, not twice)
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Then no other categories have entries
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.unknown.count, 0);
}
```

**Why value-based**: asserts the deduplicated count is exactly 2 (not 3), and verifies the exact license identifiers present. A sibling `.count() > 0` check would pass even if deduplication were broken (count 3 > 0 is still true).

## Summary

| Aspect | Sibling Pattern | This Test Plan | Rationale |
|--------|----------------|----------------|-----------|
| Assertion style | `.filter().any()`, `.count() > 0` | `assert_eq!` on exact values | Skill guidance: value-based assertions take precedence |
| Test naming | `test_<verb>_<noun>_<scenario>` | Same | Non-conflicting — adopted |
| Setup/teardown | Shared DB, transaction rollback | Same | Non-conflicting — adopted |
| Status checks | `assert_eq!(resp.status(), ...)` | Same | Non-conflicting — adopted |
| Response parsing | `.json::<T>()` | Same | Non-conflicting — adopted |
| Test documentation | None in siblings | `///` doc comment on every test | Skill standard (overrides sibling absence) |
| Test structure | No given/when/then | Given/When/Then comments | Skill standard for non-trivial tests |
