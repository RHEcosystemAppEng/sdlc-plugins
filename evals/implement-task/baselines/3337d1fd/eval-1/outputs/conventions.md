# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Module Structure
- Each domain module follows a strict `model/ + service/ + endpoints/` directory structure.
- Each sub-directory has a `mod.rs` that re-exports public types and registers sub-modules (e.g., `pub mod summary;`, `pub mod details;`).
- New model types get their own file under `model/` and are registered via `pub mod <name>;` in `model/mod.rs`.

### Naming Conventions
- **Model structs**: PascalCase noun describing the entity and its role (e.g., `AdvisorySummary`, `SbomDetails`, `PackageSummary`).
- **Service methods**: `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`). The new method should follow this pattern: `severity_summary`.
- **Endpoint files**: named after the HTTP operation or resource concept (e.g., `get.rs`, `list.rs`). The new endpoint file should be `severity_summary.rs`.
- **Test files**: named after the domain resource being tested (e.g., `sbom.rs`, `advisory.rs`, `search.rs`). The new test file should be `advisory_summary.rs`.

### Error Handling
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`.
- Errors are wrapped with `.context()` for descriptive error messages propagated to the caller.

### Endpoint Registration
- Each module's `endpoints/mod.rs` registers routes using Axum's `Router::new().route("/path", get(handler))` pattern.
- `server/main.rs` mounts all modules but does not need modification when adding routes within an existing module (auto-mount via module registration).

### Response Types
- Single-entity endpoints return the struct directly (Axum's `Json` extractor handles serialization).
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new summary endpoint returns a single aggregate struct, not a paginated list.

### Service Method Signatures
- Service methods take `&self` as the receiver.
- Methods that access the database take `sbom_id: Id` (or equivalent entity ID) and `tx: &Transactional<'_>` as parameters.
- This matches the existing `fetch` and `list` methods on `AdvisoryService`.

### Import Organization
- Framework imports (Axum, SeaORM) come first, followed by crate-level imports (`common`, `entity`), then local module imports.

### Database Access
- Uses SeaORM for database operations.
- Join tables (e.g., `sbom_advisory`) are used to traverse relationships between entities.
- Queries should use the shared query builder helpers from `common/src/db/query.rs` when applicable.

## Test Conventions

### Assertion Style
- All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into the expected response struct.
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` or equivalent status codes.

### Response Validation
- Tests validate specific field values, not just counts or lengths.
- For aggregate responses, each field should be asserted individually.

### Error Cases
- Every endpoint test file includes at least one test for 404 (not found) scenarios.
- Error responses match the `AppError` format from `common/src/error.rs`.

### Test Naming
- Tests follow the `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).
- The new tests should follow: `test_advisory_summary_<scenario>`.

### Test Setup
- Integration tests hit a real PostgreSQL test database.
- Test fixtures create the necessary entities (SBOMs, advisories, links) before exercising the endpoint.

### Test Documentation
- Every test function must have a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments inside the test body.

### Parameterized Tests
- Sibling tests in `tests/api/` do not appear to use parameterized test frameworks (`rstest`); individual test functions are used for each scenario. Follow this pattern.
