# Test Plan — TC-9208 (`tests/api/package_license.rs`)

## Approach
- These are integration tests against the real PostgreSQL test database. They use the same harness, fixture setup, and HTTP client helpers as `tests/api/sbom.rs` and `tests/api/advisory.rs` (sibling convention).
- Status is asserted with the project pattern: `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::NOT_FOUND`.
- Bodies are deserialized into the typed `LicenseSummary` model.
- **Assertions are value-based** (skill Step 7 overrides the sibling pattern). Each test builds an expected `LicenseSummary` and checks it with `assert_eq!(body, expected)`, or with `assert_eq!` on each category's `count` and its exact, sorted `licenses` vector. The sibling patterns `.filter(..).any(|_| true)` with `assert!(has_x)` and `.filter(..).count()` with `assert!(n > 0)` are **not** used. They only prove existence, so a wrong count, a wrong category, or an extra or duplicated license would still pass.
- Deterministic ordering: the handler returns sorted (BTreeSet-derived) license lists, so exact `Vec` equality works without being flaky.
- Every test has a one-line `///` doc comment. The non-trivial tests have `// Given`, `// When`, and `// Then` sections.
- No `rstest` parameterization: the siblings do not use it, and the four cases differ in setup and assertions.
- Fixture/assertion consistency: assertions only state what the ACs require (categorized counts, 404, count plus list, dedup within a category). They do not assert uniqueness *across* categories or any ordering the contract does not define, beyond the sort the implementation guarantees and documents.

## Tests

### 1. `license_summary_returns_categorized_counts`
```rust
/// Verifies that an SBOM with known package licenses returns correct per-category counts and identifiers.
```
- Given: ingest an SBOM fixture whose packages have licenses `MIT`, `Apache-2.0` (permissive), `GPL-3.0-only` (copyleft), and one package with no or unrecognized license (unknown, e.g. `LicenseRef-custom`).
- When: `GET /api/v2/sbom/{id}/license-summary`.
- Then:
  ```rust
  assert_eq!(resp.status(), StatusCode::OK);
  let body: LicenseSummary = resp.json().await?;
  assert_eq!(body, LicenseSummary {
      permissive: LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] },
      copyleft:   LicenseCategorySummary { count: 1, licenses: vec!["GPL-3.0-only".into()] },
      unknown:    LicenseCategorySummary { count: 1, licenses: vec!["LicenseRef-custom".into()] },
  });
  ```

### 2. `license_summary_returns_404_for_missing_sbom`
```rust
/// Verifies that requesting a license summary for a non-existent SBOM ID returns 404.
```
- Trivial case with a single assertion, so it has no given-when-then sections. Request a random or unused UUID, then `assert_eq!(resp.status(), StatusCode::NOT_FOUND);`.

### 3. `license_summary_empty_sbom_returns_zeros`
```rust
/// Verifies that an SBOM with no packages returns zero counts and empty license lists in every category.
```
- Given: ingest an SBOM with no packages.
- When: GET the summary.
- Then: `assert_eq!(resp.status(), StatusCode::OK);` and `assert_eq!(body, LicenseSummary::default());`. Where `Default` is not derived, assert explicitly on each category: `count: 0, licenses: vec![]`.

### 4. `license_summary_deduplicates_licenses_within_category`
```rust
/// Verifies that a license shared by multiple packages appears once and is counted once in its category.
```
- Given: an SBOM with three packages licensed `MIT`, `MIT`, `Apache-2.0` and two packages licensed `GPL-2.0-only`.
- When: GET the summary.
- Then:
  ```rust
  assert_eq!(body.permissive, LicenseCategorySummary { count: 2, licenses: vec!["Apache-2.0".into(), "MIT".into()] });
  assert_eq!(body.copyleft,   LicenseCategorySummary { count: 1, licenses: vec!["GPL-2.0-only".into()] });
  assert_eq!(body.unknown,    LicenseCategorySummary { count: 0, licenses: vec![] });
  ```
  Exact vector equality catches a duplicated `"MIT"` entry. A `count > 0` or `.any()` check would miss it.

## Execution
- Resolve crate names with `cargo metadata --no-deps --format-version 1`. Run `cargo test -p <tests-crate>` (or `cargo nextest run -p ...` if the project uses nextest), and `cargo test -p <fundamental-crate>` for the touched module.
- Any non-zero exit is a hard stop before commit. If the same failure happens 3 times, stop and ask the user.
