# Conventions Discovered from Sibling Analysis

## Source Files Analyzed

Sibling analysis performed on the `advisory` module and its peers (`sbom`, `package`) in `modules/fundamental/src/`.

### Model Conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)

- **Naming**: Model structs use `PascalCase` with descriptive suffixes: `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`
- **Derives**: All model structs derive `Clone, Debug, Serialize, Deserialize` (serde for JSON serialization via Axum)
- **Module registration**: Each model sub-module is declared in `model/mod.rs` with `pub mod <name>;`
- **Field types**: Use Rust standard types (`i64`, `String`, `Option<T>`) and domain types; no raw database types in public models

### Service Conventions (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)

- **Naming**: Service structs use `PascalCase` + `Service` suffix: `AdvisoryService`, `SbomService`
- **Method signatures**: Methods take `&self, <params>, tx: &Transactional<'_>` — all database operations go through the transactional context
- **Error handling**: Methods return `Result<T, AppError>` with `.context("description")` wrapping via anyhow-style error enrichment
- **Query pattern**: Use SeaORM entity queries with joins; shared query helpers from `common/src/db/query.rs` for filtering and pagination

### Endpoint Conventions (from `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)

- **Naming**: Handler functions use `snake_case` verbs: `get`, `list`, `get_by_id`
- **File naming**: One handler per file, named after the HTTP operation or resource action
- **Path extraction**: Use Axum `Path<Id>` extractor for path parameters
- **Service injection**: Services injected via Axum `State` or `Extension` extractors
- **Response pattern**: Handlers return `Result<Json<T>, AppError>` — Axum serializes the response struct automatically
- **Route registration**: In `endpoints/mod.rs`, use `Router::new().route("/path", get(handler))` pattern; all module routes compose into the main router

### Error Handling Conventions (from `common/src/error.rs`)

- **Error type**: `AppError` enum implements `IntoResponse` for Axum
- **Context wrapping**: Use `.context()` on Result for human-readable error messages
- **HTTP mapping**: `AppError` maps to appropriate HTTP status codes (404 for not found, 500 for internal errors)
- **Pattern**: `Result<T, AppError>` is the universal return type for both service methods and endpoint handlers

### Test Conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

- **Location**: Integration tests live in `tests/api/` directory, one file per domain
- **File naming**: Test files named after the domain: `advisory.rs`, `sbom.rs`, `search.rs`
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` for status checks; value-based assertions on response body fields
- **Test database**: Tests use a real PostgreSQL test database (not mocks)
- **Setup pattern**: Tests set up test data, make HTTP requests via the test client, and assert on response status and body
- **Parameterized tests**: Not observed in sibling test files; individual test functions used for each case
- **Test naming**: `test_<action>_<scenario>` pattern (e.g., `test_get_advisory`, `test_list_sboms`)

### Import Organization

- Standard library imports first
- External crate imports second (axum, serde, sea_orm)
- Internal crate imports last (common::, entity::)
- Grouped by blank lines between sections

### Skill Guidance Overrides

- **Test documentation**: Skill requires doc comments on every test function (`///` in Rust) even though sibling tests may not have them. This is a new standard introduced by the skill.
- **Value-based assertions**: Skill requires asserting on actual values rather than just counts. Sibling tests already follow this pattern (no conflict).
- **Given-when-then comments**: Skill requires section comments in non-trivial tests. This may not be present in siblings but is adopted per skill guidance.
