# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Module structure
- Each domain module (sbom, advisory, package) follows a consistent `model/ + service/ + endpoints/` directory structure.
- Model modules use a `mod.rs` that re-exports sub-modules (`summary.rs`, `details.rs`).
- Service modules use a `mod.rs` that re-exports the main service file (e.g., `service/mod.rs` re-exports `sbom.rs` or `advisory.rs`).
- Endpoint modules use a `mod.rs` for route registration, with individual handler files (e.g., `list.rs`, `get.rs`).

### Framework and libraries
- **HTTP framework**: Axum for all HTTP handling.
- **ORM**: SeaORM for all database interactions.
- **Caching**: `tower-http` caching middleware configured at the route level.

### Endpoint patterns
- Handlers extract path parameters via `Path<Id>` (Axum extractor).
- Handlers call service methods and return the result directly (Axum's `Json` extractor handles serialization).
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Route registration uses `Router::new().route("/path", get(handler))` pattern in each module's `endpoints/mod.rs`.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the model struct directly (e.g., `SbomDetails`, `AdvisoryDetails`).

### Error handling
- All error wrapping uses `.context()` for adding context to errors (anyhow-style).
- `AppError` implements `IntoResponse` for automatic HTTP error responses.
- Non-existent resources return 404, consistent across all GET-by-ID endpoints.

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`).
- Service method signatures take `&self` plus domain-specific parameters and `tx: &Transactional<'_>` for database transaction context.
- Model structs use PascalCase domain names (e.g., `SbomSummary`, `AdvisoryDetails`, `PackageSummary`).
- Endpoint handler files are named after the HTTP operation they handle (e.g., `get.rs`, `list.rs`).

### Import organization
- Module `mod.rs` files use `pub mod <submodule>;` declarations to register sub-modules.

### Response types
- Aggregation/summary responses use flat structs with typed fields (not nested objects).
- Serialization is derived via `#[derive(Serialize)]` (serde).

### Query patterns
- Shared query builder helpers (filtering, pagination, sorting) live in `common/src/db/query.rs`.
- Join tables (e.g., `sbom_advisory`, `sbom_package`) are used for many-to-many relationships between entities.

## Test Conventions

### Test location and organization
- Integration tests live in `tests/api/` directory, organized by domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database (not mocked).

### Assertion style
- Status code checks use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and checked with `assert_eq!` on specific fields.
- Error cases (e.g., 404) use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test structure
- Tests use given-when-then structure for non-trivial cases.
- Each test function has a documentation comment explaining what it verifies.

## CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root. Its contents would be read and followed during implementation. Verification commands from its CI checks section would be extracted and run during Step 9.
