# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` three-directory structure
- Module registration is done via `pub mod <name>;` in each directory's `mod.rs`
- Routes auto-mount via module registration in `server/main.rs`

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped with `.context()` for additional context (anyhow-style)
- 404 errors use `AppError` variant for not-found cases, consistent with existing SBOM/advisory endpoints

### Naming Conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Service structs are named `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`, `PackageService`)
- Model structs are named `<Domain><Purpose>` (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- Endpoint handler files are named by action (e.g., `get.rs`, `list.rs`)

### Service Method Signatures
- Service methods take `&self` as the first parameter
- Database-accessing methods take `tx: &Transactional<'_>` as a parameter for transaction support
- ID parameters use the project's `Id` type
- Methods return `Result<T, AppError>`

### Endpoint Patterns (from sibling: `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`)
- Path parameters extracted via Axum's `Path<Id>` extractor
- Service injected via Axum state/extension
- Return `Json<T>` for success responses
- Single-item endpoints return the struct directly (not wrapped in `PaginatedResults`)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Route Registration (from sibling: `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`)
- Routes registered via `Router::new().route("/path", get(handler))` pattern
- Module-level `mod.rs` imports handler modules and builds the router

### Response Types
- Structs derive `Serialize`, `Deserialize` for JSON handling
- Structs derive `utoipa::ToSchema` for OpenAPI documentation
- Fields use standard Rust types (`u64` for counts, `String` for text)

### Import Organization
- External crate imports first, then internal module imports
- Axum extractors imported from `axum::extract`
- Error types imported from `common::error`

## Test Conventions

### Test Location and Structure
- Integration tests live in `tests/api/` directory
- Test files named after the domain being tested (e.g., `sbom.rs`, `advisory.rs`)
- Tests hit a real PostgreSQL test database (not mocked)

### Assertion Patterns (from sibling: `tests/api/advisory.rs`, `tests/api/sbom.rs`)
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)` or `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response body deserialized and fields checked with `assert_eq!`
- Value-based assertions preferred over length-only checks

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`, `test_advisory_summary_not_found`)

### Error Case Coverage
- Every endpoint test suite includes a 404 test for non-existent resources
- Error responses validated for both status code and error structure

### Test Setup
- Test fixtures created via helper functions or direct database insertion
- Each test operates on isolated test data
