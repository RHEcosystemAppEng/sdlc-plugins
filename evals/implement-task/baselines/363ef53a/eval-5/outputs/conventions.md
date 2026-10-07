# Conventions Discovered from Sibling Analysis

## Source

Conventions extracted from analysis of the trustify-backend repository structure and the sibling migration `migration/src/m0001_initial/mod.rs`.

---

## Migration Conventions

### Naming
- Migration module directories follow the pattern `m####_descriptive_name` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- Sequential numbering with zero-padded 4-digit prefix
- Descriptive suffix uses snake_case

### Structure
- Each migration is a directory with a `mod.rs` file
- Migration struct is named `Migration` (pub) with `#[derive(DeriveMigrationName)]`
- Implements `MigrationTrait` with async `up()` and `down()` methods
- Uses `async_trait::async_trait` attribute on the trait impl

### Registration
- Migrations are registered in `migration/src/lib.rs`
- Module declared with `mod m####_name;`
- Added to `migrations()` function as `Box::new(module::Migration)`
- Chronological ordering in the vec

### Column Operations
- Table/column identifiers defined as local `#[derive(Iden)] enum` within the migration module
- Uses SeaORM's `Table::alter()` builder for schema changes
- `SchemaManager` is the entry point for all DDL operations

## Entity Conventions

### Structure
- SeaORM entities in `entity/src/` directory
- One file per entity (e.g., `advisory.rs`, `sbom.rs`)
- Join tables as separate entity files (e.g., `sbom_advisory.rs`)

## General Code Conventions

### Framework
- Axum for HTTP routing
- SeaORM for database ORM and migrations
- PostgreSQL as the database

### Error Handling
- Handlers return `Result<T, AppError>` with `.context()` wrapping
- `AppError` enum defined in `common/src/error.rs`

### Module Pattern
- Domain modules follow `model/ + service/ + endpoints/` structure
- Each module's `endpoints/mod.rs` registers routes

### Testing
- Integration tests in `tests/api/` directory
- Tests hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`

### Response Types
- List endpoints return `PaginatedResults<T>`
- Shared filtering, pagination, sorting via `common/src/db/query.rs`

## CONVENTIONS.md

- A `CONVENTIONS.md` file exists at the repository root -- would read it for additional CI check commands and project-specific rules before implementation
