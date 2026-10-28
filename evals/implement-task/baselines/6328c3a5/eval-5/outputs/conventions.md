# Conventions Discovered from Sibling Analysis

## Source

Primary sibling: `migration/src/m0001_initial/mod.rs` (the only existing migration module)
Additional sources: repository Key Conventions section, entity definitions, test patterns

## Migration Conventions

### Directory and file naming
- Each migration lives in its own subdirectory under `migration/src/`
- Directory naming pattern: `m<NNNN>_<snake_case_description>/` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- Each migration directory contains a single `mod.rs` file

### Module structure
- Implements `MigrationTrait` from SeaORM
- Exports a `Migration` struct
- Must implement both `up()` and `down()` async methods
- `up()` applies the schema change
- `down()` reverses it for rollback

### Registration pattern
- Each migration module is declared with `mod m<NNNN>_<name>;` in `migration/src/lib.rs`
- The migration is registered in the `migrations()` function's `vec![]` by adding `Box::new(m<NNNN>_<name>::Migration)`
- Migrations are listed in sequential order

### Schema operations
- Use SeaORM's `TableAlterStatement` for column changes (add, drop, modify)
- Use SeaORM's `TableCreateStatement` for new tables
- Reference entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for table and column identifiers
- Column definitions use `ColumnDef::new(...)` with chained type and constraint methods

## General Code Conventions

### Framework
- **HTTP**: Axum
- **ORM**: SeaORM
- **Database**: PostgreSQL

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` enum defined in `common/src/error.rs`

### Module pattern
- Domain modules follow `model/ + service/ + endpoints/` structure
- Each module's `endpoints/mod.rs` registers routes
- `server/main.rs` mounts all modules

### Response types
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Testing
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Test files named after the domain entity (e.g., `advisory.rs`, `sbom.rs`)

### Naming
- Snake case for Rust identifiers (functions, variables, modules)
- PascalCase for types, structs, enums
- Module directories use snake_case

## Skill Guidance Overrides

Per implement-task skill Step 7:
- **Value-based assertions** preferred over length-only checks (overrides sibling patterns if they differ)
- **Documentation comments** required on every new public symbol and test function (regardless of sibling practice)
- **Given-when-then comments** required in non-trivial test bodies
