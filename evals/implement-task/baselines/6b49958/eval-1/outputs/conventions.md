# Conventions Discovered from Sibling Analysis

## Module Structure Pattern

The `modules/fundamental/src/` directory follows a strict **model / service / endpoints** tri-layer architecture for each domain entity:

```
<domain>/
  model/
    mod.rs          # Re-exports all model types
    summary.rs      # Lightweight summary struct (used in list responses)
    details.rs      # Full detail struct (used in get-by-id responses)
  service/
    mod.rs          # Re-exports; may contain shared helpers
    <domain>.rs     # Primary service struct with business-logic methods
  endpoints/
    mod.rs          # Route registration (Router::new().route(...))
    list.rs         # GET collection handler
    get.rs          # GET single-item handler
```

Evidence: both `advisory/` and `package/` follow this exact layout. New functionality should add files within the existing layer directories rather than introducing new top-level directories.

## Error Handling

- All fallible functions return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Contextual errors are wrapped using `.context("description of what failed")`, consistent with the `anyhow`-style pattern.
- 404 responses are produced by returning an `AppError` not-found variant when a lookup yields `None`, matching the pattern used by existing SBOM and advisory endpoints.

## Service Method Signatures

From `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`:

- Methods take `&self` as receiver.
- An entity identifier parameter (e.g., `id: Id`).
- A `tx: &Transactional<'_>` parameter for database transaction context.
- Methods are `async` and return `Result<T, AppError>`.

Example inferred signature pattern:
```rust
pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<Option<AdvisoryDetails>, AppError>
pub async fn list(&self, query: Query, paginated: Paginated, tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, AppError>
```

## Endpoint Handler Patterns

From `advisory/endpoints/get.rs` and sibling handlers:

- Path parameters extracted via Axum's `Path<Id>` extractor.
- Service injected via Axum state or extension (e.g., `State<AppState>` or `Extension<AdvisoryService>`).
- Transaction context obtained from request extensions.
- Handler returns `Result<Json<T>, AppError>` where `T` is the response struct.
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler_fn))`.

## Model / Serialization Conventions

- Response structs derive `Serialize` (and often `Deserialize`) via `serde`.
- Structs also derive `Debug`, `Clone`, and commonly `utoipa::ToSchema` for OpenAPI spec generation.
- Field naming follows `snake_case` in Rust, with serde defaulting to the same for JSON serialization (no `#[serde(rename_all)]` override observed from structure).

## Entity / Join Table Conventions

- Entity modules live in `entity/src/` (e.g., `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`).
- Join tables follow the `<left>_<right>.rs` naming convention (e.g., `sbom_advisory.rs` joins SBOMs to advisories).
- ORM usage is SeaORM-based (common in Trustify), with entity structs implementing `EntityTrait`.

## Test Conventions

- Integration tests live in `tests/api/` at the workspace root.
- Test files are named after the domain they exercise (e.g., `advisory.rs`, `sbom.rs`).
- Tests use a shared test harness for standing up a test database and HTTP client.
- Assertions validate both HTTP status codes and JSON response body structure.

## Route Path Conventions

- API routes are versioned under `/api/v2/`.
- Resource-centric paths: `/api/v2/<resource>` for collections, `/api/v2/<resource>/{id}` for single items.
- Sub-resource paths nest under the parent: `/api/v2/sbom/{id}/advisory-summary`.

## Re-export Conventions

- Each `mod.rs` file re-exports child modules with `pub mod <name>;`.
- Adding a new model file requires a corresponding `pub mod` entry in the parent `model/mod.rs`.
