# Conventions Discovered (Step 4 – Convention Conformance Analysis)

Target repository: `trustify-backend` (Serena instance `serena_backend`, rust-analyzer).
Siblings analyzed (planned via `mcp__serena_backend__get_symbols_overview`, simulated from repo-backend.md):

- Production siblings: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`, `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`, `search`), `modules/fundamental/src/sbom/service/sbom.rs`
- Test siblings: `tests/api/advisory.rs`, `tests/api/sbom.rs`

CONVENTIONS.md: present at repo root (`./CONVENTIONS.md`). It must be read and followed; its CI check commands (e.g. fmt / clippy / check) are extracted for Step 9. Since its content is not part of the fixture, the plan assumes the standard Rust trio (`cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo check`) and must be replaced by the exact commands listed in CONVENTIONS.md. Any OpenAPI generation command listed there must be run and its output committed.

## Module structure
- Each domain module uses `model/ + service/ + endpoints/`. New response struct goes in `advisory/model/`, new handler in `advisory/endpoints/`, service logic as a method on `AdvisoryService`.
- One file per model struct (`summary.rs` -> `AdvisorySummary`, `details.rs` -> `AdvisoryDetails`); registered with `pub mod <name>;` in `model/mod.rs`.
- One file per endpoint handler (`list.rs`, `get.rs`); registered as a module in `endpoints/mod.rs` and wired via `Router::new().route("/path", get(handler))`.
- `server/src/main.rs` mounts modules; routes registered in a module's `endpoints/mod.rs` are picked up automatically — no change to `main.rs`.

## Naming
- Files: `snake_case.rs` named after the concept (`severity_summary.rs`).
- Types: `PascalCase` with a domain-suffix (`AdvisorySummary`, `SbomDetails`) -> `SeveritySummary`.
- Service methods: short verb / noun (`fetch`, `list`, `search`) -> `severity_summary`.
- Handlers: named after the action (`get`, `list`) -> `severity_summary` handler fn in `endpoints/severity_summary.rs`.
- Tests: `snake_case` fn names describing behavior.

## API design / parameter propagation
- Service methods signature: `pub async fn <name>(&self, <params>, tx: &Transactional<'_>) -> Result<T, AppError>`; transaction passed as the last argument.
- Handlers extract path params via `Path<Id>`, get the service via Axum state/extension, call the service, return the result serialized as JSON.
- Single-item responses return the struct (Json); list responses use `PaginatedResults<T>` (not applicable here — this is a single aggregate object).
- Caching middleware (`tower-http`) is configured in endpoint route builders — follow whatever the sibling `get` route applies.

## Error handling
- All handlers return `Result<T, AppError>`; errors wrapped with `.context("...")` (pattern in `common/src/error.rs`).
- Not-found is surfaced as `AppError::NotFound` (or equivalent variant in `common/src/error.rs`) -> HTTP 404, consistent with `GET /api/v2/sbom/{id}`.
- `fetch` returns `Option<T>` at service level and the handler maps `None` to 404 — the new method mirrors the SBOM existence check.

## Database / query
- SeaORM entities in `entity/src/`; joins via relation entities (`sbom_advisory` join table between `sbom` and `advisory`).
- Shared query helpers in `common/src/db/query.rs` — reuse where filtering/sorting applies rather than hand-writing SQL.

## Serialization / model
- Model structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, plus `utoipa::ToSchema` for OpenAPI (if present on siblings), and have `///` doc comments.

## Imports
- Group: std, external crates (axum, sea_orm, serde), then workspace crates (`trustify_common`, `trustify_entity`), then `crate::` / `super::`.

## Test conventions
- Integration tests in `tests/api/<feature>.rs` hit a real PostgreSQL test DB (shared test context/fixtures from sibling tests).
- Status assertion: `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Error case coverage: siblings test the 404 path for unknown IDs.

### Skill guidance that overrides sibling patterns (recorded deviations)
- Value-based assertions: assert the full deserialized `SeveritySummary` body (each field value), not just status or counts of items.
- Every test fn gets a `///` doc comment, even if sibling tests lack them.
- Non-trivial tests use `// Given` / `// When` / `// Then` section comments.
- Parameterized tests (`rstest`): only introduce if siblings already use them. The four required tests differ in setup and assertions (404 vs body), so they stay as individual tests regardless.

## Convention conflicts with the task
- `server/src/main.rs` is listed in Files to Modify but marked "no changes needed" — no conflict; it will be left untouched.
- Route path `/api/v2/sbom/{id}/advisory-summary` lives under the SBOM path prefix but is registered in the **advisory** module's `endpoints/mod.rs` (as the task instructs). Routes are absolute in the Router, so this works; noted for reviewers but not a blocking conflict.
