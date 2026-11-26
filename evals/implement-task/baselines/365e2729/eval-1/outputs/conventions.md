# Conventions Discovered (Step 4 – Convention Conformance Analysis)

Target repository: `trustify-backend` (Serena instance `serena_backend`, rust-analyzer).
Repository root contains `CONVENTIONS.md` — it would be read first via
`mcp__serena_backend__list_dir` / `search_for_pattern` (or Read `./CONVENTIONS.md`), and any
"CI checks" commands it lists would be recorded for Step 9. In this simulated run its contents
are not available, so the conventions below come from sibling analysis of the repository
structure plus the Key Conventions in `repo-backend.md`.

Siblings analyzed (would use `mcp__serena_backend__get_symbols_overview` on each):

| Role | Siblings |
|---|---|
| Endpoint handler | `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs` |
| Route registration | `advisory/endpoints/mod.rs`, `sbom/endpoints/mod.rs`, `package/endpoints/mod.rs` |
| Response model | `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs` |
| Model module registry | `advisory/model/mod.rs`, `sbom/model/mod.rs` |
| Service | `advisory/service/advisory.rs` (`fetch`, `list`, `search`), `sbom/service/sbom.rs` (`fetch`, `list`, `ingest`) |
| Integration tests | `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs` |

## 1. Module structure / file layout
- Each domain module follows `model/ + service/ + endpoints/`.
- One file per endpoint handler in `endpoints/` (`get.rs`, `list.rs`), named after the operation.
- One file per response struct in `model/` (`summary.rs`, `details.rs`), registered in `model/mod.rs`
  with `pub mod <name>;`.
- Each `endpoints/mod.rs` builds the module's `Router` and registers routes; `server/src/main.rs`
  mounts all modules, so new routes need no change in `main.rs`.
- Integration tests live in `tests/api/<area>.rs`, one file per endpoint area.

## 2. Naming
- Functions and methods: `snake_case` verbs (`fetch`, `list`, `search`, `ingest`); the new method is
  `severity_summary`.
- Types: `PascalCase` with a `<Domain><Kind>` suffix (`AdvisorySummary`, `SbomDetails`,
  `PackageSummary`). The new type is `SeveritySummary`.
- Files: `snake_case`, named after the struct or operation (`summary.rs` -> `AdvisorySummary`,
  `severity_summary.rs` -> `SeveritySummary`).
- Services: `<Domain>Service` (`AdvisoryService`, `SbomService`).

## 3. Service method signatures
- Read methods take `&self`, domain arguments, and a trailing `tx: &Transactional<'_>`, e.g.
  `fetch(&self, id: Id, tx: &Transactional<'_>)`.
- They return `Result<T, Error>` (service error), and handlers convert to `AppError`.
- Shared filtering, pagination and sorting live in `common/src/db/query.rs`. Reuse those helpers
  instead of building ad-hoc queries.
- Entities come from the `entity` crate (`entity::advisory`, `entity::sbom`, `entity::sbom_advisory`)
  and are queried with SeaORM (`Entity::find()`, `.join(...)`, `.filter(...)`).

## 4. Error handling
- All handlers return `Result<T, AppError>` (`common/src/error.rs`; `AppError` implements
  `IntoResponse`).
- Fallible calls are wrapped with `.context("...")` to add a human-readable message.
- Missing entities map to a not-found `AppError` variant, which becomes HTTP 404 (as in
  `sbom/endpoints/get.rs` for an unknown SBOM ID).

## 5. Endpoint / API design
- Handlers are `async fn` taking Axum extractors: `State`/`Extension` for the service and DB, and
  `Path<Id>` for path IDs.
- Handler flow: extract params -> call service -> return the result as JSON (`Json<T>`).
- Single-resource responses return the struct directly. Only list endpoints use
  `PaginatedResults<T>` (`common/src/model/paginated.rs`), so the summary endpoint does NOT
  paginate.
- Routes are registered as `Router::new().route("/path", get(handler))`.
- Caching uses `tower-http` middleware configured in the route builders. Sibling routes'
  cache configuration is mirrored for consistency.
- Path style: `/api/v2/<resource>/{id}`, with lowercase kebab-case sub-resources.

## 6. Models / serialization
- Response structs derive `Serialize, Deserialize, Debug, Clone, PartialEq` and `utoipa::ToSchema`
  (for OpenAPI), matching `AdvisorySummary`/`SbomSummary`.
- Public structs and fields have `///` doc comments.

## 7. Imports
- Ordering: `std` first, then external crates (`axum`, `sea_orm`, `serde`), then workspace crates
  (`trustify_common`, `trustify_entity`), then `crate::`/`super::` imports.

## 8. Test patterns (sibling `tests/api/*.rs`)
- Integration tests hit a real PostgreSQL test database through the shared test context and
  fixtures.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)` /
  `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Test names use `snake_case`, describe the behavior, and are `async` tests (`#[tokio::test]` or
  the project's test-context macro).
- Each error case (404) gets its own test function.

### Skill guidance applied over sibling patterns (recorded conflicts)
- **Value-based assertions:** the tests deserialize the body into `SeveritySummary` and compare it
  to a whole expected value with `assert_eq!`. They do not stop at status or count checks.
- **Test documentation:** every test function gets a `///` doc comment, and non-trivial tests get
  `// Given / // When / // Then` sections, even where sibling tests have none.
- **Parameterization:** the four required tests differ in setup and assertions (a 404 path vs
  counted bodies), so the Meszaros heuristic says to use separate tests. No `rstest` is
  introduced. Sibling tests do not appear to use it either.

## Convention conflicts with the task description (flagged)
1. **Route location vs module prefix:** the task registers `GET /api/v2/sbom/{id}/advisory-summary`
   in `advisory/endpoints/mod.rs`, whose routes otherwise live under `/api/v2/advisory`. The plan
   follows the task, which names the path and file explicitly, and registers the full path in the
   advisory router. In a live run I would ask the user to confirm this.
2. **`server/src/main.rs` listed under Files to Modify with "no changes needed":** the plan leaves
   it unchanged, consistent with the auto-mount convention.
