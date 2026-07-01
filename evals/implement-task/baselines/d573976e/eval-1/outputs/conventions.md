# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure.
- Module registration uses `pub mod <name>;` in the parent `mod.rs`.

### Endpoint patterns
- All endpoint handlers in `modules/fundamental/src/*/endpoints/` extract path params via Axum's `Path<Id>` extractor.
- All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation, matching the `AppError` enum in `common/src/error.rs`.
- Route registration follows `Router::new().route("/path", get(handler))` pattern in each module's `endpoints/mod.rs`.
- Response types are returned directly (Axum's `Json` extractor handles serialization).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Service patterns
- Service methods follow the signature pattern: `pub async fn verb_noun(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.
- Existing methods include `fetch` and `list` — new methods should follow the same structure.
- Services use SeaORM for database access.

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`).
- Model structs use PascalCase with descriptive suffixes (e.g., `SbomSummary`, `AdvisoryDetails`, `SeveritySummary`).
- Endpoint handler files are named after their operation (e.g., `get.rs`, `list.rs`, `severity_summary.rs`).

### Error handling
- All errors use `AppError` from `common/src/error.rs`.
- Errors are wrapped with `.context("descriptive message")` for traceability.
- 404 responses are returned when entities are not found, consistent across all SBOM and advisory endpoints.

### Model patterns
- Model structs derive `Serialize`, `Deserialize` (serde) for JSON serialization.
- Each model file is registered in the parent `model/mod.rs` via `pub mod <name>;`.
- Summary structs (e.g., `AdvisorySummary`) include key fields for aggregation — the `severity` field on `AdvisorySummary` is used for severity counting.

### Import organization
- Standard library imports first, then external crate imports, then local crate imports.

### Caching
- Uses `tower-http` caching middleware; cache configuration is set in endpoint route builders.

## Test Conventions

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Response body is deserialized to the expected struct type for field-level assertions.

### Response validation
- List/summary endpoint tests validate specific field values, not just presence.
- Error case tests include status code assertions (e.g., `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases).

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_details`).

### Test setup
- Integration tests hit a real PostgreSQL test database.
- Test fixtures are created via service methods or direct entity insertion.

### Error case coverage
- All endpoint test files include at least one 404 test with a non-existent ID.

### Test file organization
- Integration tests are located in `tests/api/` with one file per domain area.
- Test files are registered in `tests/Cargo.toml`.

### Framework conventions
- Framework: Axum for HTTP, SeaORM for database.
- Shared query helpers for filtering, pagination, and sorting in `common/src/db/query.rs`.
