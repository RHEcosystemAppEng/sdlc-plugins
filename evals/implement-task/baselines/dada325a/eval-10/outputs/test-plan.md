# Test Plan — TC-9208: `tests/api/package_license.rs`

## Approach

- **Structure, setup, naming:** these follow the sibling tests (`tests/api/sbom.rs`, `tests/api/advisory.rs`). That means the same async test attribute and harness/context, real PostgreSQL test DB, fixture SBOM ingestion through the shared helper, snake_case scenario names, and `assert_eq!(resp.status(), StatusCode::X)` for status codes.
- **Assertion style:** value-based, which **deviates from the sibling style on purpose**. The siblings use existence-only checks (`.filter(..).any(|_| true)` + `assert!(..)`, and `.filter(..).count()` + `assert!(n > 0)`). SKILL.md Step 7 says to prefer value-based assertions, and that skill guidance takes precedence over sibling patterns. So each test deserializes the body into `LicenseSummary` and compares it with `assert_eq!` against a fully constructed expected value, covering both counts **and** exact license identifier lists for all three categories. A failure then shows exactly which category or identifier differs. Sorted (`BTreeSet`) output makes exact list comparison deterministic.
- **No `.any()`, no `count() > 0`, no length-only checks.** Where a count is asserted, the identifier list is always asserted next to it, and `count == licenses.len()` is checked by the full-struct equality.
- **Documentation:** a `///` doc comment on every test function, plus `// Given` / `// When` / `// Then` sections, since every test has distinct setup, action, and assertion phases. Sibling tests lack these, but the skill requires them regardless.
- **Parameterization:** none. The siblings show no `rstest` or table-driven usage, so the skill says not to introduce it. The four scenarios also differ in setup and assertion shape (Meszaros heuristic: separate tests).

## Tests

### 1. `license_summary_categorizes_known_licenses`
```rust
/// Verifies that an SBOM with known package licenses returns correct per-category counts and identifiers.
#[test_context(TrustifyContext)]
#[test(tokio::test)]
async fn license_summary_categorizes_known_licenses(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SBOM whose packages carry MIT, Apache-2.0, GPL-3.0-only and a non-SPDX license
    let sbom_id = ingest_sbom_with_licenses(ctx, &["MIT", "Apache-2.0", "GPL-3.0-only", "LicenseRef-Custom"]).await?;

    // When requesting the license summary
    let resp = get(ctx, &format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then the response is 200 and each category holds exactly the expected licenses
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await?;
    assert_eq!(summary, LicenseSummary {
        permissive: LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
        copyleft:   LicenseCategorySummary { count: 1, licenses: vec!["GPL-3.0-only".into()] },
        unknown:    LicenseCategorySummary { count: 1, licenses: vec!["LicenseRef-Custom".into()] },
    });
    Ok(())
}
```
(The helper and harness names above are placeholders. The real ones are whatever `tests/api/sbom.rs` uses.)

### 2. `license_summary_unknown_sbom_returns_404`
- `///` Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
- Given a random or unused SBOM ID (no ingestion). When it is requested. Then `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`. Also assert the error body's key field (e.g. the error code or message) if sibling 404 tests or the `AppError` JSON shape expose one.

### 3. `license_summary_empty_sbom_returns_zeros`
- `///` Verifies that an SBOM with no packages returns zero counts and empty license lists for every category.
- Given an ingested SBOM with zero packages. When it is requested. Then the status is 200 and `assert_eq!(summary, LicenseSummary::default())`, plus an explicit expected literal with `count: 0, licenses: vec![]` for each of the three categories, so the intent is visible.

### 4. `license_summary_deduplicates_licenses`
- `///` Verifies that a license repeated across multiple packages is listed and counted only once within its category.
- Given an SBOM with several packages: three `MIT`, two `Apache-2.0`, and two `GPL-2.0-only`. When it is requested. Then
  `permissive == { count: 2, licenses: ["Apache-2.0", "MIT"] }`, `copyleft == { count: 1, licenses: ["GPL-2.0-only"] }`, `unknown == { count: 0, licenses: [] }`, checked with a single full-struct `assert_eq!`. Asserting the exact list, not just `count == 2`, proves both that duplicates were removed and which identifiers survived.

## Optional unit coverage (in-scope file)
If the model file uses `#[cfg(test)]` modules like its siblings, add documented unit tests in `model/license_summary.rs` for `LicenseSummary::from_licenses` and the classifier. Each uses an exact `assert_eq!` on the resulting struct or category (e.g. `"mit"` → Permissive, `"AGPL-3.0-or-later"` → Copyleft, `""` skipped). These only get added if the siblings have in-file unit tests. Otherwise only the four required integration tests are written.

## Execution
- `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`. Crate names come from `cargo metadata --no-deps --format-version 1`. Use `cargo nextest run -p ...` if the project uses nextest.
- Any non-zero exit is a hard stop and gets reported. If the same failure repeats 3 times, stop and ask the user.
