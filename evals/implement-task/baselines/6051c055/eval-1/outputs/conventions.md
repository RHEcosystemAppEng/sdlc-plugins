# Conventions Discovered from Sibling Analysis

## Endpoint Conventions (from advisory/endpoints/get.rs and sibling endpoint files)

1. **Handler signature pattern**: `async fn handler_name(Path(param): Path<Type>, State(state): State<AppState>) -> Result<Json<ResponseType>, AppError>`
2. **State extraction**: Application state is accessed via Axum's `State` extractor; services are obtained from the state (e.g., `state.advisory_service()`)
3. **Route registration**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(module::handler))` — each endpoint lives in its own submodule
4. **Module declaration**: Each endpoint file is declared as `mod endpoint_name;` in `endpoints/mod.rs`
5. **JSON response**: Handlers return the response struct directly wrapped in `Json()` — Axum handles serialization
6. **404 pattern**: Service methods return `Option<T>`; handlers map `None` to `AppError::NotFound` using `.ok_or_else(|| AppError::NotFound("descriptive message".into()))?`

## Service Conventions (from advisory/service/advisory.rs)

1. **Method signature**: Methods on the service struct take `&self`, domain-specific parameters, and a database connection reference (`&ConnectionOrTransaction`)
2. **Return type**: `Result<T, AppError>` for guaranteed-result operations; `Result<Option<T>, AppError>` for lookup-by-ID operations
3. **Error wrapping**: Errors are wrapped with `.context("human-readable description")` before propagating — this adds context to the anyhow error chain
4. **Query pattern**: SeaORM `Entity::find()` with `.filter()` and `.join()` builders, executed with `.all(db)` or `.one(db)`
5. **Deduplication**: When aggregating across join tables, use `.distinct()` on the query or deduplicate in application code with a `HashSet`

## Model Conventions (from advisory/model/summary.rs and sibling models)

1. **Derive macros**: All response models derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema` (for OpenAPI documentation)
2. **Module registration**: Each model file is registered as `pub mod model_name;` in `model/mod.rs`
3. **Field types**: Counts use unsigned integers (`u32` or `i64` depending on the database column type); IDs use `Uuid`
4. **Naming**: Model structs use PascalCase matching the domain concept (e.g., `AdvisorySummary`, `SeveritySummary`)

## Error Handling Conventions (from common/src/error.rs)

1. **AppError variants**: `NotFound(String)`, `BadRequest(String)`, `Internal(anyhow::Error)` — each maps to a specific HTTP status code
2. **Automatic conversion**: `impl From<anyhow::Error> for AppError` enables the `?` operator for anyhow-compatible errors
3. **Context pattern**: Use `.context("message")?` to wrap lower-level errors with descriptive context before they convert to `AppError::Internal`

## Test Conventions (from tests/api/ directory)

1. **Test file naming**: `tests/api/{feature_name}.rs` — one file per feature or endpoint group
2. **Test function naming**: `test_{feature}_{scenario}` in snake_case (e.g., `test_advisory_summary_not_found`)
3. **Test setup**: Each test uses a shared test harness that provisions a real PostgreSQL database, seeds data via service methods or direct entity insertion
4. **HTTP assertions**: Tests make HTTP requests via the test client, assert status codes, then deserialize and assert response body fields
5. **Test attribute**: `#[tokio::test]` for async tests
6. **Registration**: Test files are added to `tests/api/mod.rs` (or the test binary root) as `mod advisory_summary;`

## Commit Message Convention

- Follows Conventional Commits: `type(scope): description`
- Types: `feat` for new features, `fix` for bug fixes, `refactor`, `test`, `docs`
- Scope matches the module name (e.g., `advisory`)
- Jira ticket reference in footer: `Refs: TC-XXXX`
- Trailer: `--trailer='Assisted-by: Claude Code'`
