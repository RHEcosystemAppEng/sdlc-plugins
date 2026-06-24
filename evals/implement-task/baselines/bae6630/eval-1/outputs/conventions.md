# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Directory & Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` structure
- Model modules are registered via `pub mod <name>;` in the parent `model/mod.rs`
- Endpoint modules are registered and routes are mounted in `endpoints/mod.rs`
- Routes auto-mount via module registration in `server/src/main.rs` -- no manual changes needed there

### Endpoint Patterns (from `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`)

- Path parameters extracted via Axum's `Path<Id>` extractor
- Service called with `(&self, id: Id, tx: &Transactional<'_>)` signature pattern
- Return type: `Result<Json<T>, AppError>` where `T` is the response struct
- JSON serialization handled automatically by Axum's `Json` extractor wrapper
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Service Method Patterns (from `AdvisoryService::fetch`, `AdvisoryService::list`, `SbomService::fetch`)

- Methods take `&self` as first parameter
- Entity ID parameters use the `Id` type
- Transaction parameter: `tx: &Transactional<'_>`
- Return `Result<T, AppError>` with `.context()` for error wrapping
- Service methods follow `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`)

### Error Handling (from `common/src/error.rs`, sibling handlers)

- All handlers return `Result<T, AppError>`
- Error wrapping uses `.context("descriptive message")` from anyhow/context pattern
- `AppError` implements `IntoResponse` for automatic HTTP status mapping
- 404 errors for missing entities use `AppError::NotFound` or equivalent variant

### Naming Conventions

- Struct names: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- Method names: snake_case following `verb_noun` pattern (e.g., `fetch`, `list`, `severity_summary`)
- File names: snake_case matching the primary struct or concept (e.g., `summary.rs`, `details.rs`)
- Endpoint paths: kebab-case (e.g., `/api/v2/advisory-summary`)

### Model Patterns (from `AdvisorySummary` in `summary.rs`, `SbomSummary`, `PackageSummary`)

- Structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- Fields use snake_case
- Response structs are plain data transfer objects (no business logic)
- Each model is in its own file within the `model/` directory

### Import Organization

- Standard library imports first
- External crate imports second
- Internal module imports last
- Grouped by crate with blank line separation

### Route Registration (from `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`)

- Routes registered via `Router::new().route("/path", get(handler))` pattern
- Route functions are imported from sibling endpoint modules
- Module-level `pub fn router()` function returns the configured `Router`

## Test Conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`)

### Assertion Style

- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Body deserialization into typed structs for field-level validation
- Value-based assertions preferred over length-only checks

### Response Validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate key fields of the response struct
- JSON shape validated by deserializing into the expected response type

### Error Cases

- All endpoint tests include a 404 test for non-existent resource IDs
- Status code assertion: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test Naming

- Tests follow `test_<endpoint>_<scenario>` pattern
- Examples: `test_get_advisory_by_id`, `test_list_advisories_filtered`, `test_get_sbom_not_found`

### Test Setup

- Integration tests hit a real PostgreSQL test database
- Test fixtures created via service methods or direct database seeding
- Each test function is independent (no shared mutable state between tests)

### Test Organization

- One test file per endpoint group in `tests/api/`
- Tests grouped by HTTP method and scenario within each file

### Parameterized Tests

- Not observed in sibling test files -- will not introduce parameterized test patterns

### Test Documentation

- Per skill requirements, every test function will have a `///` doc comment explaining what it verifies
- Non-trivial tests will include `// Given`, `// When`, `// Then` section comments
