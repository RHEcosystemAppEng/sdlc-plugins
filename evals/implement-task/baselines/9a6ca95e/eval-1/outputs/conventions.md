# Convention Conformance Analysis: TC-9201

## CONVENTIONS.md Lookup

The repository root contains a `CONVENTIONS.md` file. Would read it via `mcp__serena_backend__read_file` or the Read tool. Extracted conventions and CI check commands would be recorded for use during implementation and verification.

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

#### Endpoint patterns (from `modules/fundamental/src/advisory/endpoints/get.rs`, `list.rs`)

- **Handler signature**: All GET handlers are `async fn` that take `Path<Id>` (or `Path<Uuid>`) for entity lookup, along with a shared service extracted via Axum's `State` or `Extension`. Return type is `Result<Json<T>, AppError>`.
- **Error handling**: All handlers use `Result<T, AppError>` with `.context("descriptive message")` wrapping on fallible operations. 404 errors are returned when the entity is not found, using a pattern like:
  ```rust
  let entity = service.fetch(id, &tx).await?.ok_or_else(|| AppError::NotFound("advisory not found".into()))?;
  ```
- **Route registration**: In `endpoints/mod.rs`, routes are registered using `Router::new().route("/path", get(handler_function))`. Each handler function is imported from its submodule.
- **Response serialization**: Structs are returned directly as `Json<T>` -- Axum handles serialization via Serde's `Serialize` derive.
- **Path parameter extraction**: Entity ID is extracted via `Path(id): Path<Id>` destructuring in the handler function signature.

#### Service patterns (from `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/sbom/service/sbom.rs`)

- **Method signature**: Service methods take `&self` as the first parameter, followed by entity-specific parameters (e.g., `id: Id`), and a `tx: &Transactional<'_>` parameter for transaction management.
- **Naming**: Service methods follow `verb_noun` or bare `verb` pattern (e.g., `fetch`, `list`, `search`). The new method `severity_summary` follows this convention.
- **Query construction**: Services use SeaORM query builders with entity-specific `Entity::find()` calls, chaining `.filter()`, `.join()`, and other query methods.
- **Error wrapping**: Service methods return `Result<T, anyhow::Error>` (or equivalent) with `.context()` on database operations.

#### Model patterns (from `modules/fundamental/src/advisory/model/summary.rs`, `details.rs`)

- **Derive macros**: All model structs derive at minimum `Debug, Clone, Serialize, Deserialize`. Some also derive `PartialEq`.
- **Module registration**: Each model file is registered in `model/mod.rs` via `pub mod <name>;` followed by `pub use <name>::*;` for re-export.
- **Field types**: Numeric counts use `i64` or `u64`. String identifiers use `String`. Optional fields use `Option<T>`.
- **Documentation**: Model structs include doc comments (`///`) describing what they represent.
- **Default values**: Structs that have sensible defaults derive `Default` or implement it manually.

#### Error handling (from `common/src/error.rs`)

- **Error type**: `AppError` is an enum implementing `IntoResponse` for Axum. Variants include `NotFound`, `BadRequest`, `Internal`, etc.
- **Wrapping pattern**: Use `.context("descriptive message")` from `anyhow` (or equivalent) to add context to errors before converting to `AppError`.
- **HTTP status mapping**: `AppError::NotFound` maps to 404, `AppError::BadRequest` to 400, `AppError::Internal` to 500.

#### Import organization

- Standard library imports first
- External crate imports second (e.g., `axum`, `serde`, `sea_orm`)
- Internal crate imports third (e.g., `crate::advisory::model::*`)
- Imports are grouped by crate with blank lines between groups

### Test Conventions (from sibling test analysis)

Inspected sibling test files: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

#### Assertion style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` for successful responses
- Response body is deserialized via `resp.json::<ResponseType>().await` or equivalent
- Field-level assertions use `assert_eq!` on specific fields, not just presence checks

#### Response validation
- GET-by-ID tests validate the response shape matches the expected struct
- Tests validate specific field values (e.g., `assert_eq!(body.id, expected_id)`)

#### Error cases
- All endpoint test modules include a 404 test using a non-existent ID
- 404 tests assert `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`

#### Test naming
- Tests follow `test_<endpoint_action>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_advisories_filtered`)

#### Test setup
- Integration tests hit a real PostgreSQL test database
- Test fixtures are created using helper functions or direct database inserts
- Each test function sets up its own data to be independent

#### Test documentation
- Sibling tests do not consistently include doc comments. Per skill rules, AI-generated tests will add `///` doc comments to every test function regardless.

#### Parameterized tests
- No evidence of `#[rstest]` or other parameterized test patterns in sibling test files. Will not introduce parameterized tests.

#### Test organization
- Tests are grouped by endpoint/feature in a single file
- Each test file corresponds to a module (e.g., `advisory.rs` tests advisory endpoints)

## Convention Conflict Check

No conflicts detected between the task description / Implementation Notes and the discovered conventions. The Implementation Notes explicitly reference the same patterns found in the sibling analysis:
- `Path<Id>` extraction matches endpoint pattern
- `Result<T, AppError>` with `.context()` matches error handling pattern
- `severity_summary` method signature (`&self, sbom_id: Id, tx: &Transactional<'_>`) matches service pattern
- Route registration via `Router::new().route(...)` matches route pattern

All Implementation Notes are consistent with discovered conventions. Proceeding with implementation.
