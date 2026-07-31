# Discovered Conventions (from Sibling Analysis)

## Production Code Conventions

### Migration pattern (from `m0001_initial/mod.rs`)
- Each migration lives in its own directory under `migration/src/` with a `mod.rs` file
- Directory naming follows `m<NNNN>_<descriptive_name>/` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- Migrations implement SeaORM's `MigrationTrait` with `up` and `down` methods
- The `up` method performs the forward migration; `down` reverses it
- Migrations are registered in `migration/src/lib.rs` in the `migrations()` function's `vec![]`
- Registration order in `vec![]` follows sequential numbering

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)

### Module structure
- Domain modules follow `model/ + service/ + endpoints/` structure
- Each module's `endpoints/mod.rs` registers routes
- `server/main.rs` mounts all modules

### Naming conventions
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`, `fetch`, `list`, `ingest`)
- Entity files are named after the domain object in snake_case (e.g., `advisory.rs`, `sbom.rs`)

### Database conventions
- SeaORM for database access
- Column operations use SeaORM's `TableAlterStatement` API
- Nullable columns use `.null()` in column definitions
- Column types: `.string()` for text, enum types for constrained values

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers (filtering, pagination, sorting) in `common/src/db/query.rs`

## Test Conventions

### Test location
- Integration tests in `tests/api/` directory
- Test files named after the domain entity (e.g., `advisory.rs`, `sbom.rs`)

### Assertion style
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Tests hit a real PostgreSQL test database

### Test naming
- Tests follow `test_<entity>_<scenario>` pattern (e.g., tests in `advisory.rs` for advisory endpoints)

## CONVENTIONS.md

The repository has a `CONVENTIONS.md` file at the root. CI check commands and code generation commands would be extracted from it during Step 4 for use in Step 9's CI verification.
