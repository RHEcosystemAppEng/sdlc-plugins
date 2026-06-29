# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module structure
- Every domain module follows the `model/ + service/ + endpoints/` three-directory pattern (observed in `sbom/`, `advisory/`, `package/`).
- Each sub-directory has a `mod.rs` that re-exports public items and registers sub-modules.

### Naming conventions
- **Service methods** follow `verb_noun` pattern: `fetch`, `list`, `search`, `ingest` (observed in `SbomService` and `AdvisoryService`).
- **Model structs** use `<Entity>Summary` for list-level representations and `<Entity>Details` for full representations (observed in `SbomSummary`/`SbomDetails`, `AdvisorySummary`/`AdvisoryDetails`).
- **Endpoint files** are named after the HTTP verb or action: `list.rs`, `get.rs`.
- **Model files** are named after the representation type: `summary.rs`, `details.rs`.

### Error handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- Errors are wrapped using `.context()` for descriptive error messages.

### Endpoint registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`.
- `server/main.rs` mounts all modules (routes auto-mount via module registration).

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-resource endpoints return the struct directly via Axum's `Json` extractor.

### Framework
- **HTTP framework**: Axum (path extraction via `Path<Id>`, JSON responses via `Json`).
- **ORM**: SeaORM for database entities.
- **Caching**: `tower-http` caching middleware configured in endpoint route builders.

### Path parameter extraction
- Endpoint handlers extract path params using Axum's `Path<Id>` extractor (observed in `get.rs` handlers).

### Service method signatures
- Service methods follow the pattern: `&self, <entity_id>: Id, tx: &Transactional<'_>` (observed in `AdvisoryService::fetch` and `AdvisoryService::list`).

## Test Conventions

### Test location
- Integration tests reside in `tests/api/` and are named after the domain entity: `sbom.rs`, `advisory.rs`, `search.rs`.

### Test infrastructure
- Tests hit a real PostgreSQL test database (not mocked).

### Assertion style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response bodies are deserialized and validated field-by-field.

### Error case coverage
- Sibling tests include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
