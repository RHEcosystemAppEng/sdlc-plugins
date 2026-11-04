# Discovered Conventions — TC-9208

Sources: sibling production files in `modules/fundamental/src/{package,sbom,advisory}/`, sibling tests `tests/api/sbom.rs` and `tests/api/advisory.rs`, the repo Key Conventions, and `CONVENTIONS.md` at the repo root (read for CI commands).

## Module structure
- Each domain module is laid out as `model/` + `service/` + `endpoints/`.
- Each new model type gets its own file under `model/` (e.g. `summary.rs`, `details.rs`) and is exposed through `pub mod` in `model/mod.rs`.
- Each new handler gets its own file under `endpoints/` (e.g. `list.rs`, `get.rs`). Routes are registered in `endpoints/mod.rs`, and `server/main.rs` mounts the module routers.

## Naming
- Files and modules are snake_case and named after the resource or view (`summary.rs`, `license_summary.rs`).
- Response structs are PascalCase with a `Summary`/`Details` suffix (`SbomSummary`, `AdvisorySummary`, `PackageSummary`), so the new struct is `LicenseSummary`.
- Handler functions use short verb names that match the file's role (`list`, `get`).
- Routes have the form `/api/v2/<resource>[/{id}[/<sub-resource>]]`, kebab-case.

## Error handling
- Every handler returns `Result<T, AppError>` (`common/src/error.rs`, which implements `IntoResponse`).
- Fallible DB calls are wrapped with `.context("...")`.
- A missing resource maps to an `AppError` not-found variant, which becomes a 404 (pattern in `sbom/endpoints/get.rs`).

## API / response design
- List endpoints return `PaginatedResults<T>`. Single-resource and aggregate endpoints return a plain `Json<T>`, so the license summary returns a plain object, as the API Changes contract specifies.
- Shared filter, pagination and sort helpers live in `common/src/db/query.rs`. They are not needed here because the endpoint has no pagination.
- Caching is configured with `tower-http` middleware in the route builders, and the new route copies the sibling caching config.
- DB access normally goes through the module service (`PackageService`).

## Tests (from sibling integration tests)
- Location: `tests/api/<resource>.rs`. Tests hit a real PostgreSQL test DB.
- Status checks use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`.
- Setup, client construction and fixture ingestion reuse the shared helpers that `sbom.rs` and `advisory.rs` use.
- Test names are snake_case and describe the behavior.
- Collection assertions in the siblings check only that a matching item exists:
  - `advisory.rs`: `.filter(|a| a.severity == "Critical").any(|_| true)` then `assert!(has_critical)`
  - `sbom.rs`: `.filter(...).count()` then `assert!(matching > 0)`
- The sibling tests show no parameterized test mechanism (no `rstest`).
- The sibling tests show no doc comments on test functions.

## Conflicts with the skill's built-in quality guidance

| # | Sibling pattern | Skill guidance | Resolution |
|---|---|---|---|
| 1 | Existence checks: `.filter(..).any(\|_\| true)` + `assert!(bool)`, and `.filter(..).count()` + `assert!(n > 0)` | Step 7: "Prefer value-based assertions over length-only checks", meaning assert on actual values and key fields | **Follow the skill guidance.** The new tests use `assert_eq!` on the full expected `LicenseSummary` or on each category's `count` and `licenses` vector. The sibling `.any()` / `count() > 0` style is not adopted. The deviation is recorded here and in the PR/Jira comment. |
| 2 | Test functions have no doc comments | Step 7: "Document every test function" with `///`, plus `// Given / // When / // Then` sections in non-trivial tests | **Follow the skill guidance.** Every new test gets a one-line `///` doc comment, and the non-trivial tests get given-when-then section comments. |
| 3 | No parameterized tests in siblings | Step 7: prefer parameterized tests for repetitive cases, but do not introduce them if the project does not use them | **No conflict in practice.** The project does not use `rstest`, so none is introduced. The four required tests also differ in setup and assertions, so by the Meszaros heuristic they would be separate tests anyway. |

Conventions kept from the siblings (no conflict): file location and naming, shared test setup and fixture helpers, `assert_eq!(resp.status(), StatusCode::...)` for status checks, `Result<T, AppError>` with `.context()`, and route registration in `endpoints/mod.rs`.

## Task vs convention conflicts
- None blocking. The Implementation Notes ask the reviewer to "review whether the assertion style above is the best pattern", which is consistent with resolution #1.
- Minor point: siblings put DB queries in `service/`, but `package/service/mod.rs` is not in Files to Modify. The query is kept in the handler file, and the service-layer placement is flagged to the user as an optional out-of-scope change.
