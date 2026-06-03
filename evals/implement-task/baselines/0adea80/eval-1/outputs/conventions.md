# Conventions Discovered from Sibling Analysis

## Project Structure Conventions

1. **Domain module pattern**: Each domain (sbom, advisory, package) follows a strict `model/ + service/ + endpoints/` three-layer structure. New functionality should add to these layers rather than creating parallel structures.

2. **One struct per file in model/**: Model structs like `SbomSummary`, `AdvisorySummary`, `SbomDetails`, `AdvisoryDetails` each live in their own file under `model/`. New model structs should follow this convention rather than being added to existing files.

3. **Module registration via mod.rs**: Each `model/`, `service/`, and `endpoints/` directory has a `mod.rs` that declares sub-modules with `pub mod`. New files must be registered here to be visible.

4. **Endpoint handler files**: Each endpoint has its own file (`get.rs`, `list.rs`) under `endpoints/`. New endpoints should follow this pattern.

## API Conventions

5. **Route registration pattern**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining. The `server/main.rs` mounts all module routers.

6. **API versioning**: All endpoints use the `/api/v2/` prefix.

7. **Path parameters**: SBOM and advisory IDs are extracted via Axum's `Path<T>` extractor. Path parameter syntax follows the Axum version in use (`:id` for older, `{id}` for 0.7+).

8. **Response types**: Single-entity endpoints return `Json<T>` directly. List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

## Service Layer Conventions

9. **Service method signature**: Service methods follow the pattern `async fn method(&self, id: &str, tx: &Transactional<'_>) -> Result<T, AppError>`. The `Transactional` parameter enables shared transaction context.

10. **Database access**: Services use `self.db.connection(tx)` to get a transaction-aware database connection.

11. **Entity queries**: SeaORM patterns are used consistently: `Entity::find()`, `Entity::find_by_id()`, `.filter()`, `.all()`, `.one()`.

## Error Handling Conventions

12. **AppError**: All handler return types use `Result<T, AppError>` from `common/src/error.rs`. `AppError` implements `IntoResponse` for Axum.

13. **Context wrapping**: Fallible operations use `.context("description")` (from anyhow) to wrap errors with descriptive messages before they become `AppError`.

14. **404 pattern**: When an entity is not found, return `AppError::NotFound(message)`. This is consistent across all `fetch`-style service methods.

## Data Model Conventions

15. **Join tables**: Relationships between entities (e.g., SBOM-to-advisory) use dedicated join table entities like `sbom_advisory`. These are defined in `entity/src/` and queried via SeaORM.

16. **Severity field**: The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` has a `severity` field. The underlying entity in `entity/src/advisory.rs` stores this value.

## Testing Conventions

17. **Integration test location**: Tests live in `tests/api/` with one file per domain area.

18. **Async test framework**: Tests use `#[tokio::test]` for async execution.

19. **Status code assertions**: Tests assert response status codes using `assert_eq!(resp.status(), StatusCode::OK)` pattern.

20. **Real database**: Integration tests hit a real PostgreSQL test database rather than mocking.

## Derive Macro Conventions

21. **Standard derives for models**: Response structs derive `Clone, Debug, Serialize, Deserialize, ToSchema`. The `ToSchema` derive is from `utoipa` for OpenAPI documentation.

22. **OpenAPI annotations**: Endpoint handlers use `#[utoipa::path(...)]` attribute macros for API documentation generation.
