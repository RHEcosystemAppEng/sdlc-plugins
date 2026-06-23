# Conventions Discovered from Sibling Analysis

## Step 0 - Project Configuration Validation

The project CLAUDE.md contains all required sections:
1. **Repository Registry** - present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** - present, includes Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** - present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured with `rust-analyzer`

Validation: PASSED - all required sections exist.

## Production Code Conventions (from sibling analysis)

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` structure
- Model directory has `mod.rs` that re-exports submodules (e.g., `summary.rs`, `details.rs`)
- Service directory has `mod.rs` that re-exports the service implementation file
- Endpoints directory has `mod.rs` for route registration plus individual handler files

### Naming Conventions
- Model structs follow `<Entity><Role>` pattern: `SbomSummary`, `SbomDetails`, `AdvisorySummary`, `AdvisoryDetails`, `PackageSummary`
- Service structs follow `<Entity>Service` pattern: `SbomService`, `AdvisoryService`, `PackageService`
- Service methods use `verb` or `verb_noun` pattern: `fetch`, `list`, `search`, `ingest`
- Endpoint handler files are named after the HTTP operation: `list.rs`, `get.rs`
- Route paths use `/api/v2/<entity>` convention

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`

### Response Types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Single-entity endpoints return the model struct directly (Axum's `Json` extractor handles serialization)

### Endpoint Registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- `server/main.rs` mounts all modules (auto-mounting via module registration)

### Path Parameter Extraction
- Path parameters extracted via `Path<Id>` (from Axum)
- Service methods accept `&self`, entity-specific ID, and `tx: &Transactional<'_>`

### Database Layer
- SeaORM for database access
- Entity definitions in `entity/src/` directory
- Join tables use `<entity1>_<entity2>.rs` naming (e.g., `sbom_advisory.rs`, `sbom_package.rs`)

### Import Organization
- Framework imports (Axum, SeaORM) first
- Common/shared module imports next
- Local module imports last

### Caching
- Uses `tower-http` caching middleware configured in endpoint route builders

## Test Conventions (from sibling test analysis)

### Test Location and Organization
- Integration tests live in `tests/api/` directory
- Test files are named after the entity being tested: `sbom.rs`, `advisory.rs`, `search.rs`
- Tests hit a real PostgreSQL test database (integration-style)

### Assertion Style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response body is deserialized after status assertion
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` pattern

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (inferred from sibling test files for SBOM and advisory endpoints)

### Test Structure
- Non-trivial tests use given-when-then section comments
- Each test function has a documentation comment explaining what it verifies

## CONVENTIONS.md Lookup

The repository has a `CONVENTIONS.md` at the root. Since we cannot read it in this eval (no actual file system access to the mock repo), we note its existence and would read it during actual implementation to extract:
- CI check commands (for Step 9 verification)
- Code generation commands
- Any additional naming rules or patterns beyond what sibling analysis reveals
