# Conventions Discovered from Sibling Analysis

## Project Structure Conventions

1. **Domain module pattern**: Each domain (sbom, advisory, package) follows a strict `model/ + service/ + endpoints/` three-layer structure. New functionality must add to these layers rather than creating parallel structures.

2. **One struct per file in model/**: Model structs like `SbomSummary`, `SbomDetails`, `AdvisorySummary`, `AdvisoryDetails`, `PackageSummary` each live in their own file under `model/`. The `SeveritySummary` struct should follow this convention with its own `severity_summary.rs` file.

3. **Module registration via mod.rs**: Each `model/`, `service/`, and `endpoints/` directory has a `mod.rs` that declares sub-modules with `pub mod`. New files must be registered here to be visible to the rest of the crate.

4. **Endpoint handler files**: Each endpoint has its own file (`get.rs`, `list.rs`) under `endpoints/`. The new severity summary endpoint should have its own `severity_summary.rs` file under `endpoints/`.

## API Conventions

5. **Route registration pattern**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining. The `server/main.rs` mounts all module routers automatically.

6. **API versioning**: All endpoints use the `/api/v2/` prefix consistently.

7. **Path parameter extraction**: SBOM and advisory IDs are extracted via Axum's `Path<T>` extractor, following the pattern in `get.rs` handlers. Path parameter syntax depends on the Axum version (`{id}` for 0.7+, `:id` for older).

8. **Response types**: Single-entity endpoints return `Json<T>` directly. List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. The severity summary endpoint is a single-entity response, so it should use `Json<SeveritySummary>`.

## Service Layer Conventions

9. **Service method signature**: Service methods follow the pattern `async fn method(&self, id: &str, tx: &Transactional<'_>) -> Result<T, AppError>`. The `Transactional` parameter enables shared transaction context across method calls.

10. **Database access**: Services use `self.db.connection(tx)` to get a transaction-aware database connection, consistent across all service methods.

11. **Entity queries**: SeaORM patterns are used consistently: `Entity::find()`, `Entity::find_by_id()`, `.filter()`, `.all()`, `.one()` for database queries.

12. **Naming convention**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). The new method `severity_summary` follows this as a compound noun describing the computed result.

## Error Handling Conventions

13. **AppError return type**: All handler return types use `Result<T, AppError>` from `common/src/error.rs`. `AppError` implements Axum's `IntoResponse` trait for automatic HTTP error responses.

14. **Context wrapping**: Fallible operations use `.context("description")` (from anyhow) to wrap errors with descriptive messages before they become `AppError`. Every `await?` should have a `.context()` call.

15. **404 pattern**: When an entity is not found, return `AppError::NotFound(message)`. This is consistent across all `fetch`-style service methods. The severity summary endpoint should return 404 when the SBOM does not exist, matching existing SBOM endpoint behavior.

## Data Model Conventions

16. **Join tables**: Relationships between entities (e.g., SBOM-to-advisory) use dedicated join table entities like `sbom_advisory`, defined in `entity/src/` and queried via SeaORM. The severity summary uses the `sbom_advisory` join table to find advisories linked to an SBOM.

17. **Severity field**: The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` has a `severity` field that maps to the underlying entity field in `entity/src/advisory.rs`.

## Derive Macro Conventions

18. **Standard derives for response models**: Response structs derive `Clone, Debug, Serialize, Deserialize, ToSchema`. The `ToSchema` derive is from `utoipa` for OpenAPI documentation generation. The `SeveritySummary` struct should also derive `Default` so all counts start at 0.

19. **OpenAPI annotations**: Endpoint handlers use `#[utoipa::path(...)]` attribute macros for API documentation generation, including path, params, and responses specifications.

## Testing Conventions

20. **Integration test location**: Tests live in `tests/api/` with one file per domain area (e.g., `sbom.rs`, `advisory.rs`, `search.rs`). The new tests should live in `tests/api/advisory_summary.rs`.

21. **Async test framework**: Tests use `#[tokio::test]` for async execution.

22. **Status code assertions**: Tests assert response status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern, followed by body deserialization and field-level assertions.

23. **Real database**: Integration tests hit a real PostgreSQL test database rather than mocking, ensuring end-to-end correctness.

24. **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

25. **Error case coverage**: All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, ensuring error paths are verified.

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at its root. Its conventions (framework choices, module patterns, error handling, response types, query helpers, testing, caching) are consistent with the sibling analysis above and have been incorporated into this document.
