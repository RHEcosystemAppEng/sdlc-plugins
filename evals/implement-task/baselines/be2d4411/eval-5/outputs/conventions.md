# Conventions Discovered from Sibling Analysis

## Source: Repository Structure and Key Conventions (repo-backend.md)

### Framework Conventions
- **HTTP Framework**: Axum for all HTTP endpoints
- **ORM**: SeaORM for all database operations and migrations
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure

### Migration Conventions (from sibling: `m0001_initial/mod.rs`)
- **File location**: Each migration lives in its own subdirectory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Module file**: Each migration directory contains a `mod.rs` file implementing `MigrationTrait`
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding the module declaration and a `Box::new(module::Migration)` entry to the `migrations()` function's `vec![]`
- **Trait implementation**: Uses `#[async_trait::async_trait]` for the async `MigrationTrait` implementation
- **Name derivation**: Uses `#[derive(DeriveMigrationName)]` to automatically derive the migration name from the module path
- **Enum identifiers**: Uses `#[derive(DeriveIden)]` enum to define table and column identifiers for use in schema operations

### Error Handling Conventions
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`

### Naming Conventions
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- Migration modules follow `m<number>_<description>` naming pattern

### Endpoint Conventions
- Each module's `endpoints/mod.rs` registers routes
- `server/main.rs` mounts all modules
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`

### Entity Conventions
- Entity files live in `entity/src/` with one file per database table
- SeaORM entities define the column mappings and relationships

### Testing Conventions
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Test files are organized by domain entity (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)

### Query Conventions
- Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- Connection pool management via `common/src/db/limiter.rs`

## Source: CONVENTIONS.md (repository root)

The repository has a `CONVENTIONS.md` file at the root. In a real implementation, this file would be read to extract:
- CI check commands for verification in Step 9
- Code generation commands
- Additional project-specific conventions

## Applied Conventions for This Task

1. **Migration file naming**: `m0002_drop_advisory_status/mod.rs` follows the `m<number>_<description>/mod.rs` pattern from `m0001_initial/mod.rs`
2. **Migration registration**: Adding to `lib.rs` follows the exact pattern of `m0001_initial` registration
3. **SeaORM idioms**: Using `Table::alter()`, `ColumnDef::new()`, `DeriveIden` enum, and `DeriveMigrationName` derive macro as established by the existing migration
4. **Scope containment**: Only modifying `migration/src/lib.rs` and creating `migration/src/m0002_drop_advisory_status/mod.rs` -- no unrelated changes
