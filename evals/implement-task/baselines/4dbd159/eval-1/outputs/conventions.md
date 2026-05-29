# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceeding.

## Step 1 -- Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **Jira ID**: TC-9201
- **Target PR**: not present (default flow -- new branch and PR)
- **Bookend Type**: not present (normal implementation)
- **Dependencies**: None

## CONVENTIONS.md Lookup

The repository has a `CONVENTIONS.md` file at root. In a real execution, we would read it via `mcp__serena_backend__list_dir` or `Read` at `./CONVENTIONS.md`. For this eval, we note that the repository structure document lists it at `trustify-backend/CONVENTIONS.md`. We would follow all conventions found there and extract any CI check commands for Step 9.

## Production Code Conventions (from sibling analysis)

### Endpoint conventions (from `modules/fundamental/src/advisory/endpoints/`)

Siblings analyzed: `get.rs`, `list.rs`, `mod.rs`

- **Route registration**: Routes are registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` chaining pattern
- **Path parameter extraction**: Handlers use Axum's `Path<Id>` extractor as a function parameter
- **Service invocation**: Handlers call the corresponding service method (e.g., `AdvisoryService::fetch()`) passing the extracted ID and a `Transactional` reference
- **Return type**: All handlers return `Result<Json<T>, AppError>` where `T` is the response struct
- **Error wrapping**: Errors use `.context("descriptive message")` from anyhow, then convert to `AppError`
- **Auto-mounting**: `server/main.rs` auto-mounts all module routes; no manual registration needed there

### Model conventions (from `modules/fundamental/src/advisory/model/`)

Siblings analyzed: `summary.rs`, `details.rs`, `mod.rs`

- **Module registration**: New model modules must be registered in `model/mod.rs` via `pub mod <module_name>;`
- **Derive macros**: Model structs derive `Serialize, Deserialize, Debug, Clone` (and likely `utoipa::ToSchema` for OpenAPI)
- **Field naming**: Snake_case fields matching database column names
- **Documentation**: Structs have doc comments describing their purpose

### Service conventions (from `modules/fundamental/src/advisory/service/advisory.rs`)

Siblings analyzed: `advisory.rs` (existing methods `fetch`, `list`, `search`)

- **Method signature pattern**: `pub async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`) -- new method should be `severity_summary`
- **Database access**: Methods use SeaORM entity queries with the transactional context
- **Error handling**: Service methods return `Result<T, AppError>` with `.context()` wrapping on database errors

### General patterns

- **Framework**: Axum for HTTP routing, SeaORM for database ORM
- **Module structure**: Each domain follows `model/ + service/ + endpoints/` triple
- **Error type**: `AppError` from `common/src/error.rs`, implements `IntoResponse`
- **List responses**: Use `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering/pagination/sorting from `common/src/db/query.rs`

## Test Conventions (from sibling test analysis)

Siblings analyzed: `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` for success cases, `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases
- **Response validation**: Tests deserialize the response body into the expected struct and assert on specific field values (not just collection lengths)
- **Error cases**: All endpoint test files include at least one 404 test for non-existent resources
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_not_found`)
- **Test setup**: Tests hit a real PostgreSQL test database with seeded fixture data
- **Integration test location**: All API integration tests live in `tests/api/` directory
- **File naming**: Test files match the domain module name (e.g., `advisory.rs` tests advisory endpoints)
- **Parameterized tests**: No evidence of `#[rstest]` usage in sibling API tests -- individual test functions are used

## Cross-Section Reference Consistency

Checked all entity references across Files to Modify, Files to Create, and Implementation Notes:

- **AdvisoryService**: Files to Modify lists `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also references `modules/fundamental/src/advisory/service/advisory.rs` -- CONSISTENT
- **AdvisorySummary**: Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field -- CONSISTENT with repo structure
- **sbom_advisory join table**: Implementation Notes references `entity/src/sbom_advisory.rs` -- CONSISTENT with repo structure
- **Endpoint registration**: Files to Modify lists `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes also references it -- CONSISTENT

No cross-section reference mismatches detected.
