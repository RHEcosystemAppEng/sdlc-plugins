# Conventions Discovered (Step 4 – Convention Conformance Analysis)

Task: TC-9201 — trustify-backend (Serena instance: `serena_backend`, rust-analyzer)

## Sources analyzed

Sibling files (would be inspected via `mcp__serena_backend__get_symbols_overview` / `find_symbol(include_body=true)`):

- Endpoints: `modules/fundamental/src/advisory/endpoints/get.rs`, `.../advisory/endpoints/list.rs`, `.../sbom/endpoints/get.rs`, `.../advisory/endpoints/mod.rs`, `.../sbom/endpoints/mod.rs`
- Services: `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`, `search`), `modules/fundamental/src/sbom/service/sbom.rs` (`fetch`, `list`, `ingest`)
- Models: `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`), `.../advisory/model/details.rs`, `.../sbom/model/summary.rs`, `.../package/model/summary.rs`
- Entities: `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`, `entity/src/sbom.rs`
- Errors: `common/src/error.rs` (`AppError`, implements `IntoResponse`)
- Tests: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`
- Repo root: `CONVENTIONS.md` (present — read and followed; its CI-check section supplies the verification commands for Step 9), `README.md`

## Module structure

- Every domain module follows `model/ + service/ + endpoints/`.
- New model types live in their own file under `model/` and are registered with `pub mod <name>;` in `model/mod.rs`.
- New handlers live in their own file under `endpoints/` (one handler per file: `list.rs`, `get.rs`) and are registered in `endpoints/mod.rs`.
- `server/src/main.rs` mounts module routers; individual routes are NOT added there.

## Naming

- Files: `snake_case`, named after the resource/action (`summary.rs`, `details.rs`, `get.rs`, `list.rs`) -> `severity_summary.rs`.
- Structs: `PascalCase` with domain prefix/suffix (`AdvisorySummary`, `SbomDetails`) -> `SeveritySummary`.
- Service methods: `snake_case` verbs/nouns on the service struct (`fetch`, `list`, `search`) -> `severity_summary`.
- Handler functions: named after the action (`get`, `list`) -> `get` inside `endpoints/severity_summary.rs`.
- Test functions: `snake_case`, descriptive of the scenario.

## Service method signature / parameter propagation

- Methods take `&self`, domain IDs, and the transaction last: `async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<..., Error>`.
- DB connection obtained from the transaction (`self.db.connection(tx)`), queries built with SeaORM entities.
- Shared query helpers in `common/src/db/query.rs` used for filtering/pagination/sorting (not needed for an aggregate count, but checked for reuse).

## Error handling

- All handlers return `Result<T, AppError>`.
- Errors are wrapped with `.context("...")` (pattern in `common/src/error.rs`).
- "Not found" is surfaced as `AppError::NotFound` (or `Option` -> 404 mapping), consistent with `sbom/endpoints/get.rs` returning 404 for unknown SBOM IDs.

## Endpoint pattern

- Path params extracted via `Path<Id>`; service injected via Axum `State`/`Extension` (same as `get.rs`).
- Response returned as `Json(value)`; single-resource endpoints return the struct directly, list endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- Routes registered as `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`.
- Caching via `tower-http` middleware configured in the route builders — follow the same builder chain as sibling routes.

## Model / serialization

- Response structs derive `Serialize, Deserialize, Debug, Clone, PartialEq` (plus `utoipa::ToSchema` if siblings use it for OpenAPI) and carry `///` doc comments.
- Field names are `snake_case` and serialize as-is (`critical`, `high`, ...).

## Imports

- Grouped: std -> external crates (`axum`, `sea_orm`, `serde`) -> workspace crates (`trustify_common`, `trustify_entity`) -> `crate::`/`super::` locals.

## Test patterns

- Integration tests in `tests/api/` against a real PostgreSQL test DB (bootstrapped by the test harness).
- Status assertion: `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Response body deserialized into the model type and compared.
- Setup: ingest fixture SBOM/advisories with the shared test context helper, then hit the endpoint.

## Skill-guidance overrides (recorded deviations from siblings)

- **Value-based assertions**: compare the full deserialized `SeveritySummary` with `assert_eq!(body, SeveritySummary { ... })` rather than only checking status or counts of items — skill guidance takes precedence over any length-only/`.any()` sibling checks.
- **Test documentation**: every test function gets a `///` doc comment and `// Given / // When / // Then` sections, even if sibling tests lack them.
- **Parameterization**: the four test scenarios differ in setup and assertions (404 vs body), so they stay as separate tests (Meszaros heuristic); no `rstest` introduced unless siblings already use it.
- **Doc comments on new symbols**: `SeveritySummary`, its fields, `severity_summary`, and the handler get `///` docs.

## Convention conflicts / observations to flag

- The new route `/api/v2/sbom/{id}/advisory-summary` lives under the `/api/v2/sbom` prefix but the task directs registration in `advisory/endpoints/mod.rs` (which mounts `/api/v2/advisory`). Plan: register the full absolute path in the advisory router as instructed (the advisory module owns the logic). If the advisory router is nested under `/api/v2/advisory`, this would produce the wrong path — flag to the user before implementation.
- `server/src/main.rs` is listed in Files to Modify but marked "no changes needed" — it will not be touched.
