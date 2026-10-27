# Convention Conformance Analysis — TC-9208

## Sibling Analysis

Analyzed sibling files in the `modules/fundamental/` domain modules and `tests/api/` integration tests to identify recurring patterns.

### Production Code Conventions

| Category | Convention | Source |
|----------|-----------|--------|
| **Module structure** | Each domain follows `model/ + service/ + endpoints/` layout | `advisory/`, `sbom/`, `package/` modules |
| **Error handling** | Handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation | `advisory/endpoints/get.rs`, `sbom/endpoints/list.rs`, `common/src/error.rs` |
| **Response types** | List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` | `sbom/endpoints/list.rs`, `advisory/endpoints/list.rs` |
| **Route registration** | Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules | `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs` |
| **Naming** | Snake_case for files and functions; `verb_noun` pattern for service methods | `advisory/service/advisory.rs`, `package/service/mod.rs` |
| **Import organization** | External crates first, then `crate::` imports, then local `super::` imports | Consistent across all endpoint files |
| **Entity access** | Use SeaORM entities from `entity/src/` for database queries; JOIN via entity relationships | `entity/src/package_license.rs`, `entity/src/sbom_package.rs` |
| **Query helpers** | Shared filtering, pagination, and sorting via `common/src/db/query.rs` | `sbom/endpoints/list.rs`, `advisory/endpoints/list.rs` |

### Test Code Conventions

| Category | Convention | Source |
|----------|-----------|--------|
| **Test location** | Integration tests in `tests/api/` directory, one file per domain | `tests/api/advisory.rs`, `tests/api/sbom.rs` |
| **Test naming** | `test_<verb>_<noun>_<scenario>` pattern (e.g., `test_list_advisories_by_severity`) | `tests/api/advisory.rs`, `tests/api/sbom.rs` |
| **Setup/teardown** | Tests use a shared test database with per-test transaction rollback | `tests/api/advisory.rs`, `tests/api/sbom.rs` |
| **Status assertions** | `assert_eq!(resp.status(), StatusCode::OK)` for HTTP status validation | `tests/api/advisory.rs`, `tests/api/sbom.rs` |
| **Response parsing** | Parse response body as JSON using `serde_json::from_slice` or `.json::<T>()` | `tests/api/advisory.rs`, `tests/api/sbom.rs` |
| **Assertion style** | `.filter().any()` for existence checks; `.filter().count() > 0` for presence validation | `tests/api/advisory.rs`, `tests/api/sbom.rs` |

## Convention Conflicts

### CONFLICT: Assertion style — sibling pattern vs. skill guidance

**Sibling pattern:** Tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` use `.filter().any()` and `.filter().count() > 0` patterns for validating list responses:

```rust
// From tests/api/advisory.rs:
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// From tests/api/sbom.rs:
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns check **existence** only — they confirm that at least one matching item exists but do not verify:
- Exact counts per category
- Specific license identifier values
- Completeness of categorization (all expected items accounted for)

**Skill guidance (Step 7):** "Prefer value-based assertions over length-only checks: When verifying collections or response data, assert on the actual values — not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*. Length checks alone hide regressions behind a passing count and prevent subsequent assertions from running."

**Resolution: Skill guidance takes precedence.** Per SKILL.md Step 7: "The guidance below (value-based assertions, parameterized tests, test documentation) is the skill's explicit quality standard and takes precedence over conflicting sibling patterns." The `.filter().any()` and `.filter().count() > 0` patterns from siblings are existence checks that hide regressions — a bug that changes "MIT" to "BSD-2-Clause" would still pass `.any()`. The new `tests/api/package_license.rs` tests will use value-based assertions (`assert_eq!` on specific license identifiers and exact counts) while following sibling conventions for all non-conflicting aspects (test naming, setup, organization, status assertions, response parsing).

### Non-conflicting conventions adopted

The following sibling conventions apply without conflict and will be followed:
- Test naming: `test_<verb>_<noun>_<scenario>` pattern
- Test setup: shared test database with transaction rollback
- Status validation: `assert_eq!(resp.status(), StatusCode::OK)`
- Response parsing: `.json::<T>()` deserialization
- Test file location: `tests/api/` directory
- Test organization: one file per domain/feature area
