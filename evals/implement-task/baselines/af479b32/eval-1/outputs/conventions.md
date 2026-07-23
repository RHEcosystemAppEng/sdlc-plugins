# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` directory structure
- Module registration is done via `mod.rs` files with `pub mod <submodule>;` declarations
- Each domain (sbom, advisory, package) follows identical organizational patterns

### Framework & Libraries
- **HTTP framework:** Axum — routes registered via `Router::new().route("/path", get(handler))`
- **ORM:** SeaORM for database entity definitions and queries
- **Caching:** `tower-http` caching middleware configured in endpoint route builders

### Endpoint Patterns
- Handlers extract path parameters via `Path<Id>` (Axum extractor)
- All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation
- Response serialization uses Axum's `Json` extractor — return the struct directly
- Route registration in each module's `endpoints/mod.rs` using `Router::new().route(...)` chaining
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Service Patterns
- Service structs follow `<Domain>Service` naming (e.g., `SbomService`, `AdvisoryService`)
- Service methods take `&self` as the first parameter
- Database transaction parameter: `tx: &Transactional<'_>` as the last parameter
- Method naming follows `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- New service methods follow the same signature pattern as existing methods in the same service

### Model Patterns
- Model structs use `#[derive(Serialize, Deserialize)]` for JSON serialization
- Structs named `<Domain>Summary` for list/summary views, `<Domain>Details` for full views
- Each model type gets its own file within the `model/` directory
- Models registered via `pub mod <name>;` in `model/mod.rs`

### Error Handling
- `AppError` enum defined in `common/src/error.rs`, implements `IntoResponse`
- Errors wrapped with `.context("descriptive message")` (anyhow-style)
- 404 responses for missing resources, consistent with existing SBOM/advisory endpoints

### Query Helpers
- Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- Connection pool limiting via `common/src/db/limiter.rs`

### Naming Conventions
- Files: snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- Types: PascalCase (e.g., `SeveritySummary`, `AdvisoryService`)
- Functions/methods: snake_case (e.g., `severity_summary`, `fetch`, `list`)
- API paths: kebab-case (e.g., `/api/v2/sbom/{id}/advisory-summary`)

### API Design
- REST API paths prefixed with `/api/v2/`
- Resource-centric URL design
- Path parameters for resource identification (e.g., `{id}`)

## Test Conventions

### Test Structure
- Integration tests located in `tests/api/` directory
- Tests hit a real PostgreSQL test database (not mocks)
- Test files named after the domain they test (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

### Assertion Patterns
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Body deserialization after status check
- 404 tests for non-existent resources: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`)

### Test Organization
- One test file per domain area in `tests/api/`
- Tests grouped by success/failure scenarios within each file
- Each test is self-contained with its own setup
