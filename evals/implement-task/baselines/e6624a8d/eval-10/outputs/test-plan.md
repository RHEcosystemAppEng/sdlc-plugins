# Test Plan for TC-9208: Package License Summary Endpoint

## Test file

`tests/api/package_license.rs` -- new integration test file following sibling pattern (`tests/api/sbom.rs`, `tests/api/advisory.rs`).

## Assertion approach

### Value-based assertions (skill guidance overrides sibling pattern)

The sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` use existence-only checks (`.filter().any()` and `.count() > 0`). The skill's Step 7 explicitly requires value-based assertions and states that skill guidance overrides sibling patterns.

**Therefore, all assertions in these tests will:**
- Use `assert_eq!` to check exact counts and specific license identifiers
- Verify the actual content of response fields, not just that they are non-empty
- Ensure test failures reveal *what* changed, not just *how many*

### What we follow from siblings
- Status code checks: `assert_eq!(resp.status(), StatusCode::OK)` / `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response deserialization into typed `LicenseSummary` struct
- Test naming: `test_<endpoint>_<scenario>` pattern
- Database setup using the project's shared test infrastructure
- No parameterized tests (siblings do not use them)

### Documentation (skill-mandated)
- Every test function has a `///` doc comment
- Non-trivial tests include `// Given`, `// When`, `// Then` section markers

## Test cases

### Test 1: `test_license_summary_valid_sbom`

```rust
/// Verifies that a valid SBOM with known package licenses returns correctly
/// categorized and counted license identifiers.
#[tokio::test]
async fn test_license_summary_valid_sbom() {
    // Given an SBOM with packages having known licenses:
    //   - Package A: MIT (permissive)
    //   - Package B: GPL-3.0 (copyleft)
    //   - Package C: Apache-2.0 (permissive)
    //   - Package D: UnknownLicense-1.0 (unknown)
    // Seed the test database with this SBOM and its package-license mappings.

    // When requesting GET /api/v2/sbom/{id}/license-summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // And the response body contains correctly categorized licenses
    let summary: LicenseSummary = resp.json().await;

    // Permissive category
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Copyleft category
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0".to_string()]);

    // Unknown category
    assert_eq!(summary.unknown.count, 1);
    assert_eq!(summary.unknown.licenses, vec!["UnknownLicense-1.0".to_string()]);
}
```

**Assertion rationale**: Uses `assert_eq!` on exact counts and `.contains()` on specific license strings. This is value-based (not existence-only), so a regression that miscategorizes a license or changes a count will produce a clear failure message showing the expected vs. actual value.

### Test 2: `test_license_summary_nonexistent_sbom`

```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_license_summary_nonexistent_sbom() {
    // Given a random UUID that does not correspond to any SBOM
    let fake_id = Uuid::new_v4();

    // When requesting GET /api/v2/sbom/{fake_id}/license-summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Assertion rationale**: Direct status code check. This test is straightforward enough that value-based vs existence-based is not at issue -- it checks a single value (`StatusCode::NOT_FOUND`).

### Test 3: `test_license_summary_empty_sbom`

```rust
/// Verifies that an SBOM with no packages returns zero counts and empty license
/// lists for all categories.
#[tokio::test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM that exists but has no associated packages
    // Seed the test database with an SBOM but no sbom_package entries.

    // When requesting GET /api/v2/sbom/{id}/license-summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", empty_sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // And all categories have zero counts and empty lists
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 0);
    assert!(summary.permissive.licenses.is_empty());

    assert_eq!(summary.copyleft.count, 0);
    assert!(summary.copyleft.licenses.is_empty());

    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Assertion rationale**: Checks exact zero values and empty vectors. A regression that accidentally includes default or phantom licenses would be caught by the `is_empty()` and `count == 0` checks.

### Test 4: `test_license_summary_deduplication`

```rust
/// Verifies that duplicate licenses within a category are counted only once,
/// ensuring deduplication works correctly when multiple packages share the same license.
#[tokio::test]
async fn test_license_summary_deduplication() {
    // Given an SBOM with multiple packages sharing the same license:
    //   - Package A: MIT (permissive)
    //   - Package B: MIT (permissive) -- duplicate
    //   - Package C: MIT (permissive) -- duplicate
    //   - Package D: GPL-3.0 (copyleft)
    // Seed the test database with this SBOM and its package-license mappings.

    // When requesting GET /api/v2/sbom/{id}/license-summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", sbom_id)).await;

    // Then the response status is 200
    assert_eq!(resp.status(), StatusCode::OK);

    // And MIT appears only once in the permissive category despite 3 packages having it
    let summary: LicenseSummary = resp.json().await;

    assert_eq!(summary.permissive.count, 1, "MIT should be deduplicated to a single entry");
    assert_eq!(summary.permissive.licenses, vec!["MIT".to_string()]);

    // Copyleft has one distinct license
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0".to_string()]);

    // Unknown has none
    assert_eq!(summary.unknown.count, 0);
    assert!(summary.unknown.licenses.is_empty());
}
```

**Assertion rationale**: Uses `assert_eq!` on the count (expecting 1, not 3) and on the exact license list content. This directly tests the deduplication requirement. If deduplication breaks, the count would be 3 and the assertion message would clearly show `expected 1, got 3`.

## Why not follow the sibling assertion pattern

The sibling tests use patterns like:

```rust
let has_critical = result.items.iter().filter(|a| a.severity == "Critical").any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

This pattern only checks for existence. If applied to the license summary tests, it would look like:

```rust
let has_permissive = summary.permissive.count > 0;
assert!(has_permissive, "should have permissive licenses");
```

This would pass even if the count was wrong (e.g., 5 instead of 2) or if the wrong licenses were in the category. The skill's Step 7 explicitly warns that "Length checks alone hide regressions behind a passing count" and mandates value-based assertions. Since the skill states "Skill guidance overrides sibling patterns," we follow the skill's quality standard here.

## Test execution

```
cargo test --test package_license
```

All four tests must pass before proceeding to commit. If any test fails 3 times with the same error, stop and ask the user for guidance per the skill's Important Rules.
