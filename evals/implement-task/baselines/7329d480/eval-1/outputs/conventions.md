# Discovered Conventions from Sibling Analysis

## Production code conventions

### Module structure

- Each domain module follows the `model/ + service/ + endpoints/` tripartite structure
- Model submodules are registered via `pub mod <name>;` in `model/mod.rs`
- Endpoint handlers are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` or similar

### Naming conventions

- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`) -- the new method `severity_summary` follows noun_noun but describes the return value, which is consistent with query-style methods
- Model structs are named with a descriptive suffix: `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails` -- the new struct `SeveritySummary` follows this pattern
- Endpoint handler files are named after the HTTP operation or the resource concept: `get.rs`, `list.rs` -- the new file `severity_summary.rs` follows the resource concept naming

### Error handling

- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped with `.context("descriptive message")` for meaningful error chains
- 404 responses are produced by returning an appropriate `AppError` variant when an entity is not found

### Endpoint patterns (from `advisory/endpoints/get.rs` and siblings)

- Path parameters extracted via Axum's `Path<Id>` extractor
- Service instance obtained from Axum state/extension
- Service method called with the extracted parameters and a `Transactional` reference
- Response returned as `Json<T>` where T is the response struct (Axum handles serialization)

### Service method patterns (from `advisory/service/advisory.rs`)

- Methods take `&self` as the first parameter
- Entity ID passed as `Id` type
- Transaction context passed as `tx: &Transactional<'_>`
- SeaORM used for database queries
- Database operations use the entity crate's models (e.g., `entity::sbom_advisory`)

### Model struct patterns (from `advisory/model/summary.rs`, `advisory/model/details.rs`)

- Structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- Serde attributes used for field naming (`#[serde(rename_all = "camelCase")]` if applicable)
- Documentation comments on the struct and its fields
- Fields use Rust-idiomatic types (`u64`, `String`, `Option<T>`)

### Import organization

- Standard library imports first
- External crate imports second
- Internal module imports third (crate-relative paths)

### Response types

- Single-entity endpoints return the entity struct directly (wrapped in `Json`)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new endpoint returns a single aggregation struct, so it follows the single-entity pattern

## Test conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)

### Assertion style

- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` or `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response body deserialized from JSON and then field values asserted individually
- Value-based assertions preferred over length-only checks

### Response validation

- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate key identifying fields (e.g., ID, name)
- Aggregation tests should validate each individual field value

### Error cases

- Every endpoint test suite includes a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs
- Error response body is also validated where applicable

### Test naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_advisory_not_found`)
- Descriptive scenario suffixes: `_with_known_advisories`, `_nonexistent_sbom`, `_no_advisories`, `_deduplication`

### Test organization

- One test file per endpoint group in `tests/api/`
- Tests grouped by success and failure scenarios within each file

### Test setup

- Tests use a real PostgreSQL test database
- Test data created via helper functions or fixtures
- Each test sets up its own data to avoid inter-test dependencies

### Test documentation

- Every test function will have a `///` doc comment explaining what it verifies (this is an AI-generated standard applied regardless of sibling convention)
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments

### Parameterized tests

- Sibling tests do not appear to use parameterized test patterns (`#[rstest]`)
- Following existing convention: individual test functions for each scenario rather than parameterized tests
