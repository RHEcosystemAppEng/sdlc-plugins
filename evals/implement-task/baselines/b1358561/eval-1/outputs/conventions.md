# Conventions Discovered (Step 4 – Convention Conformance Analysis)

Sources: `CONVENTIONS.md` (repo root, read via `mcp__serena_backend__*` / Read fallback),
the "Key Conventions" in the repo structure, and sibling files analyzed with
`get_symbols_overview` / `find_symbol`:

- Production siblings: `modules/fundamental/src/advisory/endpoints/get.rs`,
  `modules/fundamental/src/advisory/endpoints/list.rs`,
  `modules/fundamental/src/sbom/endpoints/get.rs`,
  `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`, `search`),
  `modules/fundamental/src/sbom/service/sbom.rs` (`fetch`),
  `modules/fundamental/src/advisory/model/summary.rs`, `.../model/details.rs`,
  `modules/fundamental/src/sbom/model/summary.rs`
- Test siblings: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

## Module structure
- Each domain module uses `model/ + service/ + endpoints/`.
- One file per model struct in `model/` (`summary.rs` -> `AdvisorySummary`, `details.rs` -> `AdvisoryDetails`),
  registered in `model/mod.rs` with `pub mod <name>;` (and re-exported where siblings do so).
- One file per handler in `endpoints/` (`get.rs`, `list.rs`), wired in `endpoints/mod.rs`.
- `server/src/main.rs` mounts each module's router; no per-route edits are needed there.

## Naming
- Files: `snake_case.rs` named after the resource/action (`summary.rs`, `get.rs`).
- Structs: `PascalCase` noun + role suffix (`AdvisorySummary`, `SbomDetails`) -> new `SeveritySummary`.
- Service methods: short verb or noun (`fetch`, `list`, `search`) -> new `severity_summary`.
- Handlers: verb named after the HTTP action/file (`get`, `list`); new handler `severity_summary` (file name match).
- Tests: `snake_case` descriptive names, e.g. `test_<behavior>` / `<resource>_<scenario>`.

## Service API design
- Methods take `&self`, domain args, then `tx: &Transactional<'_>` last.
- Return `Result<Option<T>, Error>` for single-resource lookups (`fetch`) so the endpoint
  maps `None` to 404; return `Result<T, Error>` for collections.
- DB access via SeaORM entities from `entity/` (`entity::sbom`, `entity::advisory`,
  `entity::sbom_advisory`); shared filtering/pagination helpers in `common/src/db/query.rs`.
- Connection obtained through `self.db.connection(tx)` (as in `fetch`/`list`).

## Error handling
- All handlers return `Result<T, AppError>` (`common/src/error.rs`, implements `IntoResponse`).
- Errors wrapped with `.context("...")` describing the failed operation.
- Missing resources: `.ok_or(AppError::NotFound(...))` / equivalent used by SBOM `get` handler -> 404.

## Endpoint pattern (`advisory/endpoints/get.rs`)
- Extractors: `State(service)` / `Extension` for service, `Path(id): Path<Id>` for path params.
- Call service with `Transactional::None`, return `Json(value)` of the model struct directly.
- Routes registered in `endpoints/mod.rs` via `Router::new().route("/path", get(handler))`,
  using the same path-parameter syntax as existing routes.
- Caching configured in route builders via `tower-http` middleware where siblings do so.
- Handlers carry `utoipa::path` annotations when siblings do (keeps OpenAPI spec current).

## Model / serialization
- Response structs derive `Serialize, Deserialize, Debug, Clone, PartialEq, Eq` (+ `ToSchema` if siblings use utoipa) and `Default` where appropriate.
- Field names `snake_case`, serialized as-is (lowercase JSON keys: `critical`, `high`, ...).
- Counts use unsigned integers (`u64`) consistent with `PaginatedResults.total`.
- Doc comments (`///`) on public structs and fields.

## Imports
- Grouped: `crate::...` first, then workspace crates (`trustify_common`, `trustify_entity`),
  then external crates (`axum`, `sea_orm`, `serde`); `use` statements merged per crate.

## Tests (`tests/api/*.rs`)
- Integration tests against a real PostgreSQL test DB using the shared test context/fixture helpers.
- Status assertions: `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Body deserialized into the model struct (`resp.json::<T>()`) and compared.
- One test function per scenario; siblings do NOT use `rstest`/parameterized tests -> do not introduce them.
- Error cases (404) covered alongside the happy path.

## Skill-over-sibling rules applied (recorded conflicts)
- Value-based assertions: compare the whole `SeveritySummary` with `assert_eq!` rather than
  checking single fields or lengths, even where siblings check only status or `.len()`.
- Every test gets a `///` doc comment and `// Given / // When / // Then` sections, even
  though sibling tests do not consistently have them.

## Verification commands (from CONVENTIONS.md CI section)
- `cargo fmt --all -- --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test -p trustify-module-fundamental` and the integration test crate (resolved via `cargo metadata`)
- OpenAPI regeneration command (if listed) -> stage the regenerated spec with the commit.
