# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows the `model/ + service/ + endpoints/` triple structure (observed in `sbom/`, `advisory/`, `package/`)
- Model module has a `mod.rs` that re-exports sub-modules (e.g., `summary`, `details`)
- Service module has a `mod.rs` that re-exports the service implementation file
- Endpoints module has a `mod.rs` for route registration plus individual handler files

### Naming Conventions
- **Model structs**: `<Entity>Summary`, `<Entity>Details` pattern (e.g., `SbomSummary`, `SbomDetails`, `AdvisorySummary`, `AdvisoryDetails`)
- **Service structs**: `<Entity>Service` pattern (e.g., `SbomService`, `AdvisoryService`, `PackageService`)
- **Service methods**: verb_noun pattern (`fetch`, `list`, `search`, `ingest`)
- **Endpoint handler files**: named by action (`list.rs`, `get.rs`)
- **Endpoint paths**: `/api/v2/<entity>` for list, `/api/v2/<entity>/{id}` for get

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`

### Framework Patterns
- **HTTP**: Axum for HTTP framework
- **ORM**: SeaORM for database access
- **Route registration**: Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`; single-item endpoints return the struct directly via Axum's `Json` extractor
- **Path parameters**: Extracted via Axum's `Path<Id>` extractor
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Import Organization
- Entity models imported from `entity/src/` crate
- Common utilities imported from `common/src/` crate
- Cross-module references use crate-level imports

### Service Method Signatures
- Service methods take `&self` as first argument
- Methods that need database access take `tx: &Transactional<'_>` as a parameter
- ID parameters use the `Id` type

## Test Conventions

### Test Location and Organization
- Integration tests live in `tests/api/` directory
- Test files are named after the domain entity being tested (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- Tests hit a real PostgreSQL test database

### Assertion Style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response bodies are deserialized from JSON and validated field-by-field
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 responses

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Response Validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-item endpoint tests validate key fields of the returned entity

### Error Case Coverage
- All endpoint test files include a 404 test with non-existent ID
- Consistent use of StatusCode enum variants for assertions
