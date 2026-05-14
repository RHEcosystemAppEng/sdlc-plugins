# Conventions Discovered from Sibling Analysis

## Source Files Analyzed

The following sibling files were inspected to derive conventions:

- `modules/fundamental/src/advisory/endpoints/get.rs` — existing GET endpoint for advisory by ID
- `modules/fundamental/src/advisory/endpoints/mod.rs` — route registration pattern for advisory module
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService with fetch/list/search methods
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct (has `severity` field)
- `modules/fundamental/src/advisory/model/details.rs` — AdvisoryDetails struct
- `modules/fundamental/src/advisory/model/mod.rs` — model module registration
- `common/src/error.rs` — AppError enum and IntoResponse implementation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity
- `tests/api/advisory.rs` — existing advisory integration tests

## Conventions

### 1. Error Handling with `Result<T, AppError>` and `.context()` Wrapping

All fallible operations throughout the codebase use `Result<T, AppError>` as the return type. Every `?` propagation site wraps the error with `.context("descriptive message")` to provide meaningful context for debugging. The `AppError` enum includes variants for common HTTP error responses (e.g., `NotFound` for 404). This pattern is defined in `common/src/error.rs` and used consistently across service methods, endpoint handlers, and database operations. The new `severity_summary` service method and endpoint handler must follow this same pattern.

### 2. Model / Service / Endpoints Module Structure

Each domain module follows a strict three-layer architecture:
- **`model/`** — Data structures for API responses and internal representations. Each model gets its own file (e.g., `summary.rs`, `details.rs`) and is registered in `model/mod.rs` with `pub mod`.
- **`service/`** — Business logic and database queries. Service structs (e.g., `AdvisoryService`) contain methods that accept entity IDs and a `Transactional` context, construct SeaORM queries, and return domain model structs.
- **`endpoints/`** — HTTP handlers and route registration. Each endpoint action gets its own file (e.g., `get.rs`, `list.rs`). The `endpoints/mod.rs` file imports all handler modules and registers their routes on the Axum `Router`.

New functionality must place code in the appropriate layer without mixing concerns across layers.

### 3. Endpoint Handler Pattern

Handlers are standalone `async fn` functions (not methods on a struct). They follow a consistent signature:
- Path parameters extracted via `axum::extract::Path<Id>` for single-resource endpoints
- Service injected via `State<Arc<AdvisoryService>>` from Axum application state
- Transaction context created and passed to the service call
- Return type is `Result<Json<T>, AppError>` for single-resource GET endpoints
- List endpoints return `Result<Json<PaginatedResults<T>>, AppError>`

### 4. Route Registration

Each module's `endpoints/mod.rs` builds routes using `Router::new().route("/path", get(handler))`. Sub-module endpoint files are declared with `mod` and their handler functions are wired into routes. The `server/main.rs` mounts all module routers, so adding routes within an existing module does not require changes to `main.rs`.

### 5. Response Model Struct Conventions

Response structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`. Fields use snake_case naming (which maps directly to JSON keys). Integer count fields use `i64` to match PostgreSQL `bigint` and SeaORM conventions. Doc comments on the struct and fields enable OpenAPI schema generation via utoipa.

### 6. Testing Conventions

Integration tests live in `tests/api/` with one file per domain area. Tests use a shared test harness that spins up a real PostgreSQL database. The pattern is: create test data, make an HTTP request to the running server, assert the status code (`StatusCode::OK`, `StatusCode::NOT_FOUND`), then parse and assert the response body via `.json::<T>()`.

### 7. Database Query Pattern

SeaORM entities are referenced via module paths (e.g., `entity::sbom_advisory`). Joins are performed via `.find_also_linked()` or manual `.join()` on entity relations. Aggregation is done either via SQL `COUNT`/`GROUP BY` or by collecting results and counting in Rust. Deduplication uses `SELECT DISTINCT` at the SQL level or `HashSet` in Rust.

### 8. Import Style

External crate imports come first, then internal crate imports, separated by a blank line. Intra-crate imports use `crate::` paths. Cross-module imports use fully qualified module paths.
