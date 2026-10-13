# Implementation Plan for TC-9208

## Summary

Add a REST endpoint `GET /api/v2/sbom/{id}/license-summary` that returns categorized
license counts (permissive, copyleft, unknown) with deduplicated license identifier
lists, plus integration tests.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`

Register the new `license_summary` route in the existing route configuration. Add an
import for the new `license_summary` endpoint module and wire its handler into the
router under `/api/v2/sbom/{id}/license-summary`.

Follow the existing pattern visible in sibling endpoint registrations (e.g., how
`list.rs` and `get.rs` are registered).

### 2. `modules/fundamental/src/package/model/mod.rs`

Add `pub mod license_summary;` to expose the new model module. Place it alphabetically
alongside existing `pub mod` declarations (e.g., after `pub mod summary;`).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`

Define the `LicenseSummary` response struct with three nested category structs, each
containing:
- `count: usize` -- number of deduplicated licenses in this category
- `licenses: Vec<String>` -- the specific license identifiers (SPDX IDs)

Top-level struct:
```rust
/// Categorized summary of package licenses within an SBOM.
pub struct LicenseSummary {
    pub permissive: LicenseCategory,
    pub copyleft: LicenseCategory,
    pub unknown: LicenseCategory,
}

/// A single license category with its count and deduplicated license identifiers.
pub struct LicenseCategory {
    pub count: usize,
    pub licenses: Vec<String>,
}
```

Derive `Serialize`, `Deserialize`, and `Debug`. Implement a constructor that takes a
list of `(license_id, category)` tuples, deduplicates within each category using a
`HashSet`, and populates the counts.

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`

Implement a GET handler following the pattern in `list.rs`:
- Extract the SBOM ID from the path.
- Query `package_license` entity (from `entity/src/package_license.rs`) joined through
  `sbom_package` to filter by the given SBOM ID.
- Classify each license into permissive/copyleft/unknown (use a static mapping or
  SPDX metadata).
- Deduplicate licenses within each category.
- Return `LicenseSummary` as JSON.
- Return 404 via `AppError` with `.context()` wrapping when the SBOM ID does not exist.

### 5. `tests/api/package_license.rs`

Create integration tests (see test-plan.md for full assertion strategy). Four test
functions covering:
1. Valid SBOM with known licenses returns correct categorized counts and identifiers.
2. Non-existent SBOM ID returns 404.
3. SBOM with no packages returns all-zero counts with empty license lists.
4. Duplicate licenses within a category are counted only once.

Also add `mod package_license;` to `tests/api/mod.rs` (or the test harness entry
point) if the project uses a module-based test registration pattern.

## Approach

1. **Understand code** (Step 4): Read sibling endpoint files (`list.rs`, `get.rs`)
   and sibling models (`summary.rs`, `details.rs`) via Serena's `get_symbols_overview`.
   Read sibling tests (`advisory.rs`, `sbom.rs`) for conventions. Read
   `entity/src/package_license.rs` for the join entity schema.

2. **Implement model** (Step 6): Create `license_summary.rs` model with doc comments
   on all public symbols and defensive defaults for missing license data.

3. **Implement endpoint** (Step 6): Create the handler with `Result<T, AppError>`
   return type, `.context()` error wrapping, and proper 404 handling.

4. **Register route** (Step 6): Wire the handler into `endpoints/mod.rs`.

5. **Write tests** (Step 7): Create integration tests using value-based assertions
   (see test-plan.md). Follow sibling conventions for test structure, naming, and
   setup -- but override assertion style per skill guidance.

6. **Verify** (Steps 8-9): Check acceptance criteria, run `cargo test`, scope
   containment check, duplication check, data-flow trace.
