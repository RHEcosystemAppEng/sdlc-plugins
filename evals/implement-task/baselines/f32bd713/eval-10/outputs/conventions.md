# Conventions Discovered from Sibling Analysis -- TC-9208

## Source Siblings

- **Production code siblings**: `modules/fundamental/src/sbom/endpoints/list.rs`,
  `modules/fundamental/src/sbom/endpoints/get.rs`,
  `modules/fundamental/src/advisory/endpoints/list.rs`
- **Test code siblings**: `tests/api/advisory.rs`, `tests/api/sbom.rs`

## Non-Conflicting Conventions (adopted as-is)

### Module structure
- Each domain module follows `model/ + service/ + endpoints/` structure.
- Endpoint modules are registered in `endpoints/mod.rs` with route builder calls.
- Model modules are exposed via `pub mod` in `model/mod.rs`.

### Naming conventions
- Files use `snake_case` naming.
- Structs use `PascalCase` (e.g., `SbomSummary`, `AdvisoryDetails`).
- Handler functions use `verb_noun` pattern (e.g., `get_sbom`, `list_advisories`).
- Test functions use `test_` prefix with descriptive snake_case names.

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping on error paths.
- 404 errors use `AppError::NotFound` (or equivalent) with a descriptive context message.

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-resource endpoints return `Json<T>` directly.

### Framework patterns
- Axum for HTTP routing and extractors (`Path`, `Extension`, `Json`).
- SeaORM for database queries with entity definitions in `entity/src/`.
- Route registration in `endpoints/mod.rs`; server mounting in `server/src/main.rs`.

### Test organization
- Integration tests live in `tests/api/` with one file per domain area.
- Tests use a shared test database setup (PostgreSQL).
- HTTP client creation and request building follow a common pattern across test files.
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)`.

### Import organization
- External crate imports first, then internal module imports, consistent with Rust convention.

## Conflicting Conventions

### CONFLICT: Assertion style -- existence checks vs. value-based assertions

**Sibling pattern** (from `tests/api/advisory.rs` and `tests/api/sbom.rs`):

```rust
// Pattern 1: .filter().any() -- existence check
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// Pattern 2: .filter().count() > 0 -- existence check
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

Both patterns check only for existence (does at least one matching item exist?) without
verifying specific values, exact counts, or the content of matched items. When these
assertions fail, the error message reveals only that something was missing, not what
was actually present.

**Skill guidance** (Step 7 -- "Prefer value-based assertions over length-only checks"):

> When verifying collections or response data, assert on the actual values -- not just
> the count. Assert on specific items or key fields so that test failures reveal *what*
> changed, not just *how many*. Length checks alone hide regressions behind a passing
> count and prevent subsequent assertions from running.

**Resolution**: Skill guidance takes PRECEDENCE over sibling patterns. The skill
explicitly states in both Step 4 and Step 7 that its built-in quality guidance overrides
conflicting sibling conventions. Sibling conventions are defaults, not overrides.

For the new `tests/api/package_license.rs` tests:
- Use `assert_eq!` on specific counts (e.g., `assert_eq!(summary.permissive.count, 2)`)
- Use `assert_eq!` on specific license identifiers (e.g., `assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"])`)
- Do NOT use `.filter().any()` or `.filter().count() > 0` patterns

Non-conflicting aspects of sibling test conventions (naming, setup, organization,
status code assertions) are still adopted.
