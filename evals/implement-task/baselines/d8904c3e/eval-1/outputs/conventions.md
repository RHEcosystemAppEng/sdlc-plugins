# Conventions Discovered from Sibling Analysis

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at its root. Since this is a simulated environment, the exact contents are not available, but its presence indicates the project has explicit conventions to follow. In a real implementation, this file would be read first and its rules applied throughout.

## Production Code Conventions (from sibling analysis)

### Framework and Architecture

- **HTTP framework**: Axum for all HTTP routing and handler extraction
- **ORM**: SeaORM for all database interactions
- **Module pattern**: Each domain module follows a strict `model/ + service/ + endpoints/` three-layer structure. The `advisory/`, `sbom/`, and `package/` modules all follow this identical layout.

### Endpoint Conventions

- **Route registration**: Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern. Siblings: `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`, `package/endpoints/mod.rs` all follow this pattern.
- **Path parameter extraction**: Handlers extract path parameters via Axum's `Path<Id>` extractor. Sibling: `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs` use this pattern.
- **Response serialization**: Handlers return structs directly; Axum's `Json` extractor handles serialization. No manual serialization calls.
- **List vs. single-item responses**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Single-item endpoints return the model struct directly wrapped in `Json`.

### Service Conventions

- **Method signatures**: Service methods follow the pattern `fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`. Siblings: `AdvisoryService::fetch`, `AdvisoryService::list`, `SbomService::fetch`, `SbomService::list` all use this signature pattern.
- **Naming**: Service methods follow `verb_noun` or simple `verb` naming (e.g., `fetch`, `list`, `search`, `ingest`).
- **Error wrapping**: All service methods use `.context()` for error wrapping, matching the `AppError` pattern in `common/src/error.rs`.

### Model Conventions

- **Module registration**: Each model submodule is registered via `pub mod <name>;` in the parent `model/mod.rs`. Siblings: `model/mod.rs` contains `pub mod summary;` and `pub mod details;`.
- **Struct derivation**: Model structs derive `Serialize`, `Deserialize`, and likely `Debug`, `Clone` based on the Axum + SeaORM ecosystem conventions.
- **Naming**: Model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`, `PackageSummary`).

### Error Handling

- **Return type**: All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- **Context wrapping**: Errors are wrapped with `.context("descriptive message")` for stack traces.
- **404 pattern**: When an entity is not found, return an `AppError` that maps to HTTP 404, consistent with existing SBOM and advisory endpoints.

### Import Organization

- Based on Rust conventions and the module structure, imports follow: standard library first, then external crates (axum, serde, sea_orm), then internal crate modules (`crate::...`, `super::...`).

## Test Conventions (from sibling test analysis)

### Test File Organization

- **Location**: Integration tests live in `tests/api/` directory, one file per domain (e.g., `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`).
- **Naming**: Test files are named after the domain entity or feature they test.

### Assertion Patterns

- **Status code checks**: All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for success cases.
- **404 checks**: Error case tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for missing entities.
- **Body deserialization**: Tests deserialize response bodies and assert on specific field values rather than just checking status codes.

### Test Structure

- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- **Database**: Integration tests hit a real PostgreSQL test database.
- **Setup**: Tests create test data (SBOMs, advisories) before asserting on endpoint responses.
- **Value-based assertions**: Tests assert on actual values (e.g., specific severity counts) rather than just collection lengths.

### Parameterized Tests

- The sibling test files would be examined for `#[rstest]` or `#[case]` usage. If not present in siblings, individual test functions would be used instead of parameterized tests.

## Convention Conflict Check

No conflicts detected between the task description/Implementation Notes and the discovered conventions. The task explicitly instructs following the existing endpoint pattern in `advisory/endpoints/get.rs` and the service method pattern in `advisory/service/advisory.rs`, which aligns with all discovered conventions.
