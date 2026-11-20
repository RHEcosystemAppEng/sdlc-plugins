# Conventions Discovered (Step 4 – Convention Conformance Analysis)

Task: TC-9201 — Add advisory severity aggregation service and endpoint
Repository: trustify-backend (Serena instance: `serena_backend`, rust-analyzer)

## Sources analyzed

Sibling analysis (planned via `mcp__serena_backend__get_symbols_overview` / `find_symbol`; simulated from repo-backend.md):

- Endpoints siblings: `modules/fundamental/src/advisory/endpoints/get.rs`, `.../advisory/endpoints/list.rs`, `.../sbom/endpoints/get.rs`, `.../advisory/endpoints/mod.rs`
- Service siblings: `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`, `search`), `modules/fundamental/src/sbom/service/sbom.rs`
- Model siblings: `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`, has `severity`), `.../advisory/model/details.rs`, `.../sbom/model/summary.rs`
- Entity: `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`, `entity/src/sbom.rs`
- Errors: `common/src/error.rs` (`AppError`, implements `IntoResponse`)
- Test siblings: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`
- `CONVENTIONS.md` at repo root (present per directory tree) — would be read in full; CI-check commands extracted from it for Step 9
- Docs: `README.md`, `docs/api.md` (REST API reference), `docs/architecture.md`

## Module structure

- Each domain module uses `model/ + service/ + endpoints/` layout.
- One struct/concept per file in `model/` (e.g. `summary.rs`, `details.rs`), registered with `pub mod <name>;` in `model/mod.rs`.
- One handler per file in `endpoints/` (`get.rs`, `list.rs`), registered in `endpoints/mod.rs`.
- `server/src/main.rs` mounts module routers; individual routes are not added there.

## Naming

- Files: snake_case named after the concept (`summary.rs`, `severity_summary.rs`).
- Structs: PascalCase with domain prefix/suffix (`AdvisorySummary`, `SbomDetails`, `SeveritySummary`).
- Services: `<Domain>Service` with verb-style methods (`fetch`, `list`, `search`) -> new method `severity_summary`.
- Handlers: short verb or concept names matching file (`get`, `list`) -> new handler `severity_summary` in `severity_summary.rs`.
- Test functions: snake_case describing scenario (e.g. `test_<behavior>` / descriptive names).

## API design / parameter propagation

- Service methods take `&self`, the domain key (`Id`), and `tx: &Transactional<'_>` as the last parameter; return `Result<T, Error>`.
- Handlers extract path params with `Path<Id>`, take the service via `State`/`Extension` (as in `get.rs`), call the service with `Transactional::None`, and return the result serialized as JSON.
- Routes registered via `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`.
- Single-object responses return the struct directly (Json serialization); list responses use `PaginatedResults<T>` (not applicable here).
- Caching via `tower-http` middleware configured in route builders — follow whatever `get.rs` route uses (if any).

## Error handling

- Handlers return `Result<T, AppError>`.
- Errors wrapped with `.context("...")` (anyhow-style) per `common/src/error.rs`.
- Missing entity -> `AppError::NotFound` (maps to HTTP 404), consistent with `GET /api/v2/sbom/{id}`.

## Database access

- SeaORM entities in `entity/src/`; join table `sbom_advisory` links SBOMs to advisories.
- Query helpers in `common/src/db/query.rs` for filtering/pagination/sorting — reuse where applicable; aggregation is done in SQL (SeaORM select + join) rather than loading full rows into memory.

## Model / serialization

- Response structs derive `Serialize, Deserialize, Debug, Clone, PartialEq` and `utoipa::ToSchema` (for OpenAPI), matching `AdvisorySummary`.
- Doc comments (`///`) on public structs and fields.

## Test conventions

- Integration tests in `tests/api/<area>.rs`, hitting a real PostgreSQL test database.
- Status assertions: `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Response bodies deserialized into the model struct and asserted.
- Siblings do not appear to use `rstest` parameterized tests -> do not introduce them; write individual test functions (the four scenarios also differ in setup/assertions, so Meszaros heuristic agrees).

## Skill guidance overriding sibling patterns (recorded deviations)

- Every test function gets a `///` doc comment, and non-trivial tests get `// Given / // When / // Then` sections — even if sibling tests lack them.
- Value-based assertions: assert the full `SeveritySummary` value (`assert_eq!(body, SeveritySummary { critical: 2, ... })`) rather than only checking status or count fields.

## Convention conflicts / flags

- Route path vs. module: the endpoint is `/api/v2/sbom/{id}/advisory-summary` (SBOM-scoped path) but the task places it in the advisory module's `endpoints/mod.rs`. Advisory router is mounted at `/api/v2/advisory`, so the route must be registered with the full path (or a router merged at root) rather than relative to the advisory prefix. Would be verified against `endpoints/mod.rs` and flagged to the user if the advisory router is nested under a prefix.
- `server/src/main.rs` is listed in Files to Modify but marked "no changes needed" — it will not be edited.
