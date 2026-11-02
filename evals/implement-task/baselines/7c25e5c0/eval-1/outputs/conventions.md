# Conventions Discovered from Sibling Analysis

## Error Handling

- All service methods and handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context("description")` from the `anyhow` pattern, matching the pattern in `common/src/error.rs`
- 404 errors use `AppError::NotFound` or `.ok_or_else(|| ...)` with `.context()` wrapping
- Errors propagate via `?` operator — no manual error matching in handlers

## Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` structure
- `model/mod.rs` re-exports submodules via `pub mod <name>;`
- `service/mod.rs` contains the primary service struct (e.g., `AdvisoryService`)
- `endpoints/mod.rs` registers routes and declares handler submodules

## Naming Conventions

- Service methods: `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Handler functions: short verb names (e.g., `get`, `list`)
- Structs: PascalCase descriptive names (e.g., `AdvisorySummary`, `SeveritySummary`)
- Test functions: `test_<feature>_<scenario>` pattern
- Files: lowercase with underscores matching the struct or handler name

## Service Method Signatures

- Methods take `&self, id: Id, tx: &Transactional<'_>` and return `Result<T, AppError>`
- Database access via `self.db(tx)` pattern
- Existing methods: `fetch`, `list`, `search` in `AdvisoryService`

## Endpoint Patterns

- Path params via `Path<Id>` extractor (Axum)
- Service injected via `State(service): State<AdvisoryService>`
- Response: return `Json<T>` directly; Axum handles serialization
- Route registration: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- OpenAPI docs via `utoipa::path` attributes on handler functions

## Model Patterns

- Derive macros: `Clone, Debug, Serialize, Deserialize, ToSchema`
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the struct directly wrapped in `Json`

## Test Patterns

- Integration tests in `tests/api/` directory
- Use `test_context` and `TrustifyContext` for database setup/teardown
- Async tests with `#[tokio::test]`
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` then deserialize body
- Hit a real PostgreSQL test database (not mocked)

## Import Organization

- External crates first, then internal modules
- Grouped by: framework imports, common imports, domain-specific imports
