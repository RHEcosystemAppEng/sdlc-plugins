# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Sibling analysis: endpoint handlers

**Siblings analyzed:**
1. `modules/fundamental/src/advisory/endpoints/get.rs` — GET /api/v2/advisory/{id}
2. `modules/fundamental/src/advisory/endpoints/list.rs` — GET /api/v2/advisory
3. `modules/fundamental/src/sbom/endpoints/get.rs` — GET /api/v2/sbom/{id}

**Discovered conventions:**

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`. Errors are never silenced; every fallible call is wrapped with a contextual message.
- **Path parameter extraction:** Handlers that operate on a single resource extract the ID using Axum's `Path<Id>` extractor as a function parameter.
- **Service call pattern:** Handlers call the corresponding service method, passing `&self`, the entity ID, and `tx: &Transactional<'_>` for database transaction context.
- **Response serialization:** Return types are returned directly as structs; Axum's `Json` extractor handles serialization. Single-entity endpoints return `Json<T>`, not `PaginatedResults<T>`.
- **Route registration:** Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` chaining. New routes are added by appending `.route(...)` calls.
- **Module re-exports:** Each `model/mod.rs` re-exports sub-module types via `pub mod <module_name>;` declarations.

### Sibling analysis: service methods

**Siblings analyzed:**
1. `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService with `fetch` and `list` methods
2. `modules/fundamental/src/sbom/service/sbom.rs` — SbomService with `fetch`, `list`, `ingest` methods

**Discovered conventions:**

- **Method signature:** Service methods take `&self`, an entity-specific parameter (e.g., ID or filter), and `tx: &Transactional<'_>` as the transaction context.
- **Naming:** Service methods follow `verb_noun` or simple verb pattern (e.g., `fetch`, `list`, `search`, `ingest`).
- **Error propagation:** Methods return `Result<T, AppError>` and use `.context()` for error wrapping, consistent with the handler layer.

### Sibling analysis: model structs

**Siblings analyzed:**
1. `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct (includes `severity` field)
2. `modules/fundamental/src/advisory/model/details.rs` — AdvisoryDetails struct
3. `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary struct

**Discovered conventions:**

- **Derive macros:** Model structs derive `Serialize`, `Deserialize`, `Debug`, and `Clone` at minimum for API response types.
- **File naming:** Each model struct lives in its own file named after the concept (e.g., `summary.rs`, `details.rs`).
- **Module registration:** New model files are registered in `model/mod.rs` via `pub mod <name>;`.

## Test Conventions

### Sibling test analysis

**Siblings analyzed:**
1. `tests/api/advisory.rs` — Advisory endpoint integration tests
2. `tests/api/sbom.rs` — SBOM endpoint integration tests

**Discovered conventions:**

- **Assertion style:** All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for success checks, followed by body deserialization into the expected response struct.
- **Error case pattern:** All endpoint tests include a 404 test verifying `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs.
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_success`, `test_list_sboms_filtered`).
- **Test database:** Integration tests hit a real PostgreSQL test database, not mocks.
- **Test organization:** Tests are grouped by endpoint/feature within a single file per domain module.

## Framework and Tooling

- **HTTP framework:** Axum
- **ORM:** SeaORM
- **Database:** PostgreSQL
- **Caching:** tower-http caching middleware
- **Response wrappers:** List endpoints use `PaginatedResults<T>` from `common/src/model/paginated.rs`; single-entity endpoints return the struct directly via `Json<T>`.
