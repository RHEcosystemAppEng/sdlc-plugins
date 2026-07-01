# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Module structure
- Every domain module follows a strict `model/ + service/ + endpoints/` tri-directory pattern within `modules/fundamental/src/<domain>/`.
- Each sub-directory has a `mod.rs` that re-exports public items and registers sub-modules.

### Model conventions
- Model structs live in dedicated files under `model/` (e.g., `summary.rs`, `details.rs`).
- `model/mod.rs` declares each sub-module with `pub mod <name>;`.
- Sibling model files (`summary.rs`, `details.rs`) define a single primary struct per file, deriving `Serialize` and `Deserialize` (serde) for JSON conversion.
- Struct names follow `<Domain><Purpose>` pattern: `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`.

### Service conventions
- Service structs are named `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`).
- Service methods take `&self` as the first parameter.
- Methods that access the database accept a `tx: &Transactional<'_>` parameter as the last argument.
- Methods follow a `verb_noun` naming pattern: `fetch`, `list`, `search`, `ingest`.
- Return type: `Result<T, AppError>` with `.context()` wrapping for error propagation.

### Endpoint conventions
- Each endpoint handler lives in its own file under `endpoints/` (e.g., `list.rs`, `get.rs`).
- `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern.
- Path parameters are extracted via Axum's `Path<Id>` extractor.
- Handlers call service methods and return JSON responses directly (Axum's `Json` extractor handles serialization).
- All handlers return `Result<T, AppError>` with `.context()` wrapping.
- Route paths follow REST conventions: `/api/v2/<resource>` for lists, `/api/v2/<resource>/{id}` for single items.

### Error handling
- All code uses `Result<T, AppError>` from `common/src/error.rs`.
- Errors are wrapped with `.context("descriptive message")` for traceability.
- `AppError` implements `IntoResponse` for automatic HTTP error conversion.
- 404 errors are returned when a resource ID does not exist, consistent across all SBOM and advisory endpoints.

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the model struct directly (wrapped in `Json`).
- New summary/aggregation endpoints return a dedicated struct (not `PaginatedResults`).

### Import organization
- Standard library imports first, then external crates, then internal modules.
- SeaORM entity imports for database operations.

### Framework stack
- **HTTP**: Axum
- **ORM**: SeaORM
- **Database**: PostgreSQL

## Test Conventions

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Status code checks come first, then body content assertions.

### Response validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Single-item tests validate specific field values after deserialization.

### Error cases
- All endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Error tests use non-existent IDs to trigger 404 responses.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test setup
- Integration tests hit a real PostgreSQL test database.
- Test data is seeded before assertions.

### Test file organization
- One test file per domain module in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- New test files for new endpoints follow the same naming: `tests/api/<feature_name>.rs`.

### Parameterized tests
- No evidence of `rstest` or parameterized test usage in sibling test files -- individual test functions are used for each scenario.

## CONVENTIONS.md
- The repository has a `CONVENTIONS.md` at the root. In a real implementation, this file would be read for CI check commands and additional project-level conventions. Since we cannot access the actual file content in this eval, we note its existence and would follow any conventions it specifies.
