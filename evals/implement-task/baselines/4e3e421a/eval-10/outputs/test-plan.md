# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach
- Integration tests against the real PostgreSQL test database, using the sibling setup helpers from `tests/api/sbom.rs` (test context/app construction and fixture ingestion).
- **Value-based assertions (skill guidance overrides the siblings).** The siblings in `advisory.rs` and `sbom.rs` use `.filter().any(|_| true)` / `assert!(bool)` and `.filter().count()` / `assert!(n > 0)`. Those checks only prove that something exists, and a failure says nothing about what was returned. The new tests deserialize the body into `LicenseSummary` and use `assert_eq!` against a fully specified expected value, so a regression shows the exact category, count and license list that changed.
- Status codes are checked with the project's `assert_eq!(resp.status(), StatusCode::OK / NOT_FOUND)` pattern (kept from the siblings).
- Every test has a `///` doc comment. Non-trivial tests have `// Given`, `// When` and `// Then` sections.
- No parameterisation (`rstest`). The project doesn't use it, and the four scenarios differ in setup and assertions.
- Fixture consistency: expected values are derived from the inserted fixture data and the stated contract only. `count` is the number of **distinct** licenses in a category (AC: "deduplicated", TR: "counted only once"). License lists are compared in sorted order because the implementation uses a `BTreeSet`. The tests require no uniqueness or ordering beyond what the contract and implementation define.

## Tests

### 1. `license_summary_returns_categorized_counts`
`/// Verifies that an SBOM with known package licenses returns correct per-category counts and license lists.`
- **Given**: an SBOM with packages licensed `MIT`, `Apache-2.0`, `GPL-3.0-only` and `Custom-Proprietary`.
- **When**: `GET /api/v2/sbom/{id}/license-summary`.
- **Then**:
  ```rust
  assert_eq!(resp.status(), StatusCode::OK);
  let summary: LicenseSummary = resp.json().await;
  assert_eq!(summary, LicenseSummary {
      permissive: LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
      copyleft:   LicenseCategory { count: 1, licenses: vec!["GPL-3.0-only".into()] },
      unknown:    LicenseCategory { count: 1, licenses: vec!["Custom-Proprietary".into()] },
  });
  ```
  The test does **not** use `summary.permissive.licenses.iter().any(|l| l == "MIT")` or `assert!(summary.permissive.count > 0)`.

### 2. `license_summary_nonexistent_sbom_returns_404`
`/// Verifies that requesting a license summary for an unknown SBOM ID returns 404.`
- When: GET with a random or unused ID.
- Then: `assert_eq!(resp.status(), StatusCode::NOT_FOUND);`. This is a single assertion with no setup, so it is a trivial test and gets no given-when-then sections.

### 3. `license_summary_empty_sbom_returns_zeros`
`/// Verifies that an SBOM with no packages returns zero counts and empty license lists in every category.`
- Given: an SBOM ingested with no packages.
- Then: `assert_eq!(resp.status(), StatusCode::OK);` and `assert_eq!(summary, LicenseSummary::default());`. The expected value is written out explicitly as three `LicenseCategory { count: 0, licenses: vec![] }`, so the test does not quietly depend on `Default`.

### 4. `license_summary_deduplicates_licenses_within_category`
`/// Verifies that a license shared by several packages is listed and counted only once in its category.`
- Given: three packages licensed `MIT` and one licensed `Apache-2.0`.
- Then: `assert_eq!(summary.permissive, LicenseCategory { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] });`, plus `assert_eq!` that `copyleft` and `unknown` are empty, so no duplicate has leaked into another category.

## Execution
- `cargo test -p <tests crate>`, plus `cargo test -p <fundamental crate>` (crate names resolved with `cargo metadata --no-deps`). Then run the CONVENTIONS.md CI commands. Any non-zero exit is a hard stop.
