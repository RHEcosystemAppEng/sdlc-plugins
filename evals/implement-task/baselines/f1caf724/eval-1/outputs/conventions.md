# Convention Conformance Analysis for TC-9201

## Source Files Analyzed

Sibling analysis performed on files in the same directory/module as the files being modified and created:

### Production Code Siblings
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
- `modules/fundamental/src/advisory/model/summary.rs` -- sibling model struct
- `modules/fundamental/src/advisory/model/details.rs` -- sibling model struct
- `modules/fundamental/src/advisory/service/advisory.rs` -- existing service (being modified)

### Test Code Siblings
- `tests/api/advisory.rs` -- sibling advisory test file
- `tests/api/sbom.rs` -- sibling SBOM test file

## Discovered Conventions

### Error Handling
- All handlers and service methods return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` from the anyhow pattern, consistent across all service methods
- 404 errors for not-found entities use AppError variants with appropriate HTTP status mapping

### Module Structure
- Each domain module follows the `model/ + service/ + endpoints/` three-directory structure
- Models are registered in their parent `mod.rs` via `pub mod <name>;` statements
- Services contain the business logic, endpoints handle HTTP concerns (path extraction, JSON serialization)
- Clear separation: endpoints do not contain business logic, services do not handle HTTP types

### Naming Conventions
- Functions follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Structs follow PascalCase with descriptive suffixes (e.g., `AdvisorySummary`, `SbomDetails`, `PaginatedResults`)
- Endpoint handler files are named after the HTTP action or resource (e.g., `get.rs`, `list.rs`)
- Model files are named after the struct they contain (e.g., `summary.rs`, `details.rs`)

### Endpoint Patterns
- Path parameters extracted via Axum's `Path<Id>` extractor
- Response serialization via Axum's `Json<T>` extractor (return struct directly)
- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-item endpoints return the model struct directly wrapped in Json

### Service Method Signatures
- Methods take `&self` as first parameter
- Database transaction parameter: `tx: &Transactional<'_>`
- Entity IDs passed as `Id` type
- Return type: `Result<ModelStruct, AppError>`

### Import Organization
- External crate imports first (serde, axum, sea_orm)
- Internal crate imports next (common, entity)
- Local module imports last

### Testing Conventions
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Test names use `test_` prefix with descriptive snake_case names
- Tests follow setup-action-assertion structure

### Database Access
- SeaORM for all database operations
- Join tables used for many-to-many relationships (e.g., `sbom_advisory`, `sbom_package`)
- Query builders from `common/src/db/query.rs` for shared filtering/pagination/sorting logic

### Response Types
- Individual resource endpoints: `Json<ModelStruct>`
- List endpoints: `Json<PaginatedResults<ModelStruct>>`
- All severity levels default to 0 (not null) in summary responses
