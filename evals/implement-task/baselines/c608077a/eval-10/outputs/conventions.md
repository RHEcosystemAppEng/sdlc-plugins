# Conventions from Sibling Analysis — TC-9208

Sources: `repo-backend.md` (Key Conventions plus the directory structure), the sibling test snippets quoted in the task's Implementation Notes (`tests/api/advisory.rs`, `tests/api/sbom.rs`), and the planned Serena inspection of `package/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs` and the `model/summary.rs` siblings.

## Production code conventions (adopted)

### Module structure
- Each domain module uses `model/ + service/ + endpoints/`. New files go in `package/model/` and `package/endpoints/`, one file per concept, registered in the matching `mod.rs`.
- Models are declared as `pub mod <name>;` in `model/mod.rs`. Endpoint handlers are declared as `mod <name>;` in `endpoints/mod.rs`, and routes are registered in that same file.
- `server/main.rs` mounts each module's router, so it needs no change for a new route inside an existing module.

### Naming
- Files: snake_case nouns (`summary.rs`, `details.rs`, `list.rs`, `get.rs`), so the new file is `license_summary.rs`.
- Response structs: `<Entity><Aspect>` in PascalCase (`SbomSummary`, `AdvisorySummary`, `PackageSummary`), so the new struct is `LicenseSummary`.
- Handlers: `verb_noun` (for example `list_packages`, `get_sbom`), so the new handler is `get_license_summary`.
- Routes: `/api/v2/<entity>` and `/api/v2/<entity>/{id}`, with sub-resources in kebab-case (`/license-summary`).

### Error handling
- Handlers return `Result<T, AppError>` (`common/src/error.rs`, which implements `IntoResponse`).
- Fallible DB calls are wrapped with `.context("...")`.
- A missing entity becomes the NotFound `AppError` variant, which maps to HTTP 404, as in `sbom/endpoints/get.rs`.

### API and response design
- List endpoints return `PaginatedResults<T>`. This endpoint is a single aggregate object, not a list, so it returns `Json<LicenseSummary>` directly, like the `get.rs` siblings. `PaginatedResults` is not used here.
- Shared filtering, pagination and sorting helpers live in `common/src/db/query.rs`. Reuse them if any apply. A plain JOIN filtered by SBOM id is expected to be enough.
- Caching: `tower-http` caching middleware is configured in the route builders. Copy whatever the sibling routes do.
- Frameworks: Axum extractors and SeaORM entities (`entity::package_license`, `entity::sbom_package`, `entity::sbom`).

### Imports
- Order: std, then external crates (axum, sea_orm, serde), then workspace crates (`common`, `entity`), then local `super::`/`crate::`. Match the grouping in `list.rs`.

## Test conventions

### Adopted from siblings
- Location: integration tests go in `tests/api/<area>.rs`, so the new file is `tests/api/package_license.rs`.
- They run against a real PostgreSQL test database, using the existing harness and fixture setup from `sbom.rs`/`advisory.rs`. No new test infrastructure.
- Status checks use `assert_eq!(resp.status(), StatusCode::OK)` (and `StatusCode::NOT_FOUND` for the 404 case).
- Test function names follow the sibling style, for example `test_<behavior>` or a descriptive snake_case name, whichever the siblings use.
- Requests use the same test client and setup/teardown as the siblings.

### Not adopted (conflicts with the skill's quality guidance)

| # | Sibling pattern | Where | Skill guidance | Resolution |
|---|---|---|---|---|
| 1 | Existence-only checks: `.filter(..).any(\|_\| true)` then `assert!(has_x)` | `tests/api/advisory.rs` | Step 7: "Prefer value-based assertions over length-only checks". Assert on actual values and key fields. | **Skill guidance wins.** Use `assert_eq!` on the whole deserialized `LicenseSummary`, or on each category's `count` and `licenses` vector. |
| 2 | Count-greater-than-zero checks: `.filter(..).count()` then `assert!(matching > 0)` | `tests/api/sbom.rs` | Same as #1. Count-only checks hide regressions and say nothing about *what* changed. | **Skill guidance wins.** Assert exact counts and exact sorted license lists, for example `assert_eq!(summary.permissive.licenses, vec!["Apache-2.0", "MIT"])`. |
| 3 | Siblings have no doc comments on test functions (assumed from the snippets) | `tests/api/*.rs` | Step 7: every test function gets a `///` doc comment, plus `// Given / // When / // Then` in non-trivial tests. | **Skill guidance wins.** Every new test gets a `///` line and given-when-then sections. |
| 4 | Parameterized tests: the siblings show no use of `rstest` | `tests/api/*.rs` | Step 7: parameterize repetitive cases, but do not introduce it if the project does not use it. | **Follow the project.** No `rstest`. The four test cases differ in setup and assertions anyway, so they stay as separate functions under the Meszaros heuristic. |

The skill's rule ("Skill guidance takes precedence over sibling patterns ... record the conflict but do not adopt the sibling pattern") resolves conflicts #1–#3, so they do not need a user decision. The task text also asks to "review whether the assertion style above is the best pattern" and says only structure, setup and naming must follow the siblings. That matches this resolution, so the task and the conventions do not conflict.

## Task-vs-convention conflicts needing user input
- None blocking.
- One thing to watch: the route `/api/v2/sbom/{id}/license-summary` uses the sbom path prefix but is registered in the **package** module's `endpoints/mod.rs`, as the task requires. Normally a module registers routes under its own prefix (`/api/v2/package`). The task is explicit, so the plan follows it. If the Step 4 inspection shows that Axum route merging would clash with the sbom module's `/api/v2/sbom/{id}` routes, this would be raised with the user.
