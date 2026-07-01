# Conventions Analysis for TC-9201

## Source: CONVENTIONS.md (Repository Root)

The repository root contains a `CONVENTIONS.md` file. Its contents would be read and followed throughout implementation. Key conventions from the repository structure documentation:

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database
- **Caching**: Uses `tower-http` caching middleware

## Discovered Conventions (from Sibling Analysis)

### Production Code Conventions

Sibling files analyzed:
- `modules/fundamental/src/advisory/endpoints/get.rs` (sibling endpoint handler)
- `modules/fundamental/src/advisory/endpoints/list.rs` (sibling endpoint handler)
- `modules/fundamental/src/advisory/model/summary.rs` (sibling model)
- `modules/fundamental/src/advisory/model/details.rs` (sibling model)
- `modules/fundamental/src/advisory/service/advisory.rs` (target service file)
- `modules/fundamental/src/sbom/endpoints/get.rs` (cross-module sibling)

#### Endpoint Handler Patterns
- **Path extraction**: Handlers use `Path<Id>` extractor from Axum to extract path parameters
- **Service invocation**: Handlers call the corresponding service method, passing the extracted ID and a transactional context (`tx: &Transactional<'_>`)
- **Return type**: Handlers return `Result<Json<T>, AppError>` where `T` is the response struct
- **Error wrapping**: Errors are wrapped with `.context("descriptive message")` before returning
- **Route registration**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern

#### Model Struct Patterns
- **Derive macros**: Model structs derive `Serialize, Deserialize, Debug, Clone` (at minimum `Serialize` for response types)
- **Field types**: Use standard Rust types; severity is represented as a string field in `AdvisorySummary`
- **Module registration**: New model modules are registered in `model/mod.rs` via `pub mod <module_name>;`
- **Documentation**: Structs have doc comments explaining their purpose

#### Service Method Patterns
- **Method signature**: Service methods take `&self`, the primary identifier, and `tx: &Transactional<'_>`
- **Naming**: Methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Query construction**: Use SeaORM query builders with entity definitions from `entity/src/`
- **Error handling**: Return `Result<T, anyhow::Error>` or `Result<T, AppError>` with `.context()` wrapping
- **Join tables**: Cross-entity queries use join table entities (e.g., `sbom_advisory` for SBOM-Advisory relationships)

#### Import Organization
- Standard library imports first
- External crate imports second (axum, serde, sea_orm)
- Internal crate imports third (using `crate::` paths)

#### Error Handling
- All handlers use `Result<T, AppError>` return type
- Error wrapping with `.context()` from `anyhow`
- `AppError` enum defined in `common/src/error.rs` implements `IntoResponse`

### Test Conventions

Sibling test files analyzed:
- `tests/api/advisory.rs` (advisory endpoint integration tests)
- `tests/api/sbom.rs` (SBOM endpoint integration tests)
- `tests/api/search.rs` (search endpoint integration tests)

#### Assertion Style
- Use `assert_eq!(resp.status(), StatusCode::OK)` for successful responses
- Use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 responses
- Deserialize response body and assert on specific field values

#### Response Validation
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-item endpoint tests validate specific fields of the returned object
- Tests check both the HTTP status code and the response body content

#### Error Case Coverage
- All endpoint test files include a 404 test for non-existent resource IDs
- Tests verify error response format matches `AppError` structure

#### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`)

#### Test Setup
- Tests use a real PostgreSQL test database
- Test data is seeded before assertions
- Each test function is independent (no shared mutable state between tests)

#### Test Organization
- One test file per domain endpoint group in `tests/api/`
- Tests grouped by endpoint within the file

## Convention Conflicts

No conflicts detected between the task description/Implementation Notes and discovered conventions. The task explicitly references following existing patterns in `get.rs` and using `Result<T, AppError>` with `.context()`, which aligns with the discovered conventions.

## Cross-Section Reference Consistency

- Entity `AdvisoryService` -- referenced in both Files to Modify (`modules/fundamental/src/advisory/service/advisory.rs`) and Implementation Notes (`modules/fundamental/src/advisory/service/advisory.rs`) -- **CONSISTENT**
- Entity `AdvisorySummary` -- referenced in Implementation Notes (`modules/fundamental/src/advisory/model/summary.rs`) for its `severity` field -- **CONSISTENT** with model directory structure
- Entity `sbom_advisory` -- referenced in Implementation Notes (`entity/src/sbom_advisory.rs`) -- **CONSISTENT** with entity directory
- Entity `AppError` -- referenced in Implementation Notes (`common/src/error.rs`) -- **CONSISTENT** with common directory
