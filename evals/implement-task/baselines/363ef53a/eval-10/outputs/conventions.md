# Conventions Discovered from Sibling Analysis: TC-9208

## Source Files Analyzed

- `tests/api/advisory.rs` -- advisory endpoint integration tests (sibling)
- `tests/api/sbom.rs` -- SBOM endpoint integration tests (sibling)
- `modules/fundamental/src/package/endpoints/list.rs` -- existing package endpoint (sibling)
- `modules/fundamental/src/package/model/summary.rs` -- existing package model (sibling)

## Discovered Conventions by Category

### Naming Conventions

- **Test functions**: `test_<action>_<entity>_<scenario>` pattern (e.g.,
  `test_list_advisories_with_filter`, `test_get_sbom_not_found`)
- **Endpoint handlers**: `<verb>_<entity>` pattern (e.g., `list_packages`, `get_sbom`)
- **Model structs**: `<Entity><Role>` pattern (e.g., `SbomSummary`, `PackageSummary`)
- **File names**: snake_case matching the entity (e.g., `advisory.rs`, `sbom.rs`)

### Error Handling

- Handlers return `Result<T, AppError>` with `.context()` wrapping on fallible operations
- 404 cases use `AppError::NotFound` or equivalent

### Import Organization

- Standard library imports first, then external crates, then internal modules
- Group imports by crate with blank lines between groups

### Response Patterns

- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Individual resource endpoints return the model struct directly as `Json<T>`
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)`

### Test Structure and Setup

- Integration tests in `tests/api/` use a real PostgreSQL test database
- Tests use shared setup helpers for database initialization and teardown
- Each test file corresponds to one domain entity
- Tests validate HTTP status codes before inspecting response body

### Test Assertion Patterns (CONFLICT IDENTIFIED)

**Sibling patterns observed:**

From `tests/api/advisory.rs`:
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

From `tests/api/sbom.rs`:
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns use `.filter().any()` and `.filter().count() > 0` to perform existence
checks -- they verify that at least one matching item exists but do not assert on
specific values, exact counts, or the complete contents of the response.

## Conflict: Sibling Assertion Style vs. Skill Quality Guidance

**Conflict detected.** The sibling test patterns described above conflict with the
implement-task skill's built-in quality guidance in Step 7:

> "Prefer value-based assertions over length-only checks: When verifying collections or
> response data, assert on the actual values -- not just the count. Assert on specific
> items or key fields so that test failures reveal *what* changed, not just *how many*.
> Length checks alone hide regressions behind a passing count and prevent subsequent
> assertions from running."

The sibling `.filter().any()` and `.filter().count() > 0` patterns are existence checks
that reveal only *whether* a match exists, not *what specific values* are present. They
are functionally equivalent to length-only checks in that they hide regressions: if the
wrong license appears in a category, these assertions would still pass as long as any
license matches the filter.

**Resolution: Skill guidance takes precedence.** Per the skill's explicit instruction
(Step 4: "Skill guidance takes precedence over sibling patterns" and Step 7: "The test
conventions from Step 4 are defaults. The guidance below [...] is the skill's explicit
quality standard and takes precedence over conflicting sibling patterns"), sibling
conventions are defaults, not overrides of explicit skill instructions. The new tests
will use value-based assertions (`assert_eq!` on specific license identifiers and exact
counts per category) instead of adopting the sibling `.any()` / `.count() > 0` patterns.

## Non-Conflicting Conventions (Adopted)

The following sibling conventions do not conflict with skill guidance and will be followed:

- Test file naming: `package_license.rs` in `tests/api/`
- Test function naming: `test_<action>_<entity>_<scenario>` pattern
- Test setup/teardown: shared database setup helpers matching sibling patterns
- Status code validation: `assert_eq!(resp.status(), StatusCode::OK)` before body checks
- Test organization: one test file per domain entity in `tests/api/`
- Error handling: `Result<T, AppError>` with `.context()` wrapping
- Response types: `Json<LicenseSummary>` for the single-resource endpoint
