# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Error handling
- All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` from the `anyhow` pattern to add context to errors
- `AppError` implements `IntoResponse` for automatic HTTP error response conversion (e.g., not-found maps to 404)

### Module structure
- Each domain module follows the `model/ + service/ + endpoints/` three-directory structure
- `model/mod.rs` declares sub-modules with `pub mod <name>;` for each model struct file
- `service/mod.rs` re-exports the main service file (e.g., `advisory.rs`, `sbom.rs`)
- `endpoints/mod.rs` registers routes and declares sub-modules for each endpoint handler

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- Model structs are named `<Entity><Role>` (e.g., `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`)
- Endpoint handler files are named by action (e.g., `get.rs`, `list.rs`)
- Endpoint handler functions mirror the file name (e.g., `get` in `get.rs`, `list` in `list.rs`)

### Service method signatures
- Service methods take `&self` as the receiver
- ID parameters use the `Id` type
- Database transaction context is passed as `tx: &Transactional<'_>`
- Return type is `Result<ModelStruct, AppError>`

### Endpoint handler patterns
- Path parameters extracted via `Path<Id>` (Axum extractor)
- Service is obtained from application state
- Handler calls service method, awaits result, and returns `Json<T>`
- Handler return type is `Result<Json<T>, AppError>`

### Route registration
- Routes registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- Route paths follow REST conventions (e.g., `/api/v2/advisory`, `/api/v2/advisory/{id}`)

### Response types
- Single-entity endpoints return the model struct directly wrapped in `Json<T>`
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Shared query helpers for filtering, pagination, and sorting from `common/src/db/query.rs`

### Serialization
- Model structs derive `Serialize`, `Deserialize` (serde)
- OpenAPI schema generation via `utoipa::ToSchema` derive

### Import organization
- Standard library imports first, then external crates, then internal modules (Rust convention)

## Test Conventions (from sibling test analysis)

### Assertion style
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code verification
- Response body deserialized from JSON and fields asserted individually with `assert_eq!`

### Response validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate the primary identifier and key fields of the returned struct

### Error cases
- All endpoint test files include a 404 test case with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- 404 tests use a non-existent/random ID to trigger the not-found path

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test setup
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Test fixtures are created in setup functions before assertions
- Cleanup is implicit (test database reset between runs)

### Test organization
- One test file per endpoint group in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests grouped by success and failure scenarios within each file
