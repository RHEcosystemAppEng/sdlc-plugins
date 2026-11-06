# Discovered Conventions — trustify-backend (TC-9201)

Source: Step 4 convention conformance analysis. Siblings examined (via `mcp__serena_backend__get_symbols_overview`
in a live run; here derived from repo-backend.md and the task's Implementation Notes):

- Production siblings: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`,
  `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`,
  `advisory/service/advisory.rs` (`fetch`, `list`, `search`), `sbom/service/sbom.rs` (`fetch`, `list`, `ingest`)
- Test siblings: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

`CONVENTIONS.md` exists at the repository root (`./CONVENTIONS.md` per Repository Registry Path `./`). It would be
read in full and its CI-check commands extracted for Step 9 (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`,
`cargo check`, plus any OpenAPI generation command). The exact commands can't be confirmed from the eval inputs.

## 1. Module / directory structure
- Each domain module uses `model/ + service/ + endpoints/` subdirectories.
- One file per model struct in `model/` (`summary.rs` -> `AdvisorySummary`, `details.rs` -> `AdvisoryDetails`),
  registered with `pub mod <name>;` in `model/mod.rs`.
- One file per endpoint handler in `endpoints/` (`get.rs`, `list.rs`), with routes registered in `endpoints/mod.rs`.
- Services are structs (`AdvisoryService`, `SbomService`) whose methods live in `service/<domain>.rs`.
- `server/src/main.rs` mounts each module's router, so new routes in a module need no server changes.

## 2. Naming
- Files: snake_case, named after the resource or the action (`summary.rs`, `get.rs`, `list.rs`).
- Structs: PascalCase, `<Domain><Shape>` (`AdvisorySummary`, `SbomDetails`, `PackageSummary`).
  The new struct follows this as `SeveritySummary`, in `severity_summary.rs`, as the task specifies.
- Service methods: short snake_case verbs or nouns (`fetch`, `list`, `search`, `ingest`). The new method is `severity_summary`.
- Handlers: snake_case function named after the file/action (`get`, `list`).
- Routes: `/api/v2/<resource>` and `/api/v2/<resource>/{id}`. Sub-resources use kebab-case (`advisory-summary`).

## 3. Service method signature
- `pub async fn <name>(&self, <id>: Id, tx: &Transactional<'_>) -> Result<T, Error>`. The `Transactional` is always
  the last parameter, and the DB connection comes from `self.db.connection(tx)`.
- Single-entity lookups return `Option<T>` (`fetch`), and the handler maps `None` to 404.

## 4. Error handling
- Handlers return `Result<impl IntoResponse, AppError>` (`AppError` lives in `common/src/error.rs` and implements `IntoResponse`).
- Fallible calls are wrapped with `.context("...")` (anyhow-style) before converting into `AppError`.
- Not-found is reported as `AppError::NotFound(..)`, which renders as HTTP 404 (same as `GET /api/v2/sbom/{id}`).

## 5. Endpoint pattern
- Path params come from `Path<Id>`, and the service from `State`/`web::Data`-style extension, depending on how `get.rs` does it.
- The handler calls the service with `Transactional::None` for read-only queries and returns `Json(value)`.
- Registration: `Router::new().route("/path", get(handler))` chained in `endpoints/mod.rs`.
- Caching: `tower-http` caching middleware is configured in the route builders. Match whatever `get.rs` uses for single-resource reads.
- List endpoints return `PaginatedResults<T>`. Not applicable here, because this endpoint returns a single object.

## 6. Model structs
- Derive `Serialize, Deserialize, Debug, Clone, PartialEq, Eq` plus `utoipa::ToSchema` (for OpenAPI) when siblings do.
- Every public struct and field gets a `///` doc comment.

## 7. Database access
- SeaORM entities live in the `entity` crate (`entity::sbom`, `entity::advisory`, `entity::sbom_advisory`).
- Shared filtering, pagination and sorting helpers are in `common/src/db/query.rs`. Reuse them where they apply,
  but an aggregate group-by is not a list query, so no pagination helper is needed.

## 8. Imports
- Group order: std, external crates (axum, sea_orm, serde), workspace crates (`trustify_common`, `trustify_entity`),
  then `crate::` / `super::`.

## 9. Test conventions
- Integration tests in `tests/api/<resource>.rs` run against a real PostgreSQL test DB.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)` and `StatusCode::NOT_FOUND`.
- Tests are async (`#[tokio::test]` or the project's test-context macro, matching `tests/api/advisory.rs`).
- Fixtures are seeded through the ingestor or service helpers already used in `tests/api/sbom.rs` and `advisory.rs`.

## Where skill guidance overrides sibling patterns (recorded deviations)
- **Value-based assertions:** sibling tests may only check status codes or lengths. The new tests deserialize the body
  and `assert_eq!` against the full expected `SeveritySummary`.
- **Test documentation:** every new test function gets a `///` doc comment and `// Given / // When / // Then`
  sections, even if siblings don't have them.
- **Parameterized tests:** none are introduced. The four required tests differ in setup and assertions
  (Meszaros heuristic), and siblings don't appear to use `rstest`.

## Convention conflicts with the task description
- Nothing blocking. One note: the route `/api/v2/sbom/{id}/advisory-summary` sits under the `sbom` path prefix,
  but the task says to register it in `advisory/endpoints/mod.rs`. I follow the task (it's in scope), and the router
  registers the full path explicitly. In a live run I would check whether `advisory/endpoints/mod.rs` nests its
  routes under `/api/v2/advisory`. If it does, the route needs a full-path `.route(...)` outside that nest, which
  I'd raise with the user.
