# Discovered Conventions — TC-9208 (trustify-backend)

Sources: repo-backend.md "Key Conventions" plus the sibling files `package/endpoints/list.rs`, `package/model/summary.rs`, `sbom/endpoints/get.rs`, `advisory/endpoints/*`, `tests/api/advisory.rs`, `tests/api/sbom.rs` (sibling test patterns as quoted in the task), and CONVENTIONS.md at the repo root. In a live run, sibling details would be confirmed with `mcp__serena_backend__get_symbols_overview`.

## Module structure
- Each domain module uses the `model/ + service/ + endpoints/` layout.
- `model/mod.rs` and `endpoints/mod.rs` declare one submodule per file (`summary.rs`, `details.rs`, `list.rs`, `get.rs`).
- File names are short nouns or verbs describing the resource or operation (`list.rs`, `get.rs`, `summary.rs`), so `license_summary.rs` follows the pattern.

## Naming
- Response structs are named `<Entity><View>`: `PackageSummary`, `SbomSummary`, `SbomDetails`, `AdvisorySummary`. The new names `LicenseSummary` and `LicenseCategorySummary` follow this.
- Handlers are snake_case `verb_noun` functions (e.g. `list_packages`, `get_sbom`). The new handler is `get_license_summary`.
- Integration test files are named after the endpoint domain in `tests/api/<domain>.rs`. The new file is `package_license.rs`, as specified by the task.

## Error handling
- All handlers return `Result<T, AppError>`. `AppError` lives in `common/src/error.rs` and implements `IntoResponse`.
- Fallible calls are wrapped with `.context("...")`.
- Unknown IDs map to the `AppError` NotFound variant, which produces an HTTP 404 (pattern from `sbom/endpoints/get.rs`).

## API design
- Routes are registered in each module's `endpoints/mod.rs`. `server/main.rs` mounts the modules, and needs no change because the package module is already mounted.
- List endpoints return `PaginatedResults<T>`. Single-resource and aggregate endpoints return a plain `Json<T>`. The license summary is an aggregate, so it is **not** paginated.
- Filtering, pagination, and sorting go through the shared helpers in `common/src/db/query.rs`. Reuse them if any filtering is needed.
- Caching is configured with `tower-http` middleware in the route builders. The new route uses the same builder chain.
- Axum handles HTTP and SeaORM handles the DB. Joins use SeaORM entity relations (`package_license`, `sbom_package`).

## Import organization
- std imports first, then external crates (axum, sea_orm, serde, utoipa), then workspace crates (`common`, `entity`), then `crate::`/`super::`. This would be confirmed from `list.rs`.

## Test patterns (from siblings)
- Integration tests in `tests/api/` run against a real PostgreSQL test database through the shared test harness/context.
- The status check is `assert_eq!(resp.status(), StatusCode::OK)`.
- There is one `#[test]`/`#[tokio::test]` function per scenario, with snake_case descriptive names.
- Fixtures are SBOMs ingested through the shared helper before the request is made.
- Collections are checked with existence/count-only assertions:
  - `tests/api/advisory.rs`: `.filter(..).any(|_| true)` then `assert!(has_critical)`
  - `tests/api/sbom.rs`: `.filter(..).count()` then `assert!(matching > 0)`
- No parameterized-test mechanism (`rstest`, etc.) appears in the siblings.
- Sibling tests have no doc comments and no given-when-then comments.

## Conflicts between sibling patterns and the skill's quality guidance

Per SKILL.md Step 4 ("Skill guidance takes precedence over sibling patterns") and Step 7, the skill guidance wins in each case below. The conflict is recorded here and the sibling pattern is **not** adopted.

| # | Sibling pattern | Skill guidance | Decision |
|---|---|---|---|
| 1 | Existence-only assertions: `.filter().any(\|_\| true)` + `assert!(has_x)` in `advisory.rs`, `.filter().count()` + `assert!(n > 0)` in `sbom.rs` | Step 7, "Prefer value-based assertions over length-only checks": assert on actual values and key fields so failures show *what* changed | **Follow skill guidance.** New tests use `assert_eq!` against the full expected `LicenseSummary` (exact counts **and** exact sorted license identifier lists per category). No `.any()` or `> 0` checks. |
| 2 | No doc comments on test functions | Step 7, "Document every test function": a `///` line on every test, overriding sibling convention | **Follow skill guidance.** Every test gets a `///` doc comment. |
| 3 | No given-when-then structure comments | Step 7: add `// Given` / `// When` / `// Then` to non-trivial tests | **Follow skill guidance** for the tests with distinct setup, action, and assertion phases (all four have an ingest/setup phase). |
| 4 | No parameterized tests in siblings | Step 7: prefer parameterized tests, **but** do not introduce them if the project does not use them | **Follow the project pattern (no `rstest`).** The four tests also differ in setup and assertion shape (404 vs body), so the Meszaros heuristic would keep them separate anyway. This is not really a conflict, since the skill itself defers to the project here. |

Kept from siblings (no conflict): test file location and naming, the shared harness and DB setup, fixture ingestion helpers, `assert_eq!(resp.status(), StatusCode::OK)` for status checks, and one test function per scenario.

## Task vs. convention conflicts (would be flagged to the user)
- The task puts the route `/api/v2/sbom/{id}/license-summary` in the **package** module's `endpoints/mod.rs`, while `/api/v2/sbom/*` routes are otherwise registered by the sbom module. This follows the task, but the user is asked to confirm.
- The module convention puts DB queries in `service/`, but `package/service/mod.rs` is not in Files to Modify. The query goes in the handler, and the user is asked whether to move it into `PackageService`.
- The new endpoint is not documented in `docs/api.md`, which is out of scope. Flagged to the user as a recommended follow-up.
