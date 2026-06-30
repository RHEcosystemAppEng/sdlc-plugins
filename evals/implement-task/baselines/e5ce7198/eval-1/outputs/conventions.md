# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Module Structure
- Each domain module follows the `model/ + service/ + endpoints/` directory structure
- Module registration in parent `mod.rs` files via `pub mod <name>;`
- Models, services, and endpoints each have their own `mod.rs` for sub-module registration

### Endpoint Patterns
- **Framework**: Axum for HTTP routing
- **Handler signature**: async functions returning `Result<Json<T>, AppError>`
- **Path parameter extraction**: `Path<Id>` extractor (seen in `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`)
- **Route registration**: each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- **Server mounting**: `server/main.rs` mounts all module routers -- routes auto-mount via module registration, so no changes needed there
- **Response types**: single-entity endpoints return the struct directly via `Json<T>`; list endpoints return `PaginatedResults<T>`

### Service Patterns
- **ORM**: SeaORM for database access
- **Method signature**: service methods take `&self`, entity ID, and `tx: &Transactional<'_>` as parameters
- **Naming**: existing methods follow verb pattern: `fetch`, `list`, `search`
- **Error handling**: all service methods return `Result<T, AppError>` with `.context()` wrapping for error chain propagation

### Error Handling
- All handlers and services use `Result<T, AppError>` return type
- Errors are wrapped with `.context("descriptive message")` for stack trace clarity
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`

### Model Patterns
- Structs derive `Serialize`, `Deserialize` (serde) for JSON serialization
- Model files sit alongside sibling models in the same `model/` directory
- `AdvisorySummary` in `model/summary.rs` has a `severity` field -- the basis for counting

### Database Patterns
- Join tables (e.g., `sbom_advisory.rs` in `entity/src/`) link domain entities
- SeaORM entities defined in `entity/src/` directory
- Query helpers for filtering, pagination, sorting in `common/src/db/query.rs`

## Test Conventions

### Test Structure
- Integration tests live in `tests/api/` directory, organized by domain entity
- Tests hit a real PostgreSQL test database (not mocked)
- Test file naming: `<entity>.rs` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

### Assertion Patterns
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response body deserialized then fields checked individually
- Error cases include 404 tests with appropriate status code assertions

### Test Naming
- Functions follow `test_<endpoint>_<scenario>` pattern (inferred from sibling structure)
- Each test covers a single scenario (valid input, not found, empty result, edge cases)

### Parameterized Tests
- Sibling test files would be inspected for `#[rstest]` / `#[case]` usage
- If siblings do not use parameterized tests, new tests will not introduce them (per constraint 5.10)

### Test Documentation
- Every test function gets a `///` doc comment explaining what it verifies (per constraint 5.11)
- Non-trivial tests get `// Given`, `// When`, `// Then` section comments (per constraint 5.12)

## Naming Conventions

### Files
- Rust source files use snake_case: `severity_summary.rs`
- Module files: `mod.rs` for directories, `<name>.rs` for leaf modules

### Types and Functions
- Structs: PascalCase (e.g., `SeveritySummary`, `AdvisoryService`)
- Functions/methods: snake_case (e.g., `severity_summary`, `fetch`, `list`)
- Service methods: verb-noun or verb pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)

## API Conventions

### URL Patterns
- Base path: `/api/v2/`
- Resource-oriented: `/api/v2/<resource>` for collections, `/api/v2/<resource>/{id}` for single entities
- New endpoint follows nested resource pattern: `/api/v2/sbom/{id}/advisory-summary`

### Response Shapes
- Single entities: direct JSON serialization of struct
- Lists: wrapped in `PaginatedResults<T>` with pagination metadata
- Errors: `AppError` auto-converted to appropriate HTTP status + error body

## Caching
- Uses `tower-http` caching middleware
- Cache configuration available in endpoint route builders
