# Discovered Conventions — trustify-backend (TC-9208)

Sources: `repo-backend.md` Key Conventions, the sibling modules `sbom/`, `advisory/` and `package/` under `modules/fundamental/src/`, the sibling tests `tests/api/sbom.rs` and `tests/api/advisory.rs` (as quoted in the task), and the task Implementation Notes.

## Module structure
- Each domain module uses `model/ + service/ + endpoints/`.
- Each endpoint gets its own file in `endpoints/` (`list.rs`, `get.rs`), and `endpoints/mod.rs` registers the routes. `server/src/main.rs` mounts whole modules, so no change is needed there because the package module is already mounted.
- Each model type gets its own file in `model/` (`summary.rs`, `details.rs`), declared in `model/mod.rs`.

## Naming
- Files are snake_case nouns describing the resource or view (`summary.rs`, `license_summary.rs`).
- Structs are `<Domain><View>` (`SbomSummary`, `AdvisoryDetails`, `PackageSummary`). The new struct is `LicenseSummary`.
- Handler functions are named after the HTTP action or view (`list`, `get`).
- Integration test files are named after the resource (`tests/api/sbom.rs`), so the new one is `tests/api/package_license.rs`. Test functions are snake_case and descriptive.

## Error handling
- Handlers return `Result<T, AppError>` (`common/src/error.rs`, which implements `IntoResponse`).
- Fallible calls are wrapped with `.context("...")`.
- A missing single resource maps to a 404 through `AppError` (as in the `get.rs` siblings).

## API design / responses
- Axum handlers and SeaORM queries.
- List endpoints return `PaginatedResults<T>`. The new endpoint is a single aggregate object, not a list, so it returns `Json<LicenseSummary>` directly, matching the `get.rs` siblings.
- Shared filtering, pagination and sorting live in `common/src/db/query.rs`. They are reused if any filtering is needed (none is needed for this aggregate).
- Caching uses `tower-http` middleware configured in the endpoint route builders. The new route is registered with the same builder as `list`.

## Imports / module organisation
- Entities are imported from the `entity` crate (`entity::package_license`, `entity::sbom_package`, `entity::sbom`).
- Common types come from the `common` crate (`common::error::AppError`).

## Test patterns (from sibling tests)
- Integration tests in `tests/api/` run against a real PostgreSQL test DB, using the shared setup and fixture helpers.
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)`.
- Body assertions in the siblings check only existence or count:
  - `advisory.rs`: `.filter(..).any(|_| true)` followed by `assert!(has_critical, ...)`
  - `sbom.rs`: `.filter(..).count()` followed by `assert!(matching > 0, ...)`
- One test function per scenario. The quoted siblings show no evidence of `rstest` or other parameterisation.
- The quoted sibling tests have no documentation comments on test functions.

## Conflicts with the skill's built-in quality guidance

The skill's rule: when skill guidance conflicts with a sibling pattern, the skill guidance wins. The conflict is recorded, and the sibling pattern is not adopted.

| # | Sibling convention | Skill guidance (Step 7) | Decision |
|---|---|---|---|
| 1 | Existence and count assertions: `.filter().any(|_| true)` + `assert!(bool)`, and `.filter().count()` + `assert!(n > 0)` | Prefer value-based assertions over length-only or existence checks. Assert on the actual values so a failure shows *what* changed. | **Follow the skill.** The new tests use `assert_eq!` on the full deserialized `LicenseSummary` (or on each category's `count` and exact `licenses` vector). The sibling `.any()` / `count() > 0` style is **not** used. |
| 2 | Test functions have no doc comments | Every test function gets a `///` doc comment, and non-trivial tests get `// Given / // When / // Then` sections. | **Follow the skill.** All new tests get `///` docs and given-when-then comments. |
| 3 | No parameterised tests in the siblings | Prefer parameterised tests for repetitive cases, **but** do not introduce them if the project doesn't use them. | **Follow the project (the skill allows this).** No `rstest`. The four scenarios also differ in setup and assertions (Meszaros heuristic), so separate tests are correct anyway. |

Conventions that are kept: file and test naming, the DB test setup helpers, the `assert_eq!(resp.status(), StatusCode::...)` status check, and the module and registration structure.

## Task vs convention conflicts (would be raised with the user)
- **Route location**: the endpoint path is under `/api/v2/sbom/...`, but the task registers it in the **package** module's `endpoints/mod.rs`, while the SBOM routes are registered in `sbom/endpoints/mod.rs`. This follows the task as written, and the user is asked to confirm that the route nesting or prefix does not clash.
- **Service layer**: siblings put DB access in `service/`, but the task lists no service file. The plan keeps the query in the handler and asks the user whether `package/service/mod.rs` may be extended instead.
- No conflict on error handling: the task's "`AppError` with `.context()`" matches the convention.
