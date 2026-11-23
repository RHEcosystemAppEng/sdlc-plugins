# Conventions Discovered — TC-9208 (trustify-backend)

Sources: repo structure / Key Conventions (repo-backend.md); siblings `package/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs`, `package/model/summary.rs`; test siblings `tests/api/advisory.rs` and `tests/api/sbom.rs` (patterns quoted in the task); `CONVENTIONS.md` (would be read at the repo root for CI commands and extra rules).

## Module structure
- Each domain module uses `model/ + service/ + endpoints/`.
- New model types go in their own file under `model/` and are declared in `model/mod.rs` (`pub mod license_summary;`).
- New handlers go in their own file under `endpoints/` and are declared and registered in `endpoints/mod.rs`. `server/main.rs` mounts the modules and needs no change.

## Naming
- Files: snake_case, named after the resource or action (`list.rs`, `get.rs`, `summary.rs`, so `license_summary.rs`).
- Types: PascalCase with a `Summary` / `Details` suffix (`SbomSummary`, `PackageSummary`, so `LicenseSummary`, `LicenseCategorySummary`).
- Handler functions are named by HTTP action (`list`, `get`). Utility functions use `verb_noun`.
- Test files are named after the resource (`tests/api/<resource>.rs`). Test fns are snake_case and describe the behavior.

## Error handling
- Handlers return `Result<T, AppError>` (`common/src/error.rs`, which implements `IntoResponse`).
- Fallible calls are wrapped with `.context("...")`.
- A missing single resource returns the 404 variant of `AppError`, matching `get.rs` siblings.

## API / response design
- Routes use the `/api/v2/...` prefix and are registered in the module's `endpoints/mod.rs` route builder.
- List endpoints return `PaginatedResults<T>`. Single-object/aggregate endpoints (like this one) return `Json<T>` directly, so pagination doesn't apply to the summary.
- Caching middleware (`tower-http`) is configured in the route builders, and the new route copies the sibling config.
- Response structs derive serde (and `utoipa::ToSchema` if siblings do).
- Shared filtering, pagination, and sorting come from `common/src/db/query.rs`. Reuse these helpers instead of writing ad-hoc SQL.

## Data access
- SeaORM entities live in `entity/src/`. The JOIN uses `sbom_package` -> `package` -> `package_license`.
- Queries are scoped by SBOM id at the DB level.

## Test conventions (sibling)
- Integration tests in `tests/api/` run against a real PostgreSQL test database, using the shared test context, fixture ingestion, and HTTP client helpers from the sibling files.
- Status checks use `assert_eq!(resp.status(), StatusCode::OK)` (and `StatusCode::NOT_FOUND`).
- Responses are deserialized into the typed model struct before assertions.
- One `#[test]`/async test function per scenario. Siblings show no parameterized-test usage (no `rstest`).
- Collection assertions in siblings are existence-only:
  - `advisory.rs`: `.filter(..).any(|_| true)` then `assert!(has_critical)`
  - `sbom.rs`: `.filter(..).count()` then `assert!(matching > 0)`

## Conflicts between sibling patterns and skill guidance

| # | Sibling pattern | Skill guidance (Step 4 / Step 7) | Resolution |
|---|---|---|---|
| 1 | Existence-only assertions (`.filter().any(|_| true)` + `assert!(bool)`; `.filter().count()` + `assert!(n > 0)`) in `tests/api/advisory.rs` and `tests/api/sbom.rs` | "Prefer value-based assertions over length-only checks", and "Skill guidance takes precedence over sibling patterns" | **Follow the skill guidance. Do not adopt the sibling pattern.** New tests assert exact values with `assert_eq!`: the full `LicenseSummary` struct, or each category's `count` and exact sorted `licenses` vec. Conflict recorded here and in the PR description. |
| 2 | Sibling tests have no doc comments (assumed; none shown in the quoted patterns) | "Document every test function" with `///`, plus `// Given / // When / // Then` for non-trivial tests | **Follow the skill guidance.** Every new test gets a `///` doc comment and given-when-then sections. |
| 3 | No parameterized tests in siblings | Prefer parameterized tests, *unless* the project doesn't use them | **Follow the project.** No `rstest` is introduced. The four scenarios also have different setup and assertions, so the Meszaros heuristic favors separate tests anyway. |

Everything else from the siblings (file layout, fixture/setup helpers, naming, `assert_eq!(resp.status(), StatusCode::...)` status checks, typed deserialization) is adopted unchanged. The task itself says to follow sibling structure, setup, and naming but to "review whether the assertion style is the best pattern". It doesn't contradict a convention, so no user clarification is needed. The assertion-style conflict is settled by the skill's precedence rule.

## Other flags (no conflict, recorded for the reviewer)
- The route `/api/v2/sbom/{id}/license-summary` is registered in the package module, though `/api/v2/sbom` routes normally live in `sbom/endpoints/mod.rs`. Kept as specified, with a check for route collisions.
- The query lives in the handler because `package/service/mod.rs` is outside Files to Modify. Moving it into `PackageService` would be flagged for approval.
- `docs/api.md` probably needs the new endpoint documented but is out of scope, so it is flagged rather than edited.
