# Conventions Discovered — TC-9208 (trustify-backend)

Sources: the repo structure and Key Conventions (repo-backend.md), sibling production files in `modules/fundamental/src/{package,sbom,advisory}/{model,endpoints}`, the sibling tests `tests/api/advisory.rs` and `tests/api/sbom.rs` (excerpts quoted in the task), and `CONVENTIONS.md` at the repo root (read in Step 4; its CI commands are used in Step 9).

## Module structure
- Each domain module follows `model/ + service/ + endpoints/`.
- Each submodule file is declared in its parent `mod.rs`, for example `pub mod summary;` in `model/mod.rs`. The new `pub mod license_summary;` follows this.
- File names are snake_case nouns describing the type or route: `summary.rs`, `details.rs`, `list.rs`, `get.rs`. `license_summary.rs` fits.

## Naming
- Model structs: `<Domain><Kind>`, such as `SbomSummary`, `AdvisoryDetails`, `PackageSummary`. The new struct is `LicenseSummary`, with a nested `LicenseCategorySummary`.
- Handler files are named after the action or resource (`list.rs`, `get.rs`). Handler functions use verb_noun names (`get_license_summary`).
- Test files are named after the resource under test (`tests/api/sbom.rs`, `advisory.rs`). The new file is `package_license.rs`, as the task specifies. Test functions use `test_<subject>_<behavior>` names.

## Error handling
- All handlers return `Result<T, AppError>` (`common/src/error.rs`, which implements `IntoResponse`).
- Fallible calls are wrapped with `.context("...")`.
- Not-found cases map to the `AppError` variant that produces 404, the same way `sbom/endpoints/get.rs` does.

## API design and registration
- Routes are registered in each module's `endpoints/mod.rs`. `server/src/main.rs` mounts the module routers.
- Paths are versioned: `/api/v2/<resource>[/{id}[/<sub-resource>]]`.
- Caching uses `tower-http` middleware configured in the endpoint route builders. The new route follows the sibling builder style.
- List endpoints return `PaginatedResults<T>`. The new endpoint is a single aggregate object, not a list, so it returns `Json<LicenseSummary>` without pagination, like `get.rs`.
- Query building uses SeaORM entities (`entity/src/*.rs`) and the shared helpers in `common/src/db/query.rs`. The aggregation is a plain filtered JOIN with no pagination or sorting, so those helpers are not needed.
- DB access normally goes in `service/`. In this task the service layer is out of scope (see plan.md).

## Test conventions (from sibling tests)
- Integration tests live in `tests/api/<resource>.rs` and run against a real PostgreSQL test database.
- HTTP status is checked with `assert_eq!(resp.status(), StatusCode::OK)` (and `StatusCode::NOT_FOUND` for errors).
- The response body is deserialized into the typed response struct before assertions.
- Sibling assertion style for collections checks existence or count only:
  - `advisory.rs`: `.filter(|a| a.severity == "Critical").any(|_| true)` then `assert!(has_critical, ...)`
  - `sbom.rs`: `.filter(|s| s.name.contains("openssl")).count()` then `assert!(matching > 0, ...)`
- The excerpts show no parameterized-test mechanism (`rstest`) in siblings.
- Siblings do not show doc comments or given-when-then sections on tests.

## Conflicts with the skill's built-in quality guidance

The skill says its own guidance takes precedence over sibling patterns. Each conflict below is recorded and the sibling pattern is **not** adopted.

| # | Sibling pattern | Skill guidance | Decision |
|---|---|---|---|
| 1 | Existence and count checks: `.filter(..).any(\|_\| true)` + `assert!(bool)`, `.filter(..).count()` + `assert!(n > 0)` | Step 7: prefer value-based assertions over length-only checks. Assert on actual values and key fields so failures show *what* changed. | **Follow the skill.** Use `assert_eq!` on the full deserialized `LicenseSummary` (or on each category's `count` and exact `licenses` vec) against an expected value. Do not use `.any(\|_\| true)` or `count() > 0`. |
| 2 | No doc comments on test functions | Step 7: every test function gets a `///` doc comment, regardless of siblings | **Follow the skill.** Add a one-line `///` to every test. |
| 3 | No given-when-then structure in tests | Step 7: non-trivial tests get `// Given` / `// When` / `// Then` comments | **Follow the skill** for the tests with separate setup, action and assertion phases (categorization, dedup, empty SBOM). The 404 test is close to trivial but still has an ingest-free setup and a request. Given/When/Then is kept there for consistency. |
| 4 | New public symbols in siblings may lack docs | Step 6: every new struct, enum and pub fn gets a doc comment | **Follow the skill.** Doc comments go on `LicenseSummary`, `LicenseCategorySummary`, `from_licenses`, the classifier and the handler. |

Kept from siblings (no conflict): test file location and naming, the real-DB integration setup and fixture/ingest helpers, `assert_eq!(resp.status(), StatusCode::...)` for status checks, typed response deserialization, and the `test_*` naming style.

Parameterized tests: the skill says not to introduce them if the project does not use them, and siblings show no `rstest`. The four required tests also differ in setup and assertions (Meszaros heuristic), so they stay as individual test functions. This agrees with the skill.

## Conflicts between the task and conventions
- No direct contradiction. The task's Implementation Notes explicitly ask to "review whether the assertion style above is the best pattern". That matches conflict #1 above, so the skill guidance is applied without blocking on the user.
- Minor structural deviation, flagged rather than silently resolved: siblings use `service/` for DB access, but `package/service/mod.rs` is not in Files to Modify. The query stays in the handler file unless the user approves extending the scope.
- The route `/api/v2/sbom/{id}/license-summary` is registered in the package module's `endpoints/mod.rs` (as the task specifies), while `/api/v2/sbom` routes normally belong to the sbom module. Follow the task and note the cross-module path in the PR description.
