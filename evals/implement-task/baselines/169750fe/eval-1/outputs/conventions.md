# Convention Conformance Analysis

Analyzed sibling files in the advisory module and neighboring modules to establish conventions for implementation.

## Sibling Files Analyzed

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — existing advisory GET endpoint
2. **`modules/fundamental/src/advisory/service/advisory.rs`** — AdvisoryService with fetch/list methods
3. **`modules/fundamental/src/advisory/model/summary.rs`** — AdvisorySummary struct with severity field
4. **`modules/fundamental/src/sbom/endpoints/get.rs`** — SBOM GET endpoint for cross-module pattern comparison
5. **`common/src/error.rs`** — AppError enum and IntoResponse implementation
6. **`tests/api/advisory.rs`** — advisory integration tests

## Discovered Conventions

### Error Handling
- All service methods return `Result<T, AppError>` where `AppError` is from `common/src/error.rs`
- Errors wrapped with `.context("descriptive message")` for debugging context
- 404 cases: service methods return `AppError::NotFound` when entity lookup yields no result
- Pattern: `entity.ok_or_else(|| AppError::NotFound("Advisory not found".into()))?`

### Module Structure
- Each domain follows `model/ + service/ + endpoints/` triple structure
- Model files define response structs with `#[derive(Debug, Clone, Serialize, Deserialize)]`
- Service files contain the business logic with database queries
- Endpoint files contain Axum handler functions

### Endpoint Patterns
- Handler signature: `async fn handler(Path(id): Path<Id>, State(service): State<Arc<AdvisoryService>>, tx: Transactional<'_>) -> Result<Json<T>, AppError>`
- Path parameter extraction via `Path<Id>` Axum extractor
- Service injected via `State<Arc<Service>>`
- Returns `Json<T>` wrapped in `Result` for automatic serialization

### Service Method Patterns
- Method signature: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Uses SeaORM for database queries
- Transaction context passed through all layers

### Route Registration
- `modules/fundamental/src/advisory/endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` chains
- Routes mounted under module prefix (`/api/v2/advisory`)

### Model Conventions
- Derive macros: `#[derive(Debug, Clone, Serialize, Deserialize, utoipa::ToSchema)]`
- Fields use snake_case
- Optional fields use `Option<T>`
- Collections use `Vec<T>`

### Testing Conventions
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database (no mocks)
- Status assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Response body deserialization: `let body: SomeStruct = resp.json().await`
- Test naming: `#[tokio::test] async fn test_<scenario>()`
- Each test sets up its own data, calls the endpoint, and asserts on response values

### Naming Conventions
- Functions: `snake_case` (e.g., `severity_summary`, `fetch`, `list`)
- Types: `PascalCase` (e.g., `SeveritySummary`, `AdvisoryService`)
- Files: `snake_case.rs` matching the primary type they contain
- Test files: named after the domain entity being tested (e.g., `advisory.rs`, `sbom.rs`)

### Import Organization
- Standard library imports first
- External crate imports second
- Internal crate imports last
- Grouped by crate with blank lines between groups
