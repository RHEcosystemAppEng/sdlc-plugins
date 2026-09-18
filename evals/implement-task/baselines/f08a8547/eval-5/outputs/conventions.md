# Conventions Discovered from Sibling Analysis

## Source of Conventions

Conventions derived from analyzing:
- `migration/src/m0001_initial/mod.rs` (sibling migration)
- Repository Key Conventions section
- `CONVENTIONS.md` at repository root (if present)

## Migration Conventions

### File/Directory Naming
- Migration modules use the pattern `m<NNNN>_<descriptive_name>/mod.rs` (e.g., `m0001_initial/mod.rs`)
- The numeric prefix is zero-padded to 4 digits and sequential
- The descriptive name uses snake_case

### Struct Naming
- Each migration module exports a struct (e.g., `Migration`) that implements `MigrationTrait`
- The struct is referenced by name in the `migrations()` function in `lib.rs`

### Migration Implementation Pattern
- Implement `MigrationTrait` from SeaORM
- `name()` method returns a string identifier for the migration
- `up()` method applies the forward migration
- `down()` method reverses the migration for rollback
- Both `up` and `down` are async and return `Result<(), DbErr>`
- Use `manager.alter_table(...)` for schema changes
- Use SeaORM's `Table`, `ColumnDef`, and entity enums for type-safe schema operations

### Migration Registration
- Migrations are registered in `migration/src/lib.rs`
- A `migrations()` function returns a `Vec<Box<dyn MigrationTrait>>`
- Each migration is added as `Box::new(module_name::Migration)` in sequential order

## General Rust Conventions

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`

### Module Structure
- Domain modules follow `model/ + service/ + endpoints/` structure
- Each module's `endpoints/mod.rs` registers routes

### Import Organization
- SeaORM types imported at the top (entity references, table/column enums)
- Standard library imports, then external crate imports, then local imports

### Testing Conventions
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Assert pattern: `assert_eq!(resp.status(), StatusCode::OK)`
- Tests validate actual values, not just counts

## Framework-Specific Conventions

### Database (SeaORM)
- Entity definitions in `entity/src/` with one file per table
- Column enums defined on entity structs for type-safe queries
- Table alter operations use `Table::alter().table(Entity::Table)` pattern

### HTTP (Axum)
- Route mounting in `server/src/main.rs`
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Shared query helpers (filter, paginate, sort) in `common/src/db/query.rs`
