# Discovered Conventions — TC-9201 (trustify-backend)

Source of analysis: sibling files in the target modules, inspected via the `serena_backend`
Serena instance (`get_symbols_overview` / `find_symbol`), plus `CONVENTIONS.md` at the repo
root (Registry path `./`) and the "Key Conventions" section of the repository description.

Siblings analyzed:
- Production (endpoints): `modules/fundamental/src/advisory/endpoints/get.rs`,
  `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`
- Production (service): `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`, `search`),
  `modules/fundamental/src/sbom/service/sbom.rs` (`fetch`, `list`)
- Production (model): `modules/fundamental/src/advisory/model/summary.rs`, `.../model/details.rs`,
  `modules/fundamental/src/sbom/model/summary.rs`
- Tests: `tests/api/advisory.rs`, `tests/api/sbom.rs`

## 1. Module structure
- Each domain module follows `model/ + service/ + endpoints/`.
- Each file under `model/` holds one response struct; `model/mod.rs` declares `pub mod <name>;`
  (e.g., `pub mod summary; pub mod details;`). New model -> `model/severity_summary.rs` +
  `pub mod severity_summary;`.
- Each endpoint handler lives in its own file under `endpoints/` (`get.rs`, `list.rs`);
  `endpoints/mod.rs` declares the submodules and builds the `Router`.
- `server/src/main.rs` mounts each module's router; no per-route changes are needed there.

## 2. Naming
- Files and functions: `snake_case`, file named after the handler/model (`get.rs`, `list.rs`, `summary.rs`).
- Structs: `PascalCase` with domain prefix/suffix (`AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`).
  New struct: `SeveritySummary`.
- Service methods: short verbs on the service struct (`fetch`, `list`, `search`). New method: `severity_summary`.
- Route paths: kebab-case under `/api/v2/<entity>` (new: `/api/v2/sbom/{id}/advisory-summary`).

## 3. Service method signature / parameter propagation
- Methods take `&self`, domain args, then `tx: &Transactional<'_>` last.
- Return `Result<T, Error>` (module error that converts into `AppError`); `fetch` returns
  `Result<Option<T>, _>` so the endpoint maps `None` to 404.
- DB access through SeaORM entities from the `entity` crate; connection obtained from the
  transactional wrapper (`self.db.connection(tx)` style).
- Shared query building (filters/pagination/sorting) via `common/src/db/query.rs` — reuse, do not
  re-implement (not needed here: no pagination/filtering on this endpoint).

## 4. Endpoint pattern
- Handler is an `async fn` that receives `State<...Service>` (or `Extension`) and `Path<Id>`.
- Calls the service with `Transactional::None` for read-only operations.
- Returns `Result<Json<T>, AppError>` (single-entity endpoints return the struct as JSON; only list
  endpoints use `PaginatedResults<T>`).
- Missing entity -> `AppError::NotFound` (404), as in `sbom/endpoints/get.rs` and `advisory/endpoints/get.rs`.
- Route registration: `Router::new().route("/path", get(handler))` chained in `endpoints/mod.rs`.
- Caching: `tower-http` caching middleware configured in the route builder — new read-only route
  should be attached to the same builder chain so it inherits the module's caching layer.
- OpenAPI: handlers carry `#[utoipa::path(...)]` annotations where siblings have them (match sibling).

## 5. Error handling
- All handlers return `Result<T, AppError>` (`common/src/error.rs`, implements `IntoResponse`).
- Errors from DB/service calls wrapped with `.context("...")` describing the failed operation.
- No `unwrap()`/`expect()` in production code paths.

## 6. Model/serialization
- Response structs derive `Debug, Clone, Serialize, Deserialize, PartialEq` (+ `ToSchema` when siblings
  use utoipa) and have `///` doc comments.
- Numeric counts as `u64`; fields `snake_case` (serde default naming, matches required
  `{ critical, high, medium, low, total }`).
- `AdvisorySummary.severity` is the source of the severity value.

## 7. Imports
- Grouped: `crate::`/workspace crates (`trustify_common`, `trustify_entity`) first, then external
  crates (`axum`, `sea_orm`, `serde`), then `std`. One `use` per crate with nested braces.

## 8. Test conventions (`tests/api/*.rs`)
- Integration tests against a real PostgreSQL test DB using the shared test context/fixture helpers.
- One file per endpoint group (`sbom.rs`, `advisory.rs`, `search.rs`) -> new file `advisory_summary.rs`.
- Status assertions: `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Response bodies deserialized into the model struct and asserted on values.
- Error case coverage: each endpoint has a not-found test.
- Test names: `snake_case` describing behavior; `#[tokio::test]` async tests.
- Parameterized tests: siblings do not use `rstest` -> do not introduce it (per skill rule).

## Skill guidance overrides (recorded conflicts)
- **Test documentation**: siblings largely lack doc comments on tests; per skill Step 7, every new test
  gets a `///` doc comment and non-trivial tests get `// Given / // When / // Then` sections.
- **Value-based assertions**: where siblings assert only on `len()`/status, new tests assert on the full
  `SeveritySummary` value with `assert_eq!` (e.g., `assert_eq!(body, SeveritySummary { critical: 1, .. })`).
- No conflicts found between the task description and sibling conventions that require user guidance.
