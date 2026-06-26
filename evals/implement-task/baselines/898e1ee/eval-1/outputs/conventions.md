# Discovered Conventions (from sibling analysis)

## Step 0 -- Validate Project Configuration

Project Configuration validated in CLAUDE.md:
- Repository Registry: present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
- Jira Configuration: present, contains Project key `TC`, Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`

All required sections are present. Proceeding.

## Step 1.5 -- Description Digest Verification

No description digest comment provided. Warning logged:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

Proceeding with implementation normally (backward compatibility).

## Production Code Conventions (from sibling analysis)

### Module structure
- Each domain module follows the `model/ + service/ + endpoints/` structure (observed in `sbom/`, `advisory/`, `package/`).
- Models are split into separate files per concern: `summary.rs`, `details.rs` in each `model/` directory.
- Each `model/mod.rs` re-exports sub-modules via `pub mod <name>;`.

### Service patterns
- Services are named `<Entity>Service` (e.g., `SbomService`, `AdvisoryService`, `PackageService`).
- Service methods take `&self`, entity-specific parameters, and a `tx: &Transactional<'_>` parameter for transaction propagation.
- Common service methods follow `verb_noun` or bare `verb` naming: `fetch`, `list`, `search`, `ingest`.

### Endpoint patterns
- Framework: Axum for HTTP routing.
- Endpoint handlers live in separate files per operation: `list.rs`, `get.rs` within each `endpoints/` directory.
- Route registration happens in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern.
- Path parameters are extracted via `Path<Id>` extractor.
- All handlers return `Result<T, AppError>` with `.context()` for error wrapping (from `common/src/error.rs`).
- Response serialization is handled by Axum's `Json` extractor -- return the struct directly.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

### Error handling
- All error handling uses `Result<T, AppError>` pattern.
- Error wrapping uses `.context("descriptive message")` from the `anyhow` style, matching `common/src/error.rs`.
- 404 errors follow existing SBOM endpoint patterns for non-existent resources.

### Database / ORM
- SeaORM is used for database operations.
- Join tables (e.g., `sbom_advisory`, `sbom_package`) link entities in the `entity/` crate.
- Shared query helpers for filtering, pagination, and sorting are in `common/src/db/query.rs`.

### Naming conventions
- Files: lowercase snake_case (e.g., `severity_summary.rs`, `sbom_advisory.rs`).
- Structs: PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `AdvisorySummary`).
- Response structs include Serialize derive for JSON serialization.

### Import organization
- External crate imports first, then internal module imports.
- Entity references use the `entity` crate path (e.g., `entity::sbom_advisory`).

## Test Conventions (from sibling test analysis)

### Test location and organization
- Integration tests live in `tests/api/` directory, with one file per domain (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database (not mocks).

### Assertion patterns
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response body is deserialized and fields are checked individually.
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 responses.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test structure
- Tests use given-when-then structure for non-trivial cases.
- Setup involves creating test fixtures in the database.
- Each test function should have a documentation comment explaining what it verifies.

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root. In this simulation, we would read it using `mcp__serena_backend__read_file` or the Read tool. Any CI check commands found would be recorded for Step 9 verification. Since we cannot read the actual file, we note that it should be consulted for:
- CI check commands (formatting, linting, compilation)
- Code generation commands
- Additional project-specific conventions
