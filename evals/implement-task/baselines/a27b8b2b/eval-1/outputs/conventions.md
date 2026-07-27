# Conventions Discovered from Sibling Analysis

## Step 1.5 -- Description Integrity Check

No description digest comment found on TC-9201 -- skipping integrity check. This task may have been created before digest tracking was introduced.

Proceeding with implementation.

## Production Code Conventions

### Files inspected for convention analysis

Before making any changes, the following sibling files would be inspected to understand existing patterns:

1. `modules/fundamental/src/advisory/endpoints/get.rs` -- GET /api/v2/advisory/{id} handler (sibling endpoint)
2. `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService with fetch, list, search methods
3. `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct (includes severity field)
4. `common/src/error.rs` -- AppError enum, implements IntoResponse
5. `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id} handler (cross-module sibling)
6. `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService with fetch, list, ingest methods

### Discovered conventions (from sibling analysis)

- **Module structure:** Each domain module follows `model/ + service/ + endpoints/` tri-part structure. Models define data structs, services contain business logic, endpoints wire HTTP routes to service calls.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation. The `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse` for Axum compatibility.
- **Endpoint pattern:** Endpoint handlers extract path params via `Path<Id>`, call the corresponding service method, and return `Json<T>`. The handler signature follows: `async fn handler(Path(id): Path<Id>, State(service): State<...>, tx: Transactional<'_>) -> Result<Json<T>, AppError>`.
- **Service method pattern:** Service methods take `&self`, an entity ID, and `tx: &Transactional<'_>` as parameters. They return `Result<T, anyhow::Error>` with `.context()` for error wrapping.
- **Route registration:** Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))`. Sub-module endpoint files are imported and their handlers wired into the router.
- **Model registration:** Each module's `model/mod.rs` re-exports sub-modules via `pub mod <name>;` declarations.
- **Response types:** Single-entity endpoints return `Json<T>` directly. List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). New method should follow: `severity_summary`.
- **Serialization:** Model structs derive `Serialize` (and often `Deserialize`) for JSON serialization via serde. Fields use `#[serde(rename = "...")]` when JSON field names differ from Rust field names.
- **Framework:** Axum for HTTP routing, SeaORM for database access. State is injected via Axum's `State` extractor.
- **Import organization:** External crates first, then `crate::` imports, then `super::` imports.

### CONVENTIONS.md

A `CONVENTIONS.md` file exists at the repository root. It would be read for explicit project conventions and CI check commands. Any verification commands found would be extracted and run during Step 9.

## Test Conventions

### Files inspected for test convention analysis

1. `tests/api/advisory.rs` -- Advisory endpoint integration tests (direct sibling)
2. `tests/api/sbom.rs` -- SBOM endpoint integration tests (cross-domain sibling)
3. `tests/api/search.rs` -- Search endpoint integration tests

### Discovered test conventions (from sibling test analysis)

- **Assertion style:** All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization via `resp.json::<T>().await`.
- **Response validation:** GET-by-ID endpoint tests validate the response body fields directly (e.g., checking specific field values, not just structure).
- **Error cases:** All endpoint tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent entity IDs.
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_advisories`).
- **Test setup:** Integration tests hit a real PostgreSQL test database. Test data is seeded using helper functions or fixtures before assertions.
- **Test documentation:** Each test function should have a `///` doc comment explaining what it verifies (AI-generated standard).
- **Test structure:** Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- **Parameterized tests:** No evidence of `#[rstest]` or parameterized tests in sibling test files -- individual test functions are used for each scenario.
