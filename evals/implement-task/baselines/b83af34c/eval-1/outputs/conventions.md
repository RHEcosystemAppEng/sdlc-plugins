# Discovered Conventions

## Production Code Conventions (from sibling analysis)

### Error handling
- All handlers in `modules/fundamental/src/advisory/endpoints/` return `Result<T, AppError>` with `.context()` for wrapping errors.
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse` for Axum.
- Sibling pattern: service methods return `Result<T, anyhow::Error>` or `Result<T, AppError>`, and endpoint handlers wrap errors with `.context("descriptive message")`.

### Naming conventions
- **Service methods**: follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` on `AdvisoryService`).
- **Endpoint handler functions**: named after the action (e.g., `get`, `list`) in their respective files.
- **Model structs**: named `<Entity><Role>` (e.g., `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`).
- **Endpoint files**: named after the HTTP action (e.g., `get.rs`, `list.rs`).
- **Model files**: named after the role (e.g., `summary.rs`, `details.rs`).
- **Test files**: named after the entity being tested (e.g., `advisory.rs`, `sbom.rs`) in `tests/api/`.

### Module structure
- Each domain module follows `model/ + service/ + endpoints/` structure.
- `model/mod.rs` declares submodules with `pub mod <name>;`.
- `service/mod.rs` re-exports or contains the primary service.
- `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`.

### Endpoint patterns
- Path parameters extracted via Axum's `Path<Id>` extractor.
- Service called with `(&self, id: Id, tx: &Transactional<'_>)` signature.
- Response returned as `Json<T>` (Axum handles serialization).
- Routes registered in `endpoints/mod.rs` following `Router::new().route(...)` pattern.

### Response types
- Single-entity endpoints return the entity struct directly (wrapped in `Json<T>`).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new endpoint is a single-entity aggregation, so it returns `Json<SeveritySummary>` directly (not paginated).

### Import organization
- External crate imports first (`use axum::...`, `use serde::...`).
- Internal crate imports next (`use crate::...`).
- Local module imports last (`use super::...`).

### Database patterns
- SeaORM used for database operations.
- Join tables accessed via entity relations (e.g., `sbom_advisory` for SBOM-to-Advisory joins).
- Queries built using SeaORM's query builder with `.find_related()` or explicit joins.
- Transactional context passed as `tx: &Transactional<'_>`.

### Options/parameter propagation
- Service methods accept `&self` plus domain-specific parameters and a transactional context (`tx`).
- Configuration flows through the service struct's fields (set at construction).

## Test Conventions (from sibling test analysis)

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Response body deserialized via `resp.json::<T>()` or equivalent.

### Response validation
- Endpoint tests validate key fields of the response struct.
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Single-entity tests validate the specific fields of interest.

### Error cases
- All endpoint test suites include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- 404 tests use a non-existent ID (e.g., UUID::nil() or a known-invalid ID).

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test setup
- Integration tests hit a real PostgreSQL test database.
- Test fixtures created via ingestion or direct database insertion.
- Tests use a shared test harness for setting up the application context.

### Test documentation
- Per skill guidance (Step 7), every test function must have a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- This is a skill standard that overrides the sibling pattern if siblings lack doc comments.

### Parameterized tests
- No parameterized test usage observed in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).
- Per skill guidance, will not introduce parameterized tests since the project does not use them.

## CONVENTIONS.md

Would read `./CONVENTIONS.md` at the repository root. Key items to extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`)
- Code generation commands (e.g., OpenAPI spec generation)
- Any naming rules, directory structure rules, or test conventions that supplement the sibling analysis above
