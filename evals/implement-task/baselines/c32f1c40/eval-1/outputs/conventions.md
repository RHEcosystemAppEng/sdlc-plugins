# Conventions Discovered from Sibling Analysis

## Source

Sibling analysis was performed on the `trustify-backend` repository structure
documented in `repo-backend.md`, focusing on the `modules/fundamental/src/advisory/`
module and its peers (`sbom/`, `package/`).

## Naming Conventions

- **Files**: lowercase snake_case (e.g., `summary.rs`, `details.rs`, `get.rs`, `list.rs`)
- **Functions/methods**: `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`)
- **Structs**: PascalCase with domain prefix (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`)
- **Test files**: named after the domain entity (e.g., `tests/api/advisory.rs`, `tests/api/sbom.rs`)
- **Modules**: each domain entity has its own directory with `mod.rs` (e.g., `advisory/mod.rs`)

## Module Structure

- Every domain module follows the `model/ + service/ + endpoints/` tri-partition
- `model/mod.rs` re-exports sub-modules (e.g., `pub mod summary;`, `pub mod details;`)
- `service/mod.rs` or `service/<entity>.rs` contains the service struct with business logic
- `endpoints/mod.rs` registers routes; individual handler files per endpoint (e.g., `get.rs`, `list.rs`)

## Error Handling

- All endpoint handlers return `Result<T, AppError>`
- Errors wrapped with `.context()` for descriptive messages
- `AppError` enum defined in `common/src/error.rs` and implements `IntoResponse`

## Endpoint Patterns

- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`
- Path parameters extracted via `Path<Id>` (Axum extractor)
- Service called with `(&self, id: Id, tx: &Transactional<'_>)` signature pattern
- Response serialization via Axum's `Json` extractor (return struct directly)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the entity struct wrapped in `Json`

## API Design

- Base path: `/api/v2/<entity>`
- GET for retrieval, path params for IDs (e.g., `/api/v2/sbom/{id}`)
- Shared query helpers for filtering, pagination, sorting from `common/src/db/query.rs`

## Database Patterns

- SeaORM for database access
- Entity definitions in `entity/src/` (e.g., `advisory.rs`, `sbom.rs`)
- Join tables as separate entities (e.g., `sbom_advisory.rs`, `sbom_package.rs`)
- Transactional context passed as `&Transactional<'_>`

## Test Patterns

- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Tests organized by domain entity (one file per entity)
- No parameterized test patterns observed in sibling test files

## Import Organization

- Standard library imports first, then external crates, then internal modules (Rust convention)
- Re-exports via `mod.rs` files

## Caching

- `tower-http` caching middleware used at route level
- Cache configuration in endpoint route builders

## Skill Guidance Overrides

- **Test documentation**: All test functions will include `///` doc comments per skill guidance, even though sibling tests may lack them
- **Value-based assertions**: Tests will assert on specific values (severity counts), not just collection lengths, per skill guidance
- **Given-when-then comments**: Non-trivial tests will include `// Given`, `// When`, `// Then` section comments per skill guidance
