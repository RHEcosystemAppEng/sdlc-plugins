# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach
- **Structure, setup, naming:** copied from `tests/api/sbom.rs` / `tests/api/advisory.rs`. Same test context and DB fixture helpers, same HTTP client, same `assert_eq!(resp.status(), StatusCode::...)` status checks, and responses deserialized into the typed `LicenseSummary` model.
- **Assertion style: value-based (skill guidance overrides the sibling pattern).** The sibling `.filter(..).any(|_| true)` + `assert!(..)` and `.filter(..).count()` + `assert!(n > 0)` patterns are deliberately **not** used. They only prove that *something* exists, so they hide wrong counts, wrong categorization, missing dedup, and extra entries. Instead:
  - Compare the full response with `assert_eq!(summary, expected_summary)` against an explicitly constructed `LicenseSummary`. This checks every category's `count` and exact `licenses` vec in one assertion, and a failure diff shows *what* changed.
  - Where a per-field check reads better, use `assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"])` together with `assert_eq!(summary.permissive.count, 2)`. Never use a length check on its own.
  - License lists are sorted (BTreeSet), so vec equality is deterministic.
- **Documentation:** every test has a `///` doc comment. Non-trivial tests have `// Given`, `// When`, `// Then` sections.
- **No parameterization:** the siblings don't use `rstest`, and the four scenarios differ in setup and assertions, so they are separate test functions.
- **Fixture consistency:** expected values come from the fixture licenses and the AC. Duplicate licenses across packages are valid fixture data. Uniqueness is asserted only *within a category's output list* (the AC "deduplicated within each category"), not across fixture rows.

## Tests

### 1. `license_summary_returns_categorized_licenses`
```rust
/// Verifies that an SBOM with known package licenses returns correct per-category counts and identifiers.
#[test_context(TrustifyContext)] #[tokio::test]
async fn license_summary_returns_categorized_licenses(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SBOM whose packages have MIT, Apache-2.0, GPL-3.0-only and a non-SPDX license
    let sbom_id = ingest_sbom_with_licenses(ctx, &["MIT", "Apache-2.0", "GPL-3.0-only", "Custom-Proprietary"]).await?;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then the response is 200 and every category matches exactly
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await?;
    assert_eq!(summary, LicenseSummary {
        permissive: LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
        copyleft:   LicenseCategorySummary { count: 1, licenses: vec!["GPL-3.0-only".into()] },
        unknown:    LicenseCategorySummary { count: 1, licenses: vec!["Custom-Proprietary".into()] },
    });
    Ok(())
}
```
Covers AC 1 and AC 3: count and list are both present and both correct.

### 2. `license_summary_unknown_sbom_returns_404`
```rust
/// Verifies that requesting a license summary for a non-existent SBOM returns 404.
async fn license_summary_unknown_sbom_returns_404(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given a random SBOM id that was never ingested
    let missing = Uuid::new_v4();
    // When requesting its license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{missing}/license-summary")).await;
    // Then the server responds 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
    Ok(())
}
```
Covers AC 2.

### 3. `license_summary_empty_sbom_returns_zeros`
```rust
/// Verifies that an SBOM with no packages yields zero counts and empty license lists in every category.
// Given an SBOM ingested with zero packages
// When requesting the license summary
// Then status is 200 and the body equals LicenseSummary::default()
assert_eq!(resp.status(), StatusCode::OK);
assert_eq!(summary, LicenseSummary::default()); // all counts 0, all licenses vec![]
```
Also checks the 404-vs-empty distinction: an existing SBOM with no packages returns 200, not 404.

### 4. `license_summary_deduplicates_licenses_within_category`
```rust
/// Verifies that a license appearing on multiple packages is listed and counted only once in its category.
// Given an SBOM with three packages licensed MIT, MIT, Apache-2.0 and two packages licensed GPL-2.0-only
// When requesting the license summary
// Then each identifier appears once and counts reflect distinct licenses
assert_eq!(summary.permissive, LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] });
assert_eq!(summary.copyleft,   LicenseCategorySummary { count: 1, licenses: vec!["GPL-2.0-only".into()] });
assert_eq!(summary.unknown,    LicenseCategorySummary::default());
```
Covers AC 4. Exact vec equality would fail if "MIT" appeared twice, which an `.any()` / `count() > 0` check would miss.

## Execution
- `cargo test -p <tests crate> package_license` and `cargo test -p <fundamental crate>`, with crate names resolved via `cargo metadata --no-deps --format-version 1`.
- Then the full CI command list from CONVENTIONS.md, with a hard stop on any non-zero exit.
- If `tests/api/` needs a module declaration or `[[test]]` entry for the new file, it is flagged as an out-of-scope change for approval.
