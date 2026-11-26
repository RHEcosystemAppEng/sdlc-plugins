# Discovered Conventions — TC-9208 (trustify-backend)

Sources: the sibling files named in the task and repo structure: `package/endpoints/list.rs`, `sbom/endpoints/{list,get}.rs`, `advisory/endpoints/{list,get}.rs`, `package/model/summary.rs`, `sbom/model/summary.rs`, `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`. Also the repo "Key Conventions" and `CONVENTIONS.md` at the repo root. Under the binding convention list from Step 4, these drive Steps 6 and 7.

## Module structure
- Every domain module uses the `model/ + service/ + endpoints/` layout. Each model and each endpoint goes in its own file, registered in that directory's `mod.rs` (`pub mod <name>;`).
- `endpoints/mod.rs` registers the module's routes, and `server/main.rs` mounts every module's routes.
- Model files are named after the shape they hold (`summary.rs`, `details.rs`). Following that, the new file is `license_summary.rs`.

## Naming
- Structs use `<Entity><Shape>` names (`SbomSummary`, `AdvisoryDetails`, `PackageSummary`). New structs: `LicenseSummary` and `LicenseCategorySummary`.
- Handler files are named after the operation (`list.rs`, `get.rs`). Handler functions use the verb_noun pattern, so the new one is `get_license_summary`.
- Routes are `/api/v2/<resource>[/{id}]` with kebab-case sub-resources (`license-summary`).

## Error handling
- Handlers return `Result<T, AppError>`, where `AppError` comes from `common/src/error.rs` and implements `IntoResponse`.
- Fallible database calls are wrapped with `.context("...")`.
- A missing resource maps to an `AppError` NotFound variant, which produces a 404. The pattern is in `sbom/endpoints/get.rs`.

## API / response design
- List endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`), filtered, paginated, and sorted through `common/src/db/query.rs`.
- Single-resource endpoints return `Json<T>`. The new endpoint returns one aggregate object, so it follows the `get.rs` single-object style rather than pagination.
- Model structs derive serde `Serialize`/`Deserialize` and a utoipa schema, and handlers carry `#[utoipa::path]` annotations.
- Caching is configured in the endpoint route builders with tower-http. The new route copies the sibling configuration.

## Data access
- Data access uses SeaORM entities from the `entity` crate. Join tables are `sbom_package` and `package_license`.
- Queries are scoped at the database (filter by id); results are not filtered in memory.

## Test conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`)
- Tests are integration tests in `tests/api/<resource>.rs`, one file per resource. The new file is `tests/api/package_license.rs`.
- They run against a real PostgreSQL test database, with data set up through the ingestion and fixture helpers the siblings use.
- Status is checked first, with `assert_eq!(resp.status(), StatusCode::OK)` (or `NOT_FOUND`).
- Response bodies are deserialized into the typed model struct (for example `PaginatedResults<AdvisorySummary>`) and assertions run on fields.
- Test names are `snake_case` and describe the behaviour.
- Siblings show no use of parameterized tests (`rstest`), so none are introduced (see below).
- **Assertion style in siblings:** existence-only checks, such as `.filter(..).any(|_| true)` with `assert!(has_x)`, and `.filter(..).count()` with `assert!(matching > 0)`.

## Conflicts with the skill's built-in quality guidance

The rule (SKILL.md Step 4 and Step 7): skill guidance takes precedence over sibling patterns. Each conflict is recorded, and the sibling pattern is not adopted.

| # | Sibling pattern | Skill guidance | Resolution |
|---|---|---|---|
| 1 | Existence-only assertions: `.filter(..).any(|_| true)` + `assert!(has_critical)` (advisory.rs) and `.filter(..).count()` + `assert!(matching > 0)` (sbom.rs). These say nothing about which values came back. | Step 7: "Prefer value-based assertions over length-only checks". Assert on actual values and key fields so failures show *what* changed. | **Follow the skill.** New tests compare the whole deserialized `LicenseSummary` (or each category's `count` and exact `licenses` vector) with `assert_eq!` against an expected value. No `.any(|_| true)` or `> 0` checks. |
| 2 | Sibling tests have no doc comments. | Step 7: "Document every test function" with `///`, plus `// Given / // When / // Then` in non-trivial tests. This overrides sibling conventions for documentation specifically. | **Follow the skill.** Every test gets a one-line `///` doc comment, and the non-trivial tests get given-when-then sections. |
| 3 | Siblings do not use parameterized tests. | Step 7: prefer parameterized tests, but "if the sibling test analysis shows the project does not use parameterized tests, do not introduce them." | **Follow the sibling pattern.** The skill defers here explicitly. The four tests also differ in setup and assertions (Meszaros heuristic), so separate tests are right anyway. |

Retained sibling conventions (they do not conflict): test file placement and naming, real-database setup and fixture helpers, the `assert_eq!(resp.status(), StatusCode::...)` status check, typed deserialization of response bodies, and snake_case test names.

## Task vs convention conflicts flagged to the user (not silently resolved)
- A route under the `/api/v2/sbom/` prefix is placed in the package module, while the `sbom` module owns that prefix. The plan follows the task and asks the user to confirm.
- The module pattern expects query logic in `service/`, but `package/service/mod.rs` is outside Files to Modify. The plan keeps the query in the handler and asks whether to extend `PackageService`.
- The convention says list endpoints return `PaginatedResults`. This endpoint returns an aggregate rather than a list, so returning `Json<LicenseSummary>` is not a violation. It is noted for reviewers.
