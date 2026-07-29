<!-- SYNTHETIC TEST DATA — task where sibling test patterns conflict with skill's built-in quality guidance -->

# Mock Jira Task

**Key**: TC-9208
**Summary**: Add package license summary endpoint with tests
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add a REST endpoint that returns a summary of license types for packages within an SBOM.
The endpoint aggregates package licenses by type (permissive, copyleft, unknown) and
returns counts plus the list of specific license identifiers in each category.

## Files to Modify
- `modules/fundamental/src/package/endpoints/mod.rs` — register the new route
- `modules/fundamental/src/package/model/mod.rs` — add `pub mod license_summary;`

## Files to Create
- `modules/fundamental/src/package/model/license_summary.rs` — LicenseSummary response struct
- `modules/fundamental/src/package/endpoints/license_summary.rs` — GET handler for /api/v2/sbom/{id}/license-summary
- `tests/api/package_license.rs` — integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-summary` — NEW: returns `{ permissive: { count: N, licenses: [...] }, copyleft: { count: N, licenses: [...] }, unknown: { count: N, licenses: [...] } }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/package/endpoints/list.rs`
- Use the `package_license` entity from `entity/src/package_license.rs` for the JOIN query
- Error handling: return `AppError` with `.context()` wrapping

### Sibling test patterns
The existing integration tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` use a
common assertion pattern for validating list responses:

```rust
// Pattern from tests/api/advisory.rs:
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// Pattern from tests/api/sbom.rs:
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns check for existence but do not verify specific values. The new tests
for `package_license.rs` should follow the project's conventions for structure, setup,
and naming — but review whether the assertion style above is the best pattern for the
new tests.

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-summary returns categorized license counts
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Each category includes both a count and a list of license identifiers
- [ ] Licenses are deduplicated within each category

## Test Requirements
- [ ] Test that a valid SBOM with known package licenses returns correct categorized counts
- [ ] Test that a non-existent SBOM ID returns 404
- [ ] Test that an SBOM with no packages returns all zeros with empty license lists
- [ ] Test that duplicate licenses within a category are counted only once

## Dependencies
- Depends on: None
