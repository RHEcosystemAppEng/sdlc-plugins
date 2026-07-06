# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure.
- Each sub-directory has a `mod.rs` that re-exports or registers child modules (e.g., `pub mod summary;` in `model/mod.rs`).

### Naming conventions
- Model structs use PascalCase nouns: `AdvisorySummary`, `SbomDetails`, `PackageSummary`.
- Model files use snake_case matching the struct concept: `summary.rs`, `details.rs`.
- Service files are named after the domain entity: `advisory.rs`, `sbom.rs`.
- Service methods follow `verb_noun` pattern: `fetch`, `list`, `search`, `ingest`.
- Endpoint handler files are named after the HTTP operation: `get.rs`, `list.rs`.

### Error handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Errors are wrapped using `.context()` for descriptive error messages.
- `AppError` implements `IntoResponse` for automatic HTTP error conversion.

### Endpoint registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`.
- Routes are composed into the parent router; `server/main.rs` mounts all modules.
- Path parameters are extracted via `Path<Id>` extractor.

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the struct directly wrapped in Axum's `Json` extractor.
- All response structs derive `Serialize` (and likely `Deserialize`).

### Database access
- SeaORM is used for all database operations.
- Service methods accept `&self`, domain-specific IDs, and `tx: &Transactional<'_>` for transaction support.
- Join tables (e.g., `sbom_advisory`, `sbom_package`) are used for many-to-many relationships.

### Import organization
- Entity imports come from the `entity` crate (e.g., `entity::sbom_advisory`).
- Common utilities are imported from the `common` crate.
- Module-internal imports use relative paths.

## Test Conventions

### Assertion style
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Body is deserialized and fields are checked with `assert_eq!` on specific values.

### Response validation
- Status code is always checked first.
- Response body is deserialized into the expected struct type.
- Key fields are validated individually rather than comparing entire structs.

### Error cases
- All endpoint test files include a 404 test for non-existent resource IDs.
- Error responses are validated by checking `StatusCode::NOT_FOUND`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test organization
- Integration tests live in `tests/api/` with one file per domain entity.
- Tests hit a real PostgreSQL test database.

### Test setup
- Test fixtures are created in the database before assertions.
- Each test function sets up its own data (no shared mutable state between tests).
