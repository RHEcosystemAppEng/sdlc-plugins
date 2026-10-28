# Test Plan for TC-9208

## Assertion Approach

### Skill Guidance Over Sibling Patterns

The sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`) use existence-only
assertion patterns (`.filter().any()` and `.filter().count() > 0`). These check that at
least one matching item exists but do not verify specific values, exact counts, or the
identity of matched items.

The implement-task skill's Step 7 explicitly states: "Prefer value-based assertions over
length-only checks." The skill further states: "Skill guidance overrides sibling patterns."

**Decision:** Use value-based assertions (`assert_eq!` on specific license names and exact
counts) instead of the sibling existence-check patterns. This ensures test failures reveal
exactly what changed, not just that something is missing.

### Adopted from Siblings

The following non-conflicting sibling conventions are adopted:
- Test file at `tests/api/package_license.rs`
- Test function names use `test_<description>` pattern
- Real PostgreSQL test database with provisioned fixture data
- HTTP status code validation: `assert_eq!(resp.status(), StatusCode::OK)`
- Descriptive assertion messages

---

## Test File: `tests/api/package_license.rs`

### Test 1: `test_license_summary_with_known_licenses`

**Requirement:** Test that a valid SBOM with known package licenses returns correct
categorized counts.

**Doc comment:** `/// Verifies that an SBOM with known package licenses returns correctly categorized counts and license identifiers.`

**Approach:**

```rust
/// Verifies that an SBOM with known package licenses returns correctly categorized
/// counts and license identifiers.
#[tokio::test]
async fn test_license_summary_with_known_licenses() {
    // Given an SBOM with packages having known licenses:
    //   - "MIT" (permissive)
    //   - "Apache-2.0" (permissive)
    //   - "GPL-3.0" (copyleft)
    //   - "Proprietary-XYZ" (unknown)
    // (provision test SBOM and package-license records in the test DB)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{id}/license-summary").await;

    // Then the response is successful
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then permissive category contains exactly MIT and Apache-2.0
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Then copyleft category contains exactly GPL-3.0
    assert_eq!(summary.copyleft.count, 1);
    assert_eq!(summary.copyleft.licenses, vec!["GPL-3.0".to_string()]);

    // Then unknown category contains exactly Proprietary-XYZ
    assert_eq!(summary.unknown.count, 1);
    assert_eq!(summary.unknown.licenses, vec!["Proprietary-XYZ".to_string()]);
}
```

**Why value-based:** Instead of `.filter(|c| c.count > 0).any()`, we assert on exact
counts (2, 1, 1) and specific license names ("MIT", "Apache-2.0", "GPL-3.0",
"Proprietary-XYZ"). A regression that miscategorizes a license or drops one from the
response will produce a clear failure message naming the expected vs actual value.

---

### Test 2: `test_license_summary_nonexistent_sbom`

**Requirement:** Test that a non-existent SBOM ID returns 404.

**Doc comment:** `/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.`

**Approach:**

```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_license_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the license summary
    let resp = client.get(&format!("/api/v2/sbom/{}/license-summary", fake_id)).await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

**Why value-based:** Status code is checked with `assert_eq!` on the exact status code,
not a boolean check like `assert!(resp.status().is_client_error())`.

---

### Test 3: `test_license_summary_empty_sbom`

**Requirement:** Test that an SBOM with no packages returns all zeros with empty license lists.

**Doc comment:** `/// Verifies that an SBOM with no packages returns zero counts and empty license lists for all categories.`

**Approach:**

```rust
/// Verifies that an SBOM with no packages returns zero counts and empty license lists
/// for all categories.
#[tokio::test]
async fn test_license_summary_empty_sbom() {
    // Given an SBOM that exists but has no associated packages
    // (provision an SBOM with no sbom_package records)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{id}/license-summary").await;

    // Then the response is successful
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then all categories have zero counts and empty lists
    assert_eq!(summary.permissive.count, 0);
    assert_eq!(summary.permissive.licenses, Vec::<String>::new());
    assert_eq!(summary.copyleft.count, 0);
    assert_eq!(summary.copyleft.licenses, Vec::<String>::new());
    assert_eq!(summary.unknown.count, 0);
    assert_eq!(summary.unknown.licenses, Vec::<String>::new());
}
```

**Why value-based:** Asserts exact zero counts and empty vectors, not just
`.count() == 0` or `.is_empty()`. This catches regressions where a default value
is incorrectly populated.

---

### Test 4: `test_license_summary_deduplicates_licenses`

**Requirement:** Test that duplicate licenses within a category are counted only once.

**Doc comment:** `/// Verifies that duplicate licenses within a category are deduplicated, appearing only once in the count and list.`

**Approach:**

```rust
/// Verifies that duplicate licenses within a category are deduplicated, appearing only
/// once in the count and list.
#[tokio::test]
async fn test_license_summary_deduplicates_licenses() {
    // Given an SBOM with multiple packages that share the same license:
    //   - Package A: "MIT"
    //   - Package B: "MIT"
    //   - Package C: "Apache-2.0"
    // (provision test SBOM with three packages, two sharing MIT)

    // When requesting the license summary
    let resp = client.get("/api/v2/sbom/{id}/license-summary").await;

    // Then the response is successful
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: LicenseSummary = resp.json().await;

    // Then permissive count reflects deduplicated licenses (MIT + Apache-2.0 = 2, not 3)
    assert_eq!(summary.permissive.count, 2);
    assert!(summary.permissive.licenses.contains(&"MIT".to_string()));
    assert!(summary.permissive.licenses.contains(&"Apache-2.0".to_string()));

    // Then MIT appears only once in the list (not duplicated)
    let mit_occurrences = summary.permissive.licenses.iter()
        .filter(|l| l.as_str() == "MIT")
        .count();
    assert_eq!(mit_occurrences, 1, "MIT should appear exactly once after deduplication");
}
```

**Why value-based:** Instead of checking `.count() > 0` for MIT, we assert the exact
deduplicated count is 2 (not 3), verify specific license names are present, and
explicitly confirm MIT appears exactly once. This catches both deduplication failures
(count = 3) and over-deduplication (count = 1 if Apache-2.0 were also dropped).

---

## Summary of Assertion Strategy

| Sibling Pattern (NOT adopted) | Skill-Guided Pattern (adopted) | Rationale |
|---|---|---|
| `.filter(\|a\| ...).any(\|_\| true)` | `assert_eq!(summary.permissive.count, 2)` | Exact count reveals what changed |
| `.filter(\|s\| ...).count() > 0` | `assert!(list.contains(&"MIT".to_string()))` | Specific value identifies missing item |
| `assert!(has_critical)` | `assert_eq!(category.licenses, vec![...])` | Full value comparison catches regressions |

The skill's "prefer value-based assertions" guidance takes precedence over sibling
`.filter().any()` and `.filter().count() > 0` patterns. Non-conflicting sibling
conventions (test naming, file location, setup/teardown, status code checks) are
followed throughout.
