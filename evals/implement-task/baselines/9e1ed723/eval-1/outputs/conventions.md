# Conventions Discovered — trustify-backend (sibling analysis for TC-9201)

Sources: siblings `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`,
`sbom/endpoints/get.rs`, `advisory/service/advisory.rs` (`fetch`, `list`),
`sbom/service/sbom.rs`, `advisory/model/summary.rs`, `advisory/model/details.rs`,
`common/src/error.rs`, `tests/api/advisory.rs`, `tests/api/sbom.rs`, plus `CONVENTIONS.md`
and the repo's Key Conventions. (Serena `serena_backend`: `get_symbols_overview` on 2–3 siblings
per role. If Serena were unavailable, Read/Glob would be used instead.)

## Module structure
- Each domain module uses `model/ + service/ + endpoints/`, and every submodule is declared in its parent `mod.rs` (`pub mod summary;`, `pub mod details;`).
- One file per response type in `model/` (`summary.rs` → `AdvisorySummary`, `details.rs` → `AdvisoryDetails`). The new type therefore goes in `model/severity_summary.rs` as `SeveritySummary`.
- One file per handler in `endpoints/` (`get.rs`, `list.rs`). The new handler goes in `endpoints/severity_summary.rs`.
- Service logic lives in a single `<Domain>Service` struct (`AdvisoryService`, `SbomService`), and handlers stay thin.
- `server/src/main.rs` mounts module routers. Individual routes are never added there.

## Naming
- Types: `PascalCase` with a `<Domain><Kind>` suffix (`SbomSummary`, `AdvisoryDetails`, `PackageSummary`).
- Service methods: short `snake_case` verbs or nouns (`fetch`, `list`, `search`, `ingest`). New method: `severity_summary`.
- Files: `snake_case.rs` matching the type or handler.
- URL paths: kebab-case, versioned under `/api/v2/<resource>` (`/api/v2/sbom/{id}`). New path: `/api/v2/sbom/{id}/advisory-summary`.
- Integration test files are named after the resource (`tests/api/advisory.rs`). Test functions use the `test_<subject>_<behaviour>` snake_case pattern.

## Error handling
- Every handler and service method returns `Result<T, AppError>` (`common/src/error.rs`). `AppError` implements `IntoResponse`, which maps `NotFound` to 404.
- Fallible calls are wrapped with `.context("...")` to add a human-readable message.
- A missing entity becomes `AppError::NotFound` (the SBOM `get` endpoint returns 404 this way), so the new endpoint reuses that mechanism.
- No `unwrap()`/`expect()` in production paths.

## Service / parameter propagation
- Service method signature: `pub async fn <name>(&self, <id>: Id, tx: &Transactional<'_>) -> Result<T, AppError>`. The transaction reference comes last, and the DB connection is obtained from `tx` (e.g. `self.db.connection(tx)`).
- Handlers pass `Transactional::None` (read-only endpoints).
- DB access goes through SeaORM entities from the `entity` crate (`sbom`, `advisory`, `sbom_advisory`). Join tables are used for relationship queries.
- Shared filtering, pagination, and sorting come from `common/src/db/query.rs`. They are not needed here because the response is not a list.

## API / endpoint design
- Handlers use Axum extractors: `Path<Id>` for path params and `State<...>` (or `Extension`) for the service.
- Single-object responses are returned as `Json<T>`. List responses use `PaginatedResults<T>`, which does not apply here because the result is a single aggregate object.
- Routes are registered in `endpoints/mod.rs` via `Router::new().route("/path", get(handler))`, and each handler module is declared with `mod <handler>;`.
- Caching: the `tower-http` caching middleware is configured in the route builders. The new route goes into the same builder, so it inherits the same layers.
- Response structs derive `Serialize` (+ `Deserialize`, `Debug`, `Clone`) and `utoipa::ToSchema` for OpenAPI. Handlers are annotated with `#[utoipa::path(...)]` where siblings use it.

## Imports
- Ordering: `std`, then external crates (`axum`, `sea_orm`, `serde`), then workspace crates (`trustify_common`, `trustify_entity`), then `crate::`/`super::`.
- Workspace crates are imported by crate name, not by relative path.

## Test conventions
- Integration tests live in `tests/api/*.rs` and hit a real PostgreSQL test database, using the shared test context/fixture helpers from sibling tests to ingest SBOMs and advisories.
- Status assertions use the pattern `assert_eq!(resp.status(), StatusCode::OK)` (and `StatusCode::NOT_FOUND` for missing resources).
- Body checks deserialize the response JSON into the typed struct.
- Error cases (404) get their own tests.
- Parameterized tests: the siblings show no `rstest` usage, so none are introduced. Each scenario also has different setup and behaviour, which means the Meszaros heuristic recommends separate tests anyway.

## Skill guidance that overrides sibling patterns (recorded deviations)
- **Value-based assertions**: tests compare the full `SeveritySummary` struct with `assert_eq!(body, SeveritySummary { critical: 1, ... })` rather than checking only `total` or individual fields.
- **Test documentation**: every test function gets a `///` doc comment and `// Given / // When / // Then` sections, even though sibling tests may not have them.
- **Doc comments on new symbols**: `SeveritySummary`, each of its fields, `severity_summary`, and the handler all get `///` docs.

## CI checks (from CONVENTIONS.md, to be extracted at runtime)
- Expected: `cargo fmt --all -- --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo check`, and any OpenAPI generation command (e.g. regenerating `openapi.yaml`). The exact commands are taken from CONVENTIONS.md's CI section and run in Step 9. Any non-zero exit is a hard stop.

## Conflicts detected
- None between the task's Implementation Notes and the sibling conventions.
- One note: the route is under `/api/v2/sbom/...` but is registered in the advisory endpoints module. The task explicitly specifies this, so it is followed as given.
