# Conventions discovered — TC-9208 (Step 4 convention conformance analysis)

Sources: `repo-backend.md` Key Conventions, `CONVENTIONS.md` (repo root, to be read), sibling production files (`package/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs`, `package/model/summary.rs`) and sibling tests (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`), plus the sibling snippets quoted in the task.

## Production code

### Module structure
- Each domain module uses `model/ + service/ + endpoints/`.
- New model types go in their own file under `model/` and are declared in `model/mod.rs` (`pub mod license_summary;`).
- Each module's `endpoints/mod.rs` registers routes; `server/src/main.rs` mounts modules.

### Naming
- Files: snake_case, named after the resource/feature (`summary.rs`, `details.rs`, `list.rs`, `get.rs`) -> `license_summary.rs`.
- Types: PascalCase with a domain prefix + role suffix (`SbomSummary`, `AdvisorySummary`, `PackageSummary`) -> `LicenseSummary`.
- Handlers: `verb_noun` -> `get_license_summary`.
- Routes: `/api/v2/<resource>[/{id}][/<sub-resource>]`.

### Error handling
- Handlers return `Result<T, AppError>`; errors wrapped with `.context("...")`.
- `AppError` (common/src/error.rs) implements `IntoResponse`; missing entity -> 404 via `AppError` (as in sibling `get.rs` handlers).

### Response types / APIs
- List endpoints return `PaginatedResults<T>`; this endpoint is a single aggregate object, so it returns `Json<LicenseSummary>` (like `get.rs`), not `PaginatedResults`.
- Shared filtering/pagination/sorting in `common/src/db/query.rs` (reuse if any helper applies).
- Caching configured via `tower-http` in route builders — replicate the sibling route builder configuration.
- SeaORM entities in `entity/src/`; JOIN through `sbom_package` and `package_license`.

## Test code

### Structure / setup / naming (FOLLOW siblings)
- Integration tests live in `tests/api/<resource>.rs` -> `tests/api/package_license.rs`.
- Tests hit a real PostgreSQL test database using the same fixture/context setup and data-ingestion helpers that `sbom.rs`/`advisory.rs` use.
- Status assertions: `assert_eq!(resp.status(), StatusCode::OK)` (and `StatusCode::NOT_FOUND` for the error case).
- Response body is deserialised into the typed response struct before assertions (siblings use `result.items`).
- Test names follow sibling naming style (snake_case describing the behaviour).
- Parameterized tests: siblings do not show `rstest` or table-driven tests, so none are introduced (and the four required cases have different setup/assertions anyway).

### Assertion style (sibling pattern — NOT followed)
- Siblings check existence only:
  - `advisory.rs`: `.iter().filter(|a| a.severity == "Critical").any(|_| true)` then `assert!(has_critical, ...)`
  - `sbom.rs`: `.iter().filter(|s| s.name.contains("openssl")).count()` then `assert!(matching > 0, ...)`

## Conflicts with the skill's built-in quality guidance

The skill says: **"Skill wins over sibling patterns"** — when a sibling pattern conflicts with built-in quality guidance, follow the skill and record the conflict (binds Steps 6 and 7).

| # | Area | Sibling pattern | Skill guidance | Resolution |
|---|---|---|---|---|
| 1 | Assertion style | Existence checks: `.filter().any(\|_\| true)` + `assert!(bool)`; `.filter().count()` + `assert!(n > 0)` | Step 7: "Prefer value-based assertions over length-only checks" — assert on actual values/key fields so failures show *what* changed | **Skill wins.** Use `assert_eq!` on the full `LicenseSummary` (or on each category's `count` and exact `licenses` vector). No `.any()` / `> 0` checks. |
| 2 | Test documentation | Sibling tests are not shown to carry doc comments | Step 7: "Document every test function" with `///`; add `// Given / // When / // Then` for non-trivial tests | **Skill wins.** Every test gets a `///` doc line; non-trivial tests get given-when-then comments. |
| 3 | Doc comments on new symbols | Not evident in siblings | Step 6: every new struct/public fn needs a doc comment | **Skill wins.** `LicenseSummary`, `LicenseCategory`, `classify`, `from_licenses`, `get_license_summary` documented. |
| 4 | Defensive access | n/a | Step 6: guard data crossing module boundaries | Treat nullable license values from `package_license` defensively (`Option` handled, no `unwrap`). |

Retained from siblings (no conflict): file location, fixture/DB setup, test naming, `assert_eq!(resp.status(), StatusCode::...)` status checks, no parameterized tests.

No conflict between the task description and established conventions was found (the task itself invites reviewing the assertion style), so no user escalation is required; the conflicts above are recorded per the skill rule and would be noted in the PR description.
