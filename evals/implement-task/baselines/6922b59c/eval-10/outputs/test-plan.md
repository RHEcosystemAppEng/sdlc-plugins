# Test Plan for TC-9208

## Test File

`tests/api/package_license.rs`

## Assertion Approach: Value-Based Assertions

The sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`) use existence-only
assertion patterns (`.filter().any()` and `.filter().count() > 0`). These patterns
conflict with the implement-task skill's quality guidance, which requires value-based
assertions that verify specific values rather than just existence or counts.

**Skill guidance takes precedence over sibling patterns.** All tests below use
value-based assertions that assert on concrete expected values, so test failures reveal
exactly what changed.

## Test Cases

### Test 1: Valid SBOM with known package licenses returns correct categorized counts

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized counts and license identifiers.
#[tokio::test]
async fn test_license_summary_with_known_licenses() {
    // Given an SBOM with packages containing known licenses:
    //   - "MIT" (permissive), "Apache-2.0" (permissive), "GPL-3.0" (copyleft)
    // (set up test database with these fixture packages and licenses)

    // When requesting the license summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/license-summary", sbom_id))
        .send()
        .await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then the permissive category contains exactly MIT and Apache-2.0
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Then the copyleft category contains exactly GPL-3.0
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0".to_string()]);

    // Then the unknown category is empty
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Why value-based:** Asserts on the exact count (2 permissive, 1 copyleft, 0 unknown)
and verifies specific license identifiers appear in the correct category. A regression
that miscategorizes "MIT" as copyleft would fail with a clear message about which
license is wrong, not just "count mismatch."

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_license_summary_not_found() {
    // Given a UUID that does not correspond to any SBOM
    let fake_id = Uuid::new_v4();

    // When requesting the license summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/license-summary", fake_id))
        .send()
        .await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Why value-based:** Asserts on the exact status code `NOT_FOUND` rather than just
checking "not success." This is already value-based and consistent with sibling
convention.

### Test 3: SBOM with no packages returns all zeros with empty license lists

```rust
/// Verifies that an SBOM with no associated packages returns zero counts
/// and empty license lists for all categories.
#[tokio::test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM that exists but has no associated packages
    // (set up test database with an SBOM that has no sbom_package rows)

    // When requesting the license summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/license-summary", empty_sbom_id))
        .send()
        .await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then all categories have zero counts and empty lists
    assert_eq!(summary.permissive.count, 0);
    assert!(summary.permissive.licenses.is_empty());
    assert_eq!(summary.copyleft.count, 0);
    assert!(summary.copyleft.licenses.is_empty());
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Why value-based:** Asserts each category individually with exact zero counts and
empty lists, rather than a single "response is empty" check. If a regression introduces
a default license into the copyleft category, the test failure will point to the exact
category.

### Test 4: Duplicate licenses within a category are counted only once

```rust
/// Verifies that duplicate license identifiers within a category are
/// deduplicated -- each unique license appears exactly once.
#[tokio::test]
async fn test_license_summary_deduplication() {
    // Given an SBOM with multiple packages that all have "MIT" license
    // (e.g., 3 packages each with "MIT")

    // When requesting the license summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/license-summary", sbom_with_dupes_id))
        .send()
        .await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then MIT appears exactly once in the permissive category
    assert_eq!(summary.permissive.count, 1);
    assert_eq!(summary.permissive.licenses, vec!["MIT".to_string()]);

    // Then other categories remain empty
    assert_eq!(summary.copyleft.count, 0);
    assert!(summary.copyleft.licenses.is_empty());
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Why value-based:** Asserts that the count is exactly 1 (not 3) and the specific
license "MIT" is present. Without deduplication, count would be 3 -- this test catches
that regression by asserting on the exact value. The sibling pattern
`.filter(|l| l == "MIT").count() > 0` would pass regardless of whether deduplication
works, since at least one "MIT" would always be present.

## Sibling Pattern Comparison

| Aspect | Sibling Pattern | This Test Plan | Reason |
|--------|----------------|----------------|--------|
| Assertion style | `.filter().any()`, `.filter().count() > 0` | `assert_eq!` on exact values | Skill guidance: prefer value-based assertions |
| Status code checks | `assert_eq!(resp.status(), StatusCode::OK)` | Same | No conflict -- already value-based |
| Test file location | `tests/api/` | `tests/api/package_license.rs` | Follows sibling convention |
| Test naming | `test_` prefix, snake_case | Same | Follows sibling convention |
| Setup approach | Real PostgreSQL test database with fixtures | Same | Follows sibling convention |
| Doc comments | Not present on sibling tests | Added per skill guidance | Skill requires doc comments on every test |
| Given-When-Then | Not present in siblings | Added per skill guidance | Skill requires section comments for non-trivial tests |

## Parameterized Tests

The four test cases exercise different scenarios with different setup data and different
assertion targets. They do not share the same algorithm with different data -- each has
distinct fixture setup and distinct assertion structures. Per the Meszaros heuristic
(parameterize when tests share the same algorithm with different data), individual test
functions are appropriate here.
