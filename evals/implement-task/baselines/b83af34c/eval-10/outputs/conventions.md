# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Error handling
All handlers in `modules/fundamental/src/*/endpoints/` return `Result<T, AppError>`
with `.context()` for error wrapping. Errors propagate via the `?` operator.
(Source: `list.rs`, `get.rs` in sbom and advisory endpoints)

### Module structure
Each domain module follows a consistent `model/ + service/ + endpoints/` directory
layout. Models are separate files under `model/`, re-exported via `model/mod.rs`.
(Source: sbom, advisory, and package modules)

### Naming
- Endpoint handler files are named by action: `list.rs`, `get.rs`
- Model files are named by concept: `summary.rs`, `details.rs`
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`)

### Route registration
Each module's `endpoints/mod.rs` registers routes using Axum's router builder.
The `server/main.rs` mounts all modules.

### Response types
List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Single-entity endpoints return the model struct directly.

### Import organization
Standard library imports first, then external crates, then internal modules.

## Test Conventions

### Test file location and naming
Integration tests reside in `tests/api/` and are named after the domain entity:
`sbom.rs`, `advisory.rs`, `search.rs`. New test file should be `package_license.rs`.

### Test function naming
Tests follow the `test_<endpoint>_<scenario>` pattern (e.g.,
`test_list_advisories_filtered`, `test_get_sbom_not_found`).

### Test setup
Tests hit a real PostgreSQL test database. Setup involves creating test fixtures
(e.g., ingesting test SBOMs or advisories) before making HTTP requests.

### Response status assertion
All endpoint tests begin with `assert_eq!(resp.status(), StatusCode::OK)` or the
expected status code, followed by body deserialization.

### Error case coverage
All endpoint test files include a 404 test using
`assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Assertion style (CONFLICT DETECTED)

**Sibling pattern observed:** Sibling test files (`tests/api/advisory.rs`,
`tests/api/sbom.rs`) use existence-checking assertion patterns:

```rust
// Pattern 1: .filter().any()
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

// Pattern 2: .filter().count() > 0
let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

These patterns only verify that at least one matching item exists. They do not
assert on specific values, counts, or field contents. A regression that changes
the returned data (e.g., wrong license identifiers, incorrect categorization)
could pass these checks as long as at least one item superficially matches.

**Skill guidance (Step 7):** "Prefer value-based assertions over length-only
checks: When verifying collections or response data, assert on the actual values
-- not just the count. Assert on specific items or key fields so that test failures
reveal *what* changed, not just *how many*."

**Resolution:** Per Step 4's explicit rule -- "Skill guidance takes precedence over
sibling patterns" -- the new tests will NOT adopt the `.any()` / `.count() > 0`
patterns from siblings. Instead, they will use value-based assertions such as
`assert_eq!` on specific counts and `assert_eq!` or `assert!` with exact value
comparisons on license identifiers. The conflict is noted here but the skill's
quality standard is the binding reference.

## Non-Conflicting Conventions (adopted from siblings)

The following sibling conventions do NOT conflict with skill guidance and will
be adopted in the implementation:

- Test file naming: `package_license.rs` in `tests/api/`
- Test function naming: `test_<endpoint>_<scenario>` pattern
- Test setup: real PostgreSQL test database with fixture ingestion
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Error case: dedicated 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response deserialization pattern from siblings
- Production code error handling with `Result<T, AppError>` and `.context()`
