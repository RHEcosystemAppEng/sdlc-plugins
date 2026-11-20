# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach

- Structure, setup, naming, harness and status assertions follow the sibling tests `tests/api/sbom.rs` and `tests/api/advisory.rs`: a real PostgreSQL test DB, the existing test client and fixture helpers, and `assert_eq!(resp.status(), StatusCode::...)`.
- **Assertions are value-based.** The sibling `.filter().any(|_| true)` and `.count() > 0` existence checks are deliberately not used. The skill's Step 7 guidance takes precedence over sibling patterns (recorded in conventions.md). Each test deserializes the body into `LicenseSummary` and compares exact counts and exact license-identifier lists. When a test fails, the diff shows *which* license landed in *which* category.
- Determinism: license lists are sorted (the `BTreeSet` in `from_licenses`), so `assert_eq!` against literal `Vec`s is stable. Where possible, the whole struct is compared against an expected `LicenseSummary` so that an extra or wrong field also fails.
- Every test has a `///` doc comment and `// Given / // When / // Then` sections.
- No `rstest`. The siblings do not use it, and the four cases differ in setup and assertions (Meszaros heuristic: separate tests).

## Tests

### 1. `test_license_summary_returns_categorized_counts`
`/// Verifies that an SBOM with known package licenses returns the correct licenses and counts per category.`
- Given: ingest an SBOM fixture whose packages have the licenses MIT, Apache-2.0, GPL-3.0-only and one custom or NOASSERTION license.
- When: `GET /api/v2/sbom/{id}/license-summary`
- Then:
  ```rust
  assert_eq!(resp.status(), StatusCode::OK);
  let summary: LicenseSummary = resp.json().await;
  assert_eq!(summary, LicenseSummary {
      permissive: LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
      copyleft:   LicenseCategorySummary { count: 1, licenses: vec!["GPL-3.0-only".into()] },
      unknown:    LicenseCategorySummary { count: 1, licenses: vec!["LicenseRef-custom".into()] },
  });
  ```

### 2. `test_license_summary_nonexistent_sbom_returns_404`
`/// Verifies that requesting a license summary for an unknown SBOM ID returns 404.`
- When: GET with a random, unused id.
- Then: `assert_eq!(resp.status(), StatusCode::NOT_FOUND);`. This is a single assertion with no setup, so given-when-then sections are optional. A short `// When`/`// Then` is still fine.

### 3. `test_license_summary_empty_sbom_returns_zeros`
`/// Verifies that an SBOM with no packages returns zero counts and empty license lists in every category.`
- Given: ingest an SBOM with no packages.
- Then: `assert_eq!(resp.status(), StatusCode::OK);` and `assert_eq!(summary, LicenseSummary::default());`. The expected value is also written out explicitly (`count: 0, licenses: vec![]` for each of the three categories) so the test does not depend on what `Default` does.

### 4. `test_license_summary_deduplicates_licenses_within_category`
`/// Verifies that a license shared by several packages is listed and counted only once in its category.`
- Given: an SBOM whose three packages are licensed MIT, MIT and Apache-2.0, plus two packages licensed GPL-2.0-only.
- Then:
  ```rust
  assert_eq!(summary.permissive.count, 2);
  assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"]);
  assert_eq!(summary.copyleft.count, 1);
  assert_eq!(summary.copyleft.licenses, vec!["GPL-2.0-only"]);
  ```
  It also checks `count == licenses.len()` for each category. That is a consistency check made *in addition to* the value assertions, not instead of them.

## Assertion and fixture consistency
- Expected values come from the Acceptance Criteria (categorized counts, a count plus a list per category, deduplication within each category) and from the fixture licenses that were actually ingested.
- Repeated licenses across packages are valid fixture data. The tests only require uniqueness *within a category's list*, which is exactly what the acceptance criterion says. Uniqueness across categories is not asserted.

## Execution
- `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`, with names resolved through `cargo metadata --no-deps --format-version 1`. A non-zero exit is a hard stop.
- Plus the CI commands from CONVENTIONS.md (fmt, clippy and so on).
