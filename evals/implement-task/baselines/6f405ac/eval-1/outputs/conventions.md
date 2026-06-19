# Conventions Discovered from Sibling Analysis

## Step 0 -- Validate Project Configuration

Project Configuration validated in `CLAUDE.md`:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, custom fields
- Code Intelligence: present with tool naming convention `mcp__serena_backend__<tool>` and rust-analyzer

## Step 1 -- Parse Jira Task

Parsed fields:
- Repository: trustify-backend
- Target Branch: main
- Bookend Type: none
- Target PR: none
- Dependencies: none
- GitHub Issue custom field: customfield_10747 (not populated)
- Git Pull Request custom field: customfield_10875
- Jira web URL: (would be fetched from API, e.g. https://redhat.atlassian.net/browse/TC-9201)

## Step 1.5 -- Verify Description Integrity

> WARNING: No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## CONVENTIONS.md Lookup

A `CONVENTIONS.md` file exists at the repository root (`trustify-backend/CONVENTIONS.md`). Would read and follow its conventions. No specific CI check commands or code generation commands are detailed in the repo-backend.md fixture, so standard `cargo build` / `cargo test` / `cargo clippy` checks would be run as fallback.

## Production Code Conventions (from sibling analysis)

### Endpoint handler conventions (from `endpoints/get.rs`, `endpoints/list.rs` in advisory/ and sbom/)
- **Framework**: Axum for HTTP routing, handlers are async functions
- **Path extraction**: Use `Path<Id>` extractor for path parameters (e.g., `Path(id): Path<Id>`)
- **Return type**: All handlers return `Result<Json<T>, AppError>` where `T` is the response model
- **Error handling**: Use `.context("descriptive message")` wrapping on fallible operations; return `AppError` (defined in `common/src/error.rs`) which implements `IntoResponse`
- **Service invocation**: Handlers receive the service via Axum state extraction, call a service method, and wrap the result in `Json()`
- **Response types**: Single-resource endpoints return `Json<DetailStruct>`; list endpoints return `Json<PaginatedResults<SummaryStruct>>`

### Route registration conventions (from `endpoints/mod.rs` in advisory/ and sbom/)
- **Pattern**: `Router::new().route("/path", get(handler_function))` chaining
- **Mount point**: Each module registers routes under its own prefix (e.g., `/api/v2/advisory`, `/api/v2/sbom`)
- **Auto-mounting**: `server/src/main.rs` mounts all module routers; no changes needed there for new routes within existing modules

### Model struct conventions (from `model/summary.rs`, `model/details.rs` in advisory/ and sbom/)
- **Module registration**: Each model file is registered via `pub mod <name>;` in `model/mod.rs`
- **Derive macros**: Model structs derive `Serialize`, `Deserialize`, and likely `Debug`, `Clone`
- **Naming**: Response structs follow `<Entity><Purpose>` naming (e.g., `AdvisorySummary`, `SbomDetails`)
- **Fields**: Use standard Rust types; severity is represented as a field on `AdvisorySummary`

### Service conventions (from `service/advisory.rs`, `service/sbom.rs`)
- **Method signature**: Service methods take `&self`, domain-specific ID parameter, and `tx: &Transactional<'_>` for database transaction context
- **Naming**: Methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Error handling**: Methods return `Result<T, anyhow::Error>` or equivalent with `.context()` wrapping
- **Database access**: Use SeaORM for queries; join tables like `sbom_advisory` are in `entity/src/`

### Module structure conventions
- **Directory layout**: Each domain module follows `model/ + service/ + endpoints/` structure
- **mod.rs files**: Each subdirectory has a `mod.rs` that re-exports or registers submodules
- **Entity layer**: Database entities live in `entity/src/` with SeaORM definitions

### Error handling conventions
- **Error type**: `AppError` enum in `common/src/error.rs`, implements `IntoResponse`
- **Wrapping**: Use `.context("message")` from anyhow for adding context to errors
- **404 pattern**: Return appropriate HTTP status when entity not found, consistent with existing SBOM endpoints

### Import organization
- Standard library imports first, then external crates, then internal modules (Rust convention)

## Test Conventions (from sibling test analysis)

### Test file conventions (from `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`)
- **Location**: Integration tests live in `tests/api/` directory
- **Test database**: Tests hit a real PostgreSQL test database (not mocked)
- **Assertion style**: Use `assert_eq!(resp.status(), StatusCode::OK)` for status checks, followed by body deserialization and field-level assertions
- **Response validation**: Validate specific field values, not just collection lengths
- **Error cases**: Include 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: Follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Test organization**: Grouped by feature/endpoint within a single test file
- **Documentation**: Each test function should have a `///` doc comment explaining what it verifies (AI-generated standard)
- **Structure**: Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- **Parameterized tests**: Not explicitly indicated in sibling test files from the repo structure; individual test functions are the default pattern
