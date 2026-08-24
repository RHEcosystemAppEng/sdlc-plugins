# Conventions Discovered from Sibling Analysis -- TC-9208

## Sibling files analyzed

### Production code siblings
- `modules/fundamental/src/package/endpoints/list.rs` -- existing GET /api/v2/package endpoint handler
- `modules/fundamental/src/package/model/summary.rs` -- PackageSummary struct
- `modules/fundamental/src/advisory/endpoints/list.rs` -- advisory list endpoint (similar domain)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- SBOM list endpoint (similar domain)

### Test code siblings
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

---

## Discovered conventions by category

### Naming conventions
- **Files**: snake_case for all Rust source files (e.g., `license_summary.rs`, `summary.rs`)
- **Structs**: PascalCase with domain prefix (e.g., `SbomSummary`, `AdvisorySummary`, `PackageSummary`)
- **Functions**: snake_case verb_noun pattern (e.g., `get_license_summary`, `list_sboms`)
- **Test functions**: `test_` prefix followed by descriptive name (e.g., `test_list_advisories`, `test_get_sbom_by_id`)
- **Test files**: named after the domain entity being tested (e.g., `advisory.rs`, `sbom.rs`)

### Module structure
- Each domain follows `model/ + service/ + endpoints/` structure
- `model/mod.rs` declares submodules with `pub mod <name>;`
- `endpoints/mod.rs` registers routes and declares endpoint submodules
- Models derive `Debug, Clone, Serialize, Deserialize, ToSchema` (utoipa for OpenAPI)

### Error handling
- All handlers return `Result<T, AppError>` using the `AppError` type from `common/src/error.rs`
- Errors are wrapped with `.context("descriptive message")` from the `anyhow` crate
- This pattern is consistent across all endpoint handlers in the codebase

### Import organization
- Standard library imports first, then external crates, then internal crate imports
- Grouped by source with blank lines between groups

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-item endpoints return the model struct directly
- Query helpers from `common/src/db/query.rs` for filtering, pagination, sorting

### Test conventions -- non-conflicting aspects
- **Setup/teardown**: Tests use a shared test database setup (real PostgreSQL) with test data fixtures
- **Test organization**: Integration tests live in `tests/api/` directory, one file per domain
- **Response validation**: Tests check `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- **Error cases**: Tests verify 404 responses for non-existent resources
- **Structure**: Tests follow the arrange/act/assert pattern

### Test conventions -- CONFLICTING assertion patterns

**CONFLICT DETECTED** between sibling test patterns and skill quality guidance.

#### Sibling patterns (from `tests/api/advisory.rs` and `tests/api/sbom.rs`)

The existing integration tests use `.filter().any()` and `.filter().count() > 0` existence-check patterns for validating list response contents:

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

These patterns check for *existence* only -- they verify that at least one matching item exists but do not verify:
- Exact counts
- Specific values of individual items
- Completeness of results

#### Skill guidance (from SKILL.md Step 7)

The implement-task skill's built-in quality guidance states:

> "Prefer value-based assertions over length-only checks: When verifying collections or response data, assert on the actual values -- not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*. Length checks alone hide regressions behind a passing count and prevent subsequent assertions from running."

#### Resolution

**The skill guidance takes precedence over the sibling patterns.** Per the SKILL.md:

> "Skill guidance overrides sibling patterns: The test conventions from Step 4 are defaults. The guidance below (value-based assertions, parameterized tests, test documentation) is the skill's explicit quality standard and takes precedence over conflicting sibling patterns. Note any deviation in the convention output."

Sibling conventions are treated as defaults -- they apply when no explicit skill instruction conflicts. In this case, the skill's value-based assertion guidance directly conflicts with the sibling `.filter().any()` and `.filter().count() > 0` existence-check patterns. Therefore:

- **Follow sibling conventions for**: test naming, file naming, test organization, setup/teardown, module structure, response status assertions, error case coverage
- **Override sibling conventions for**: assertion style on collection/response data -- use value-based assertions (`assert_eq!` on specific license identifiers, exact counts per category) instead of existence checks (`.any()`, `.count() > 0`)

This conflict is documented here so reviewers understand why the new tests in `tests/api/package_license.rs` deviate from the assertion style in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
