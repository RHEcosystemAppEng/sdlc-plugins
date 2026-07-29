# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Error handling
- All handlers and service methods in `modules/fundamental/` return `Result<T, AppError>` with `.context()` for error wrapping, matching the pattern defined in `common/src/error.rs`.
- 404 responses are returned when an entity is not found, consistent across all GET endpoints (e.g., `advisory/endpoints/get.rs`, `sbom/endpoints/get.rs`).

### Module structure
- Every domain module follows a strict `model/ + service/ + endpoints/` structure.
- Model submodules are registered in `model/mod.rs` via `pub mod <name>;` declarations.
- Endpoint submodules are registered in `endpoints/mod.rs` with route definitions.
- Service files contain the core business logic, while endpoint files handle HTTP extraction and delegation.

### Naming conventions
- Service methods follow a `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`). The new method `severity_summary` follows a `noun_noun` pattern to describe what it computes, which is acceptable as a query/aggregation method.
- Structs follow `PascalCase` with descriptive suffixes: `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `PaginatedResults`.
- Endpoint handler files are named after their HTTP action or resource (e.g., `get.rs`, `list.rs`).

### Endpoint registration
- Routes are registered in each module's `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining.
- `server/src/main.rs` mounts all modules automatically -- individual endpoint registration stays within the module.

### Parameter and option propagation
- Service methods accept `&self`, the entity identifier, and a `tx: &Transactional<'_>` for database transaction context.
- Endpoint handlers extract path parameters via Axum's `Path<Id>` extractor.
- Service instances are obtained from application state in handlers.

### Response types
- Single-entity endpoints return the model struct directly (Axum's `Json` extractor handles serialization).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new `SeveritySummary` endpoint returns a single aggregation struct, consistent with single-entity response patterns.

### Import organization
- Standard library imports first, then external crate imports, then internal crate imports.
- SeaORM entity imports for database operations.
- Common module imports for shared types (`AppError`, `PaginatedResults`, etc.).

### Derive macros
- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI spec generation.
- This pattern is consistent across `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`, and `PackageSummary`.

### Documentation
- Public structs and functions have `///` doc comments explaining their purpose.

## Test Conventions

### Assertion style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into the expected response type.
- Value-based assertions are used -- asserting on specific field values rather than just collection lengths.

### Response validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Single-entity endpoint tests validate the full response structure and key field values.

### Error cases
- All endpoint tests include a 404 test using `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs.

### Test naming
- Tests follow the `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_not_found`).

### Test organization
- Tests are organized in `tests/api/` by domain entity (one file per entity: `sbom.rs`, `advisory.rs`, `search.rs`).
- Each test file contains multiple test functions covering success and error paths.

### Test setup
- Integration tests use a real PostgreSQL test database.
- Test fixtures are created inline using helper functions or builder patterns.

### Parameterized tests
- No evidence of `#[rstest]` or other parameterized test frameworks in sibling test files. Individual test functions are used for each scenario. Following this existing convention, the new tests will use individual functions rather than introducing parameterized tests.

## CONVENTIONS.md Conventions

The repository contains a `CONVENTIONS.md` at the root. Its contents would be read during implementation to extract:
- CI check commands for Step 9 verification
- Code generation commands (if any)
- Any additional project-specific naming or structural rules beyond what sibling analysis reveals
