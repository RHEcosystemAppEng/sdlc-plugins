# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module Structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure
- `model/mod.rs` re-exports sub-modules (e.g., `pub mod summary;`, `pub mod details;`)
- `service/mod.rs` re-exports the service implementation file
- `endpoints/mod.rs` registers routes and re-exports handler modules

### Endpoint Patterns (from `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`)
- Handlers extract path parameters via Axum's `Path<Id>` extractor
- All handlers return `Result<Json<T>, AppError>` where `T` is the response struct
- Error wrapping uses `.context("descriptive message")` (from `anyhow` or similar)
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern
- Single-item endpoints use `GET /api/v2/<entity>/{id}` path pattern
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Service Patterns (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- Service structs named `<Entity>Service` (e.g., `AdvisoryService`, `SbomService`)
- Methods follow `verb_noun` naming: `fetch`, `list`, `search`, `ingest`
- Method signatures include `&self` receiver and `tx: &Transactional<'_>` for database context
- Methods return `Result<T, anyhow::Error>` or equivalent

### Model Patterns (from `advisory/model/summary.rs`, `sbom/model/summary.rs`)
- Structs derive `Serialize, Deserialize, Debug, Clone`
- Summary structs are lightweight projections for list responses
- Detail structs extend summary data with related entities
- Field naming follows Rust conventions (snake_case) with serde renaming for JSON (camelCase) where applicable

### Error Handling (from `common/src/error.rs`)
- Central `AppError` enum that implements `IntoResponse` for Axum
- All service and handler errors are wrapped using `.context()` for descriptive error chains
- HTTP status codes derived from error variants (404 for not-found, 500 for internal errors)

### Framework Stack
- HTTP framework: Axum
- ORM: SeaORM
- Database: PostgreSQL
- Caching middleware: tower-http

### Import Organization
- Standard library imports first, then external crates, then internal modules
- Grouped by origin with blank lines between groups

## Test Conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

### Assertion Style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Response bodies deserialized via `.json::<ResponseType>().await`

### Response Validation
- Status code checked first
- Body structure validated with field-level assertions
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields

### Error Cases
- All endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Non-existent IDs tested to confirm proper error responses

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test Setup
- Integration tests hit a real PostgreSQL test database
- Test fixtures created via service methods or direct database seeding
- Each test function is independent (no shared mutable state between tests)

### Test Organization
- Tests grouped by API domain in `tests/api/<domain>.rs`
- Each file covers one domain's endpoints
