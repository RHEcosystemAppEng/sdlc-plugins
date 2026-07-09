# Discovered Conventions for TC-9201

## Production Code Conventions (from sibling analysis)

### Error Handling
- All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped using `.context()` to add descriptive messages at each layer (endpoint -> service -> database)
- `AppError` implements `IntoResponse` for automatic HTTP error response conversion
- 404 errors are returned when a requested entity does not exist, consistent across all GET endpoints

### Module Structure (model/service/endpoints)
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure
- Models are defined in `model/` with one file per struct (e.g., `summary.rs`, `details.rs`)
- Model sub-modules are registered in `model/mod.rs` via `pub mod <name>;`
- Services are defined in `service/` and contain business logic methods
- Endpoints are defined in `endpoints/` with one file per HTTP handler
- Route registration happens in `endpoints/mod.rs` using `Router::new().route(...)` pattern

### Service Method Signatures
- Service methods follow the `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`)
- All service methods accept `&self` as the first parameter
- Database-accessing methods take `tx: &Transactional<'_>` as the last parameter for transaction support
- Methods return `Result<T, AppError>` using the standard error type

### Endpoint Handler Pattern
- Path parameters are extracted via Axum's `Path<Id>` extractor
- Handlers call the corresponding service method and return the result
- Response types are returned directly -- Axum's `Json` extractor handles serialization
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-item endpoints return the model struct directly wrapped in `Json`

### Route Registration
- Routes are registered in each module's `endpoints/mod.rs`
- Pattern: `Router::new().route("/api/v2/<resource>/<path>", get(handler_function))`
- `server/src/main.rs` mounts all modules -- individual modules do not need to modify `main.rs`

### Derive Macros and Struct Conventions
- Model structs derive `Serialize, Deserialize, Debug, Clone` and `utoipa::ToSchema` for OpenAPI
- Struct fields use standard Rust naming (snake_case)
- Documentation comments are expected on public types and functions

### Database and ORM
- Framework: SeaORM for database access
- Entities are defined in `entity/src/` with one file per table
- Join tables follow `<parent>_<child>.rs` naming (e.g., `sbom_advisory.rs`)
- Shared query helpers for filtering, pagination, and sorting are in `common/src/db/query.rs`

## Test Conventions (from sibling test analysis)

### Assertion Style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks
- Response body is deserialized after status assertion for further field-level checks
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 responses

### Test Setup
- Integration tests hit a real PostgreSQL test database
- Test data is seeded before assertions
- Each test function is independent and sets up its own test state

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` naming pattern (e.g., `test_list_advisories_filtered`)
- Test files are named after the domain they test (e.g., `advisory.rs`, `sbom.rs`)

### Test Organization
- All API integration tests live in `tests/api/` directory
- Tests are organized by domain entity (one file per entity type)
- Each file covers both success and error scenarios for that entity's endpoints

### Test Documentation
- Every test function must have a `///` documentation comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments inside the test body
