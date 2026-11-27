# Test Plan — TC-9208 `tests/api/package_license.rs`

## Approach

- **Structure, setup, naming**: copied from sibling `tests/api/sbom.rs` / `tests/api/advisory.rs` — same test-context/DB fixture setup against real PostgreSQL, same HTTP call helper, same snake_case naming, status checks via `assert_eq!(resp.status(), StatusCode::...)`.
- **Assertion style**: **value-based**, per the skill's Step 7 rule, which overrides the sibling existence-check pattern (`.filter(..).any(|_| true)` / `.filter(..).count() > 0`). Each test deserialises the body into `LicenseSummary` and asserts with `assert_eq!` on exact counts **and** exact, sorted license-identifier vectors (ideally comparing the whole struct to an expected value, so a failure diff shows exactly what changed).
- **No existence-only or length-only assertions.** `count` is always checked together with the `licenses` contents.
- **Documentation**: every test has a `///` doc comment; non-trivial tests use `// Given`, `// When`, `// Then` sections.
- **Parameterization**: not used — siblings do not use `rstest`, and the four cases differ in setup and assertions (Meszaros heuristic says separate tests).
- **Fixtures**: ingest a purpose-built SBOM whose packages have known licenses so expected values are deterministic. Assertions must reflect fixture semantics only (no added constraints beyond ACs).

## Tests

### 1. `license_summary_returns_categorized_counts`
```rust
/// Verifies that an SBOM with known package licenses returns correct counts and identifiers per category.
#[test_context(TrustifyContext)]
#[tokio::test]
async fn license_summary_returns_categorized_counts(ctx: &TrustifyContext) -> anyhow::Result<()> {
    // Given an SBOM with packages licensed MIT, Apache-2.0, GPL-3.0-only and a non-SPDX license
    let sbom_id = ingest_sbom_with_licenses(ctx, &["MIT", "Apache-2.0", "GPL-3.0-only", "Custom-Proprietary"]).await?;

    // When requesting the license summary
    let resp = ctx.get(&format!("/api/v2/sbom/{sbom_id}/license-summary")).await;

    // Then the response is OK and every category matches exactly
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: LicenseSummary = resp.json().await?;
    assert_eq!(summary, LicenseSummary {
        permissive: LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
        copyleft:   LicenseCategory { count: 1, licenses: vec!["GPL-3.0-only".into()] },
        unknown:    LicenseCategory { count: 1, licenses: vec!["Custom-Proprietary".into()] },
    });
    Ok(())
}
```

### 2. `license_summary_returns_404_for_missing_sbom`
```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
async fn license_summary_returns_404_for_missing_sbom(ctx: &TrustifyContext) -> anyhow::Result<()> {
    let resp = ctx.get(&format!("/api/v2/sbom/{}/license-summary", Uuid::new_v4())).await;
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
    Ok(())
}
```
(Trivial: single assertion, no distinct setup — given-when-then omitted.)

### 3. `license_summary_empty_sbom_returns_zeros`
- Given an SBOM ingested with no packages; When GET license-summary; Then `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(summary, LicenseSummary::default())` — plus explicit expected struct with `count: 0, licenses: vec![]` for all three categories so the intent is visible.

### 4. `license_summary_deduplicates_licenses_within_category`
- Given an SBOM with three packages: two `MIT`, one `Apache-2.0` (and two `GPL-2.0-only`);
- When GET license-summary;
- Then `assert_eq!(summary.permissive, LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] })` and `assert_eq!(summary.copyleft, LicenseCategory { count: 1, licenses: vec!["GPL-2.0-only".into()] })` and `assert_eq!(summary.unknown, LicenseCategory::default())`.
- This asserts both that the duplicate is not double-counted and that the identifier appears once in the list.

## Contrast with sibling style (recorded conflict)

| Sibling (not used) | New tests (used) |
|---|---|
| `assert!(items.iter().filter(..).any(\|_\| true))` | `assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"])` |
| `assert!(items.iter().filter(..).count() > 0)` | `assert_eq!(summary.permissive.count, 2)` together with the exact list |

## Optional unit tests
If allowed in scope, a `#[cfg(test)]` module in `model/license_summary.rs` testing `classify` / `from_licenses` with value-based `assert_eq!` (e.g. `None` -> skipped, `"GPL-3.0-or-later"` -> copyleft). Not required by Test Requirements; only added if consistent with sibling model files.

## Execution
Run CI checks from `CONVENTIONS.md`; otherwise per-crate `cargo test -p <crate>` for the fundamental crate and the `tests` crate (crates resolved via `cargo metadata`), plus `cargo fmt --check` and `cargo clippy`.
