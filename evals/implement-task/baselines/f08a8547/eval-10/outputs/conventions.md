# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Naming Conventions
- **Files**: snake_case for all source files (e.g., `license_summary.rs`, `summary.rs`, `list.rs`)
- **Modules**: snake_case matching file names; declared with `pub mod <name>;` in parent `mod.rs`
- **Types**: PascalCase for structs (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`)
- **Functions**: snake_case, verb_noun pattern (e.g., `license_summary`, `list`, `get`)
- **Endpoints**: kebab-case URL paths (e.g., `/api/v2/sbom/{id}/license-summary`)

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` tri-directory structure
- Models in `model/` with a `mod.rs` re-exporting sub-modules
- Endpoints in `endpoints/` with a `mod.rs` handling route registration
- Route registration pattern: `endpoints/mod.rs` defines routes, `server/main.rs` mounts modules

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` pattern
- `AppError` implements `IntoResponse` for automatic HTTP error mapping

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-resource endpoints return the model struct directly wrapped in `Json<T>`
- All response structs derive: `Clone`, `Debug`, `Serialize`, `Deserialize`, `ToSchema`

### Import Organization
- Standard library imports first
- External crate imports second
- Internal crate imports third (workspace crates)
- Local module imports last

### API Design Patterns
- RESTful URL structure: `/api/v2/<resource>` for collections, `/api/v2/<resource>/{id}` for single items
- Path parameters use Axum `Path` extractor
- Database connection via Axum `State` extractor
- Query helpers from `common/src/db/query.rs` for filtering, pagination, sorting

### Database Patterns
- SeaORM for all database operations
- Entity definitions in `entity/src/` crate
- JOIN queries built using SeaORM relation definitions
- Shared query builder helpers in `common/src/db/query.rs`

## Test Code Conventions

### Test File Organization
- Integration tests in `tests/api/` directory
- One test file per domain (e.g., `sbom.rs`, `advisory.rs`)
- Tests hit a real PostgreSQL test database

### Test Naming
- Test functions use `test_` prefix with descriptive snake_case names
- Pattern: `test_<action>_<subject>_<condition>` (e.g., `test_list_advisories_by_severity`)

### Test Setup
- Tests create test fixtures directly in the database
- Shared test utilities for database setup/teardown
- Each test function is self-contained with its own setup

### Assertion Style (Sibling Pattern)
- Status code check: `assert_eq!(resp.status(), StatusCode::OK)`
- Collection validation: existence-based using `.filter().any()` or `.filter().count() > 0`

Example from `tests/api/advisory.rs`:
```rust
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");
```

Example from `tests/api/sbom.rs`:
```rust
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

### Error Case Testing
- 404 responses tested with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Tests verify both success and error paths

## Conflicts with Skill Built-in Quality Guidance

### CONFLICT 1: Assertion Style -- Existence Checks vs. Value-Based Assertions

**Sibling pattern**: Siblings use existence-based assertions (`.any()`, `.count() > 0`) that verify an item matching a filter exists in the collection but do not assert on specific counts or exact values.

**Skill guidance (Step 7)**: "Prefer value-based assertions over length-only checks: When verifying collections or response data, assert on the actual values -- not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*. Length checks alone hide regressions behind a passing count and prevent subsequent assertions from running."

**Resolution**: Per the skill's explicit instruction ("Skill guidance takes precedence over sibling patterns"), the new tests will use value-based assertions. Instead of checking `.any()` or `.count() > 0`, tests will assert on exact counts and specific license identifiers in each category.

For example, instead of:
```rust
let has_permissive = result.permissive.licenses.iter().any(|l| l == "MIT");
assert!(has_permissive);
```

The tests will use:
```rust
assert_eq!(result.permissive.count, 2);
assert_eq!(result.permissive.licenses, vec!["Apache-2.0", "MIT"]);
```

This diverges from the sibling test pattern but follows the skill's quality standard.

### CONFLICT 2: Test Documentation

**Sibling pattern**: Sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs` do not include doc comments on test functions.

**Skill guidance (Step 7)**: "Document every test function: Add a documentation comment before every test function explaining what it verifies [...] This applies regardless of whether sibling tests have documentation; AI-generated tests introduce this as a new standard that overrides the 'Follow test conventions' guidance above for documentation specifically."

**Resolution**: Per the skill's explicit instruction, all new test functions will include `///` doc comments. This is a new standard the skill introduces even when siblings lack documentation.

### NO CONFLICT: Given-When-Then Structure

**Sibling pattern**: Sibling tests do not use given-when-then section comments.

**Skill guidance (Step 7)**: Non-trivial tests should include `// Given`, `// When`, `// Then` section comments.

**Resolution**: The skill guidance adds this as a new standard. Since the new tests have distinct setup, action, and assertion phases, they will include given-when-then comments. This is additive, not conflicting -- siblings simply omit these without contradicting them.

## Conventions to Follow (No Conflict)

The following sibling conventions align with the skill's guidance and will be adopted:

1. **Status code assertions**: `assert_eq!(resp.status(), StatusCode::OK)` -- value-based, consistent with skill guidance
2. **Error handling pattern**: `Result<T, AppError>` with `.context()` -- matches Implementation Notes
3. **Response struct derives**: `Clone, Debug, Serialize, Deserialize, ToSchema` -- standard across all models
4. **Module structure**: `model/ + service/ + endpoints/` -- organizational pattern to follow
5. **Route registration**: Declare module in `endpoints/mod.rs`, register route -- matches sibling endpoints
6. **Test file location**: `tests/api/` directory -- follows project layout
7. **Test naming**: `test_` prefix with snake_case descriptive names
