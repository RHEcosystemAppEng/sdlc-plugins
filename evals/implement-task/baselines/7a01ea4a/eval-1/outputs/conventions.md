# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module structure

All domain modules in `modules/fundamental/src/` follow a consistent three-part structure:
- `model/` -- data structs (DTOs/response types) with `mod.rs` re-exporting sub-modules
- `service/` -- business logic and data access methods
- `endpoints/` -- HTTP route handlers with `mod.rs` registering routes

This pattern is observed consistently across `sbom/`, `advisory/`, and `package/` modules. New files must be placed in the correct sub-directory and registered in the corresponding `mod.rs`.

### Error handling

All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`. Errors are wrapped using `.context()` to provide human-readable error messages that describe the operation that failed. This pattern is used consistently across all endpoint handlers and service methods.

Example pattern from sibling code:
```rust
let sbom = self.fetch(sbom_id, tx)
    .await
    .context("Failed to fetch SBOM for severity summary")?;
```

### Endpoint handler pattern

All GET endpoint handlers in `endpoints/` follow this structure:
1. Extract path parameters via Axum's `Path<Id>` extractor
2. Obtain a reference to the service (typically injected via Axum state)
3. Call the appropriate service method
4. Return `Result<Json<T>, AppError>` where `T` is the response struct

This pattern is visible in `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`, and `sbom/endpoints/list.rs`.

### Route registration

Each module's `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` to register routes. Sub-modules are imported with `mod <name>;` and handler functions are referenced in the route definition. The `server/main.rs` mounts all modules automatically.

### Service method signature

Service methods follow the pattern:
```rust
pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>
```

Parameters typically include `&self`, an entity identifier, and a transaction reference. Methods use the `verb_noun` naming convention (e.g., `fetch`, `list`, `search`).

### Struct naming and derives

Model structs (response types) use `#[derive(Serialize, Deserialize, Debug, Clone)]` and include documentation comments. Field names use snake_case. Structs in `model/` are re-exported through `mod.rs` with `pub mod <name>;`.

### Response types

- Single-entity endpoints return `Json<T>` where `T` is the model struct
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new severity summary endpoint returns a single aggregate, so it uses `Json<SeveritySummary>`

### Import organization

Imports are organized with:
1. Standard library imports first
2. External crate imports (serde, axum, sea_orm)
3. Internal crate imports (common::, entity::)
4. Local module imports

## Test Conventions

### Assertion style

All endpoint tests in `tests/api/` use:
```rust
assert_eq!(resp.status(), StatusCode::OK);
```
followed by body deserialization into the expected struct and field-level assertions.

### Response validation

Tests validate specific field values, not just collection lengths. For example, tests check that individual fields like `total`, `critical`, `high` contain expected values rather than just asserting the response was successful.

### Error cases

All endpoint tests include a 404 test case:
```rust
assert_eq!(resp.status(), StatusCode::NOT_FOUND);
```
This is consistent across `tests/api/sbom.rs` and `tests/api/advisory.rs`.

### Test naming

Tests follow the `test_<endpoint>_<scenario>` naming pattern, e.g.:
- `test_get_advisory_summary_valid_sbom`
- `test_get_advisory_summary_not_found`
- `test_get_advisory_summary_empty`
- `test_get_advisory_summary_deduplication`

### Test setup

Integration tests use a real PostgreSQL test database. Test data is seeded by inserting entities directly through the ORM or through ingestion service helpers. Tests clean up or use isolated transactions.

### Test documentation

Every test function will include a `///` documentation comment explaining what it verifies, following the skill's mandatory documentation convention for AI-generated tests. Given-when-then section comments (`// Given`, `// When`, `// Then`) will be used for non-trivial tests.
