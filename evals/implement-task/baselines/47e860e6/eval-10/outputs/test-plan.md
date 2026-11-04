# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach

- Use the sibling structure: same test DB setup, HTTP client helper and fixture ingestion as `tests/api/sbom.rs` and `tests/api/advisory.rs`, with snake_case behavior names.
- **Assertions compare values (skill guidance overrides the sibling pattern).** The sibling `.filter().any(|_| true)` + `assert!(..)` and `.filter().count()` + `assert!(n > 0)` style is not used. Each test deserializes the body into `LicenseSummary` and uses `assert_eq!` against a fully specified expected value, so a failure shows exactly which category, count or identifier is wrong.
- Status codes are asserted with `assert_eq!(resp.status(), StatusCode::...)`, the existing sibling convention.
- Every test function has a `///` doc comment. Non-trivial tests have `// Given`, `// When`, `// Then` sections.
- No parameterization. The project does not use `rstest`, and the four cases differ in setup and assertions (Meszaros heuristic), so they are separate tests.
- Fixture consistency: expected values come from the licenses actually present in the ingested fixture SBOM and from the Acceptance Criteria. The tests do not add constraints the contract does not state. For example, ordering is asserted only because the implementation explicitly sorts via `BTreeSet`.

## Tests

### 1. `license_summary_returns_categorized_counts`
```rust
/// Verifies that an SBOM with known package licenses returns correct per-category counts and identifiers.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn license_summary_returns_categorized_counts(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SBOM whose packages carry MIT, Apache-2.0, GPL-3.0-only and a custom license
    let id = ctx.ingest_sbom_with_licenses(&["MIT", "Apache-2.0", "GPL-3.0-only", "LicenseRef-custom"]).await?;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{id}/license-summary")).await;

    // Then each category contains exactly the expected identifiers
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await?;
    assert_eq!(summary, LicenseSummary {
        permissive: LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
        copyleft:   LicenseCategory { count: 1, licenses: vec!["GPL-3.0-only".into()] },
        unknown:    LicenseCategory { count: 1, licenses: vec!["LicenseRef-custom".into()] },
    });
    Ok(())
}
```

### 2. `license_summary_returns_404_for_unknown_sbom`
- `/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.`
- Given a random `Uuid::new_v4()` that is not in the DB. When GET is called. Then `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### 3. `license_summary_empty_sbom_returns_zeros`
- `/// Verifies that an SBOM with no packages returns zero counts and empty license lists in every category.`
- Given an ingested SBOM with no packages. Then `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(summary, LicenseSummary::default())`, i.e. every category is `{ count: 0, licenses: vec![] }`. The test checks the empty vectors explicitly, not only the counts.

### 4. `license_summary_deduplicates_licenses_within_category`
- `/// Verifies that a license shared by multiple packages is listed and counted only once in its category.`
- Given an SBOM with three packages licensed `MIT`, `MIT`, `Apache-2.0`. Then `assert_eq!(summary.permissive, LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] })`. Copyleft and unknown are also asserted equal to `LicenseCategory::default()`, so a duplicate cannot leak into another category.

## Not used (and why)
```rust
// Sibling style rejected for the new tests:
let has_mit = summary.permissive.licenses.iter().filter(|l| *l == "MIT").any(|_| true);
assert!(has_mit);                       // passes even if counts, other entries or duplicates are wrong
assert!(summary.permissive.count > 0);  // hides regressions behind a passing count
```

## Execution
- `cargo test -p <tests-crate>` and `cargo test -p <fundamental-crate>`, with crate names resolved through `cargo metadata`, plus the CI commands from CONVENTIONS.md. Any failure is a hard stop before commit.
- If the `tests` crate needs `mod package_license;` in an aggregator file, that file is out of scope and needs user approval first.
