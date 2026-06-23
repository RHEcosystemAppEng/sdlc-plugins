# Discovered Conventions (from Sibling Analysis)

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md validated:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: present, contains Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention `mcp__<serena-instance>__<tool>`

All required sections are present. Proceeding.

## Step 1.5 -- Description Digest Verification

WARNING: No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Production Code Conventions

### Module structure
- Each domain module (sbom, advisory, package) follows a consistent `model/ + service/ + endpoints/` tri-directory structure under `modules/fundamental/src/`.
- Each sub-directory has a `mod.rs` that re-exports public types and registers sub-modules.

### Model conventions (from `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`)
- Model structs derive `Serialize, Deserialize, Debug, Clone`.
- Each model lives in its own file named after its role (e.g., `summary.rs`, `details.rs`).
- The parent `mod.rs` declares `pub mod <name>;` for each sub-module and re-exports the primary type.

### Service conventions (from `advisory/service/advisory.rs`, `sbom/service/sbom.rs`)
- Service structs are named `<Domain>Service` (e.g., `AdvisoryService`, `SbomService`).
- Methods follow the `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `ingest`).
- Method signatures accept `&self`, domain-specific ID parameters, and `tx: &Transactional<'_>` for database transaction context.
- Methods return `Result<T, AppError>` using the `AppError` enum from `common/src/error.rs`.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` pattern adapted via `AppError`.

### Endpoint conventions (from `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`)
- Handler functions are async and return `Result<Json<T>, AppError>`.
- Path parameters are extracted via `Path<Id>` (Axum extractor).
- Service calls are invoked on the service instance passed via Axum state.
- Route registration happens in each module's `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`.
- The `server/main.rs` mounts all module routers -- modules self-register their routes.

### Error handling
- All handlers use `Result<T, AppError>` with `.context()` wrapping.
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`.
- 404 responses are returned when an entity lookup fails (consistent with existing SBOM and advisory endpoints).

### Naming conventions
- Files: snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`)
- Types: PascalCase (e.g., `AdvisorySummary`, `SbomDetails`)
- Functions: snake_case verb_noun (e.g., `severity_summary`, `fetch`, `list`)
- Modules: snake_case matching the file name

### Import organization
- Standard library imports first, then external crates, then internal crate modules.

### Response types
- Single-entity endpoints return `Json<T>` directly.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- The new endpoint returns a single summary object, so it should return `Json<SeveritySummary>`.

## Test Conventions

### Test file conventions (from `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`)
- Integration tests live in `tests/api/` and test against a real PostgreSQL test database.
- Test functions follow the `test_<endpoint>_<scenario>` naming pattern (e.g., `test_list_advisories_filtered`, `test_get_sbom_not_found`).
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` for status code checks, followed by body deserialization and field-level assertions.
- Error cases: all endpoint test files include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Response validation: tests deserialize the JSON body and assert on specific field values (not just collection lengths).
- Each test file corresponds to a domain module (e.g., `advisory.rs` tests advisory endpoints, `sbom.rs` tests SBOM endpoints).
- The new test file `advisory_summary.rs` should follow this same pattern.

### CONVENTIONS.md
- A `CONVENTIONS.md` file exists at the repository root. Its contents would be read for CI check commands and additional project-level conventions. Since we cannot access the actual file in this eval, we note its presence and would follow any conventions found within it during real implementation.
