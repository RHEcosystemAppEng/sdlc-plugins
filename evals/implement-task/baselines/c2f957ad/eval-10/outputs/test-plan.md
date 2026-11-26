# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach

- **Kept from siblings**: integration tests against the real PostgreSQL test database, using the same harness, fixture and ingest helpers as `tests/api/sbom.rs` and `tests/api/advisory.rs`. Status checks use `assert_eq!(resp.status(), StatusCode::...)`. The body is deserialized into `LicenseSummary`. Test names use the `test_*` pattern.
- **Assertion style — value-based (skill guidance overrides siblings)**: the sibling tests assert existence only, with `.filter(..).any(|_| true)` + `assert!` or `.filter(..).count()` + `assert!(n > 0)`. Those checks pass even when the wrong licenses, wrong categories or wrong counts come back. Under Step 7 ("prefer value-based assertions over length-only checks"), the new tests:
  - build an **expected `LicenseSummary`** from the known fixture data and compare it with `assert_eq!(summary, expected)`. A failure then shows a full diff of what changed. (`LicenseSummary` derives `PartialEq` and `Debug`, and `licenses` is sorted via `BTreeSet`, so equality is deterministic.)
  - where a per-field check is clearer, assert exact values such as `assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"])` and `assert_eq!(summary.permissive.count, 2)`, never only `count > 0` or `!is_empty()`.
  - no `.any(|_| true)`, `count() > 0` or other existence-only assertions.
- **Documentation**: every test gets a `///` doc comment. Non-trivial tests get `// Given` / `// When` / `// Then` sections.
- **Parameterization**: none. Siblings do not use `rstest`, and the four cases differ in setup and assertions, so the Meszaros heuristic favors separate tests.
- **Fixture/assertion consistency**: assertions are derived from the fixture's actual licenses and the Acceptance Criteria only. No assertion adds a constraint the contract does not state. For example, licenses only need to be unique *within* a category. Cross-category uniqueness is not asserted.

## Tests

### 1. `test_license_summary_categorizes_known_licenses`
```rust
/// Verifies that an SBOM with known package licenses returns the correct per-category counts and identifiers.
#[tokio::test]
async fn test_license_summary_categorizes_known_licenses() {
    // Given an SBOM with packages licensed MIT, Apache-2.0, GPL-3.0-only, and one with an unrecognized license
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom_with_packages(&[
        ("pkg-a", "MIT"), ("pkg-b", "Apache-2.0"),
        ("pkg-c", "GPL-3.0-only"), ("pkg-d", "Custom-Proprietary"),
    ]).await;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then the response is 200 and every category matches exactly
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary, LicenseSummary {
        permissive: LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
        copyleft:   LicenseCategorySummary { count: 1, licenses: vec!["GPL-3.0-only".into()] },
        unknown:    LicenseCategorySummary { count: 1, licenses: vec!["Custom-Proprietary".into()] },
    });
}
```

### 2. `test_license_summary_nonexistent_sbom_returns_404`
```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404 Not Found.
#[tokio::test]
async fn test_license_summary_nonexistent_sbom_returns_404() {
    // Given an SBOM ID that does not exist
    let ctx = TestContext::new().await;
    let missing_id = Uuid::new_v4();

    // When requesting its license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing_id}/license-summary")).await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### 3. `test_license_summary_empty_sbom_returns_zeros`
```rust
/// Verifies that an SBOM with no packages returns zero counts and empty license lists in every category.
#[tokio::test]
async fn test_license_summary_empty_sbom_returns_zeros() {
    // Given an SBOM with no packages
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom_with_packages(&[]).await;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then every category is exactly { count: 0, licenses: [] }
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary, LicenseSummary::default());
}
```
(The comparison is with the full default value, which checks zeros *and* empty vecs in all three categories, not only one count.)

### 4. `test_license_summary_deduplicates_licenses`
```rust
/// Verifies that a license shared by multiple packages is listed and counted only once within its category.
#[tokio::test]
async fn test_license_summary_deduplicates_licenses() {
    // Given an SBOM where three packages are MIT, one is Apache-2.0, and two are GPL-2.0-only
    let ctx = TestContext::new().await;
    let sbom_id = ctx.ingest_sbom_with_packages(&[
        ("pkg-a", "MIT"), ("pkg-b", "MIT"), ("pkg-c", "MIT"),
        ("pkg-d", "Apache-2.0"),
        ("pkg-e", "GPL-2.0-only"), ("pkg-f", "GPL-2.0-only"),
    ]).await;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then each distinct license appears once and counts reflect distinct identifiers
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await;
    assert_eq!(summary.permissive, LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] });
    assert_eq!(summary.copyleft,   LicenseCategorySummary { count: 1, licenses: vec!["GPL-2.0-only".into()] });
    assert_eq!(summary.unknown,    LicenseCategorySummary::default());
}
```

`TestContext`, `ingest_sbom_with_packages` and `ctx.get` stand in for whatever harness and fixture helpers the sibling tests actually use. They would be confirmed with `get_symbols_overview` on `tests/api/sbom.rs` and reused, not reinvented.

## Execution
- `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>` (crate names resolved via `cargo metadata --no-deps --format-version 1`). Any failure is a hard stop before commit.
- If the new test file needs registering (for example in `tests/Cargo.toml` `[[test]]` or a `tests/api/main.rs`), flag that as an out-of-scope change for user approval.
