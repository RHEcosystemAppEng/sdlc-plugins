# Convention Conformance Analysis for TC-9201

Conventions discovered from analyzing sibling files in the trustify-backend repository.

## Error Handling

- All service methods and endpoint handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("descriptive message")` from the `anyhow` pattern, matching the established pattern throughout the codebase
- 404 errors are returned when entities are not found, consistent with existing SBOM and advisory endpoints

## Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` three-tier structure
- Models contain data structs (e.g., `summary.rs`, `details.rs`), services contain business logic, endpoints contain HTTP handlers
- Model submodules are registered in `model/mod.rs` with `pub mod <name>;`
- Service files follow the pattern of methods on a service struct taking `&self, id: Id, tx: &Transactional<'_>` parameters

## Endpoint Patterns

- Endpoint handlers extract path parameters via Axum's `Path<Id>` extractor
- Handlers call service methods and return the result directly (Axum's `Json` extractor handles serialization)
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Naming Conventions

- Function names follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Model struct names use PascalCase descriptive names (e.g., `AdvisorySummary`, `SbomDetails`)
- File names use snake_case matching the primary struct or function they contain

## Testing Conventions

- Integration tests are located in `tests/api/` and hit a real PostgreSQL test database
- Test assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Tests follow the pattern of setting up test data, making HTTP requests, and asserting on responses
- Test file names match the feature being tested (e.g., `advisory.rs` for advisory endpoint tests)

## Import Organization

- External crate imports first, then internal module imports
- `use` statements grouped by crate

## Database Query Patterns

- SeaORM is used for database access
- Join tables (e.g., `sbom_advisory`) are used for many-to-many relationships
- Shared query builder helpers (filtering, pagination, sorting) are in `common/src/db/query.rs`

## Response Types

- Single-entity endpoints return the entity struct directly (serialized as JSON)
- List endpoints return `PaginatedResults<T>` for paginated responses
- New summary/aggregation endpoints return custom response structs with `#[derive(Serialize)]`
