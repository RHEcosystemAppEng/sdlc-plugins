# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Error Handling
- All service methods and endpoint handlers use `Result<T, AppError>` as the return type, where `AppError` is the error enum defined in `common/src/error.rs`.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` crate (re-exported through AppError) to add context to errors as they propagate up the call stack.
- Endpoint handlers return `AppError` directly, which implements `IntoResponse` for Axum, translating error variants into appropriate HTTP status codes (e.g., 404 for not found).
- Example pattern: `service.fetch(id, &tx).await.context("failed to fetch advisory")?`

### Module Structure (model/service/endpoints)
- Each domain module (e.g., `advisory`, `sbom`, `package`) in `modules/fundamental/src/` follows a consistent three-layer structure:
  - **`model/`** -- Data structs (response types, summaries, details) with `Serialize`/`Deserialize` derives. Each logical model gets its own file, registered via `pub mod <name>;` in `model/mod.rs`.
  - **`service/`** -- Business logic layer. Service structs (e.g., `AdvisoryService`) contain methods like `fetch`, `list`, and domain-specific operations. Methods take `&self`, domain-specific parameters, and a `tx: &Transactional<'_>` for database access.
  - **`endpoints/`** -- HTTP route handlers. Each endpoint gets its own file. Handlers extract path parameters via Axum's `Path<Id>`, call service methods, and return `Json<T>` responses. Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.

### Endpoint Handler Pattern
- Handlers follow a consistent structure: extract path parameters via `Path<Id>`, obtain a service instance, call the service method with the extracted ID and a transaction reference, and return the result as JSON.
- Route registration follows the pattern in `endpoints/mod.rs`: `Router::new().route("/path", get(handler_fn))`.
- The `get.rs` file in advisory/endpoints/ is the primary reference for this pattern.

### Service Method Signatures
- Service methods on `AdvisoryService` follow a consistent signature: `async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.
- Database queries use the SeaORM entities defined in `entity/src/` (e.g., `sbom_advisory.rs` for the join table between SBOMs and advisories).
- The `fetch` and `list` methods in `advisory/service/advisory.rs` serve as the primary reference for adding new methods.

### Naming Conventions
- Service methods use `verb_noun` naming (e.g., `fetch`, `list`, `severity_summary`).
- Model structs use PascalCase descriptive names (e.g., `AdvisorySummary`, `SeveritySummary`).
- Endpoint handler functions use snake_case (e.g., `get_advisory`, `list_advisories`).
- File names match the feature they implement (e.g., `summary.rs` for the Summary model, `get.rs` for the GET handler).

### Struct Definitions
- Response structs in model files use `#[derive(Serialize, Deserialize, Debug)]` (and potentially `Clone`, `PartialEq`).
- The `AdvisorySummary` struct in `model/summary.rs` has a `severity` field that represents the advisory's severity level -- this is used for counting by severity level.

## Test Conventions

### Assertion Style
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization into the expected response struct.
- Response validation checks specific field values, not just counts or lengths.

### Error Case Coverage
- All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent resource IDs.

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` naming convention (e.g., `test_advisory_summary_valid`, `test_advisory_summary_not_found`).

### Test Documentation
- Every test function will include a doc comment (`///`) explaining what it verifies (enforced by implement-task Step 7, regardless of sibling patterns).
- Non-trivial tests include given-when-then inline comments (`// Given`, `// When`, `// Then`).

### Test Setup
- Integration tests in `tests/api/` set up test fixtures (SBOMs, advisories) and make HTTP requests against the test server.
