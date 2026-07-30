# Conventions Discovered from Sibling Analysis for TC-9208

## Production Code Conventions

### Module structure
- Each domain module follows `model/ + service/ + endpoints/` directory structure.
- New model files are declared in `model/mod.rs` with `pub mod <name>;`.
- New endpoint files are declared in `endpoints/mod.rs` with `pub mod <name>;` and route registration in the same file.

### Endpoint handler pattern
- **Framework**: Axum for HTTP routing and extractors.
- **Handler signature**: all handlers return `Result<T, AppError>` where `T` is typically `Json<ResponseType>`.
- **Path parameters**: extracted via Axum's `Path` extractor (e.g., `Path(id): Path<Uuid>`).
- **Error handling**: all handlers use `AppError` with `.context()` wrapping for error messages. 404 responses use a specific `AppError::NotFound` variant (or similar).

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-resource endpoints return the domain struct directly wrapped in `Json<T>`.
- The license summary endpoint is a single-resource response (not paginated), so it should return `Json<LicenseSummary>`.

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`).
- Model structs use PascalCase domain names (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`).
- Endpoint handler files are named by action (e.g., `list.rs`, `get.rs`).

### ORM and database
- SeaORM for database access.
- Entity definitions in `entity/src/` (e.g., `package_license.rs`).
- JOIN queries use SeaORM's relation and linked APIs.

### Derive macros and serde
- Model structs derive: `Clone`, `Debug`, `Serialize`, `Deserialize`, `ToSchema` (for OpenAPI via utoipa).
- Default derives may also be used where applicable.

### Import organization
- Standard library imports first, then external crates, then internal modules (standard Rust convention).

## Test Conventions

### Test file organization
- Integration tests live in `tests/api/` directory.
- Each test file covers one domain area (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database (not mocks).

### Test naming
- Tests follow `test_<endpoint>_<scenario>` naming pattern.

### Test setup
- Tests use shared test infrastructure for database setup and HTTP client creation.
- Setup creates test data in the database, then exercises the endpoint via HTTP.

### Assertion style (sibling pattern)
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)` for success, `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404.
- Response body: deserialized into typed structs, then fields checked.

### Assertion style (sibling pattern -- CONFLICT WITH SKILL GUIDANCE)

**Sibling pattern (from `tests/api/advisory.rs` and `tests/api/sbom.rs`):**
```rust
// Existence-only checks using .filter().any() or .filter().count() > 0
let has_critical = result.items.iter()
    .filter(|a| a.severity == "Critical")
    .any(|_| true);
assert!(has_critical, "should contain a Critical advisory");

let matching = result.items.iter()
    .filter(|s| s.name.contains("openssl"))
    .count();
assert!(matching > 0, "should find at least one openssl SBOM");
```

**Skill guidance (Step 7 -- overrides sibling pattern):**
> "Prefer value-based assertions over length-only checks: When verifying collections or response data, assert on the actual values -- not just the count. Assert on specific items or key fields so that test failures reveal *what* changed, not just *how many*. Length checks alone hide regressions behind a passing count and prevent subsequent assertions from running."

**Resolution:** The skill explicitly states "Skill guidance overrides sibling patterns" and "Skill guidance takes precedence over sibling patterns." Therefore, the new tests for TC-9208 will NOT follow the sibling `.any()` / `.count() > 0` existence-check pattern. Instead, they will use value-based assertions that check specific license identifiers and exact counts, so test failures reveal what changed rather than just that something changed.

**What we adopt from siblings:**
- File location pattern (`tests/api/`)
- Test naming convention (`test_<endpoint>_<scenario>`)
- Status code assertion style (`assert_eq!(resp.status(), StatusCode::OK)`)
- Test setup and database seeding approach
- Response deserialization into typed structs

**What we override (per skill guidance):**
- Assertion style: use `assert_eq!` with specific values instead of `.filter().any()` / `.count() > 0`

### Test documentation (skill-mandated, not from siblings)
- Every test function must have a `///` doc comment explaining what it verifies.
- Non-trivial tests must include `// Given`, `// When`, `// Then` section comments.
- This is applied regardless of whether sibling tests have documentation, per the skill's explicit instruction.

### Parameterized tests
- Sibling tests do not appear to use `#[rstest]` or parameterized test patterns.
- Per skill guidance: "if the sibling test analysis shows the project does not use parameterized tests, do not introduce them -- follow the project's existing test patterns instead."
- Therefore, parameterized tests will NOT be introduced for TC-9208.

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root. Its contents would be read during implementation to extract:
- Additional naming rules or directory structure conventions
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`)
- Code generation commands (if any)

These would be followed during implementation and used for CI verification in Step 9.
