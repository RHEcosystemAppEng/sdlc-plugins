# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` structure
- Model modules use a `mod.rs` barrel file that re-exports submodules (e.g., `pub mod summary;`, `pub mod details;`)
- Service modules use a `mod.rs` barrel and a dedicated `<domain>.rs` implementation file (e.g., `service/advisory.rs`)
- Endpoint modules use a `mod.rs` for route registration and separate files per handler (e.g., `list.rs`, `get.rs`)

### Naming Conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`)
- Model structs follow `<Domain><Role>` pattern (e.g., `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`)
- Endpoint handler files are named after the HTTP operation (e.g., `get.rs`, `list.rs`)
- Route registration files are always `mod.rs` within the `endpoints/` directory

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context()` method for adding context to errors
- `AppError` implements `IntoResponse` for automatic HTTP error responses

### Endpoint Patterns
- Path parameters extracted via `Path<Id>` extractor (Axum)
- Service is called with the extracted parameters and a transactional reference
- Response returned directly as struct (Axum's `Json` extractor handles serialization)
- Route registration uses `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`

### Service Patterns
- Service methods take `&self`, entity ID, and `tx: &Transactional<'_>` as parameters
- Services are struct-based with methods (e.g., `AdvisoryService`, `SbomService`)
- Database access uses SeaORM entities and query builders

### Response Types
- Single-entity endpoints return the struct directly (serialized to JSON)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers (filtering, pagination, sorting) come from `common/src/db/query.rs`

### Import Organization
- Framework imports (axum, sea-orm) first
- Common/shared imports second
- Module-local imports last

## Test Conventions

### Assertion Style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks
- Response body is deserialized and validated after status check

### Error Cases
- All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent IDs

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test Setup
- Integration tests hit a real PostgreSQL test database
- Test data is seeded before assertions

### Test Organization
- Tests grouped by domain in separate files under `tests/api/`
- Each file covers one domain's endpoints (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

### Parameterized Tests
- No evidence of parameterized test usage (e.g., `#[rstest]`) in sibling test files; individual test functions are used instead
