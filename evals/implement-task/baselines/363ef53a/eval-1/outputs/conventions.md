# Conventions Discovered from Sibling Analysis

Conventions identified by analyzing sibling files in the trustify-backend repository, organized by category. These serve as binding reference during implementation.

## Module Structure

- **Domain module pattern:** Each domain module (sbom, advisory, package) follows a consistent `model/ + service/ + endpoints/` tri-directory structure. New domain features must add files within this structure rather than introducing alternative layouts.
- **Module registration:** Sub-modules are registered in their parent `mod.rs` with `pub mod <name>;` declarations. Both `model/mod.rs` and `endpoints/mod.rs` follow this pattern (e.g., `pub mod summary;`, `pub mod details;`).

## Error Handling

- **Return type convention:** All service methods and endpoint handlers return `Result<T, AppError>` where `AppError` is the shared error enum from `common/src/error.rs`.
- **Error wrapping with `.context()`:** Errors are wrapped with `.context("descriptive message")` using anyhow-style context chaining. This provides stack-trace-like error messages in API responses. Example: `.context("failed to fetch advisory severity summary")`
- **`AppError` implements `IntoResponse`:** The `AppError` enum in `common/src/error.rs` implements Axum's `IntoResponse` trait, allowing handlers to return `Result<Json<T>, AppError>` directly.

## Endpoint Patterns

- **Path parameter extraction:** Endpoint handlers use Axum's `Path<Id>` extractor to parse path parameters (e.g., SBOM ID from `/api/v2/sbom/{id}/advisory-summary`). Seen in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`.
- **Service invocation pattern:** Handlers call service methods with the pattern `service.method_name(id, &tx).await?` where `tx` is a `Transactional` reference for database operations.
- **JSON response:** Handlers return the response struct directly; Axum's `Json` extractor handles serialization. Pattern: `Ok(Json(result))`.
- **Route registration:** Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`. Each module's router is then mounted by the server.

## Service Method Patterns

- **Method signature convention:** Service methods follow the pattern `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`. The `AdvisoryService` has `fetch` and `list` methods following this pattern.
- **Query building:** Services use SeaORM for database queries, leveraging the entity definitions in `entity/src/`.

## Model/Struct Patterns

- **Derive macros:** Model structs use `#[derive(Debug, Clone, Serialize, Deserialize)]` for JSON serialization compatibility with Axum.
- **Serde integration:** Response structs derive `serde::Serialize` for automatic JSON serialization when returned via `Json<T>`.
- **Field naming:** Struct fields use snake_case, matching Rust conventions. Serde renames to camelCase or keeps snake_case depending on project convention (inspect `AdvisorySummary` for confirmation).

## Naming Conventions

- **Function names:** `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`).
- **File names:** Snake_case matching the primary type or concept (e.g., `summary.rs` for `SbomSummary`, `advisory.rs` for `AdvisoryService`).
- **Endpoint handler files:** Named after the HTTP verb or action (e.g., `get.rs`, `list.rs`).

## Test Patterns

- **Test location:** Integration tests reside in `tests/api/` with one file per domain area (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code verification and `assert_eq!` on deserialized response fields for value verification.
- **Test database:** Integration tests hit a real PostgreSQL test database (not mocked).
- **Response validation:** Tests deserialize the response body and assert on specific field values, not just collection lengths.

## Database Patterns

- **Join tables:** Entity relationships are modeled with explicit join table entities (e.g., `sbom_advisory.rs` for the SBOM-Advisory relationship).
- **SeaORM entities:** Each database table has a corresponding entity file in `entity/src/` with SeaORM derive macros.

## Response Type Conventions

- **List endpoints:** Return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Single-item endpoints:** Return the model struct directly wrapped in `Json<T>`.
- **Aggregation endpoints (new):** Should return a purpose-built summary struct (e.g., `SeveritySummary`) rather than reusing an existing paginated wrapper, since the response is a fixed-shape aggregation rather than a collection.
