# Discovered Conventions (from sibling code analysis)

## Production Code Conventions

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Errors are wrapped using `.context()` from the `anyhow` crate to add descriptive context before returning.
- Service methods propagate errors via `?` with `.context()` wrapping for each fallible operation.

### Module Structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure.
- Models are registered via `pub mod <name>;` in the module's `model/mod.rs`.
- Services are implemented as structs with methods that take `&self`, an ID or query parameter, and `tx: &Transactional<'_>`.
- Endpoints are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.

### Naming Conventions
- Service methods follow a `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- Model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `SbomDetails`).
- Endpoint handler files are named after their action (e.g., `get.rs`, `list.rs`).
- New model files are named after the struct they contain (e.g., `summary.rs`, `details.rs`).

### Endpoint Patterns
- Path parameters are extracted via Axum's `Path<Id>` extractor.
- Service is called to perform business logic; handlers do not contain business logic directly.
- Responses are returned as the struct directly; Axum's `Json` extractor handles serialization.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the model struct directly wrapped in `Json`.

### Import Organization
- Standard library imports first, then external crates, then internal modules.
- Axum extractors and types imported from `axum::extract` and `axum::Json`.
- Service types imported from the module's service submodule.

### Response Types
- Structs derive `Serialize`, `Deserialize`, `Debug` at minimum.
- Response structs use serde attributes for field naming as needed.

### Framework
- HTTP framework: Axum
- ORM: SeaORM for database operations
- Route mounting: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules automatically.

## Test Conventions

### Assertion Style
- Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for successful responses.
- Response bodies are deserialized from JSON and individual fields are checked with `assert_eq!`.

### Response Validation
- Status codes are checked first, then body content.
- For single-item endpoints, specific field values are asserted.
- For list endpoints, `total_count`, `items.len()`, and at least one item's key fields are validated.

### Error Cases
- All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Non-existent IDs are tested to confirm proper error responses.

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test Setup
- Tests hit a real PostgreSQL test database.
- Test data is seeded before assertions.
- Each test function is independent and sets up its own required state.

### Test Organization
- One test file per domain area in `tests/api/`.
- Tests grouped logically within the file (success cases first, then error cases).
