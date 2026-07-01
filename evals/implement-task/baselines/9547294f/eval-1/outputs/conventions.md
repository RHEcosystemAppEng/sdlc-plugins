# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module structure
- Each domain module (sbom, advisory, package) follows the `model/ + service/ + endpoints/` tri-directory structure
- Model modules are registered via `pub mod <name>;` in `model/mod.rs`
- Endpoint modules are registered via route declarations in `endpoints/mod.rs`

### Error handling
- All handlers in `endpoints/` return `Result<T, AppError>` with `.context()` for wrapping errors
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`
- 404 errors use `AppError::NotFound` or equivalent variant (matching existing SBOM endpoints)

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Endpoint handler files are named after their HTTP action or resource (e.g., `get.rs`, `list.rs`)
- Model struct files are named after the concept they represent (e.g., `summary.rs`, `details.rs`)
- Test files in `tests/api/` are named after the domain entity (e.g., `sbom.rs`, `advisory.rs`)

### Service method signatures
- All service methods on `AdvisoryService` take `&self` as the receiver
- Methods accept domain-specific identifiers (e.g., `Id` type for entity IDs)
- Methods accept `tx: &Transactional<'_>` as a parameter for database transaction context
- Return types are `Result<T, Error>` where `T` is the domain model

### Endpoint handler patterns
- Path parameters extracted via Axum's `Path<Id>` extractor
- Handler calls the corresponding service method
- Response returned directly as the struct (Axum's `Json` extractor handles serialization)
- Route registration follows `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the model struct directly (e.g., `AdvisoryDetails`, `SbomDetails`)
- Aggregation endpoints (like the new severity summary) return a dedicated response struct

### Import organization
- Standard library imports first
- External crate imports second
- Internal crate imports third (using `crate::` paths)

### Database patterns
- SeaORM for database access
- Join tables used for many-to-many relationships (e.g., `sbom_advisory` for SBOM-Advisory links)
- Query builder helpers from `common/src/db/query.rs` for filtering, pagination, sorting

### Option/parameter propagation
- Configuration flows through service constructors
- Transaction context passed explicitly via `Transactional` parameter

## Test Conventions

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Response body is deserialized into the expected struct type for field-level assertions

### Response validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate specific field values after deserialization
- Aggregation tests should validate each field of the response struct individually

### Error cases
- All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs
- Error response body is validated when the error type includes a message

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Descriptive scenario suffixes: `_valid`, `_not_found`, `_empty`, `_deduplicated`

### Test setup and teardown
- Integration tests hit a real PostgreSQL test database
- Test fixtures are created via service methods or direct database insertion
- Each test function sets up its own data context

### Test organization
- Tests grouped by endpoint in a single file per domain (e.g., `tests/api/advisory.rs`)
- Related scenarios are in the same file, ordered: happy path first, then error cases

### Parameterized tests
- No parameterized test usage observed in sibling test files; individual test functions are used for each scenario

### Documentation
- AI-generated tests introduce documentation comments (`///`) on every test function describing what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments
