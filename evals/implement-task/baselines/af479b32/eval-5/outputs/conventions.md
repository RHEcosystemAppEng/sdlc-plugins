# Conventions Discovered from Sibling Analysis

## Project Configuration Validation (Step 0)

The project CLAUDE.md (`claude-md-mock.md`) contains all required sections:
- Repository Registry: `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: `serena_backend` with `rust-analyzer`

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)
- **Directory structure:** Each migration lives in its own directory under `migration/src/`, named with a sequential number prefix: `m0001_initial/`, `m0002_drop_advisory_status/`, etc.
- **File structure:** Each migration directory contains a single `mod.rs` file.
- **Trait implementation:** Each migration implements SeaORM's `MigrationTrait` with two async methods: `up()` and `down()`.
- **Up method:** Applies the forward migration (create tables, add/drop columns, etc.).
- **Down method:** Reverses the migration for rollback support (drop tables, re-add columns, etc.).
- **Manager usage:** Both methods receive a `&SchemaManager` and use builder-pattern statements (`Table::alter()`, `Table::create()`, etc.) via `manager.alter_table(...)` or `manager.create_table(...)`.
- **Entity references:** Migrations reference entity enums (e.g., `Advisory::Table`, `Advisory::Status`) for type-safe table/column identification.

### Migration Registration (from `migration/src/lib.rs`)
- **Registration pattern:** `lib.rs` contains a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>` listing all migration modules in order.
- **Module declaration:** Each migration module is declared with `mod m000N_name;` at the top of `lib.rs`.
- **Ordering:** Migrations are listed in sequential order in the `vec![]` macro.

### SeaORM Conventions
- **Framework:** SeaORM for ORM and database migrations.
- **Column definitions:** Use `ColumnDef::new(Entity::Column)` builder pattern with chained type and constraint methods (e.g., `.string()`, `.null()`, `.not_null()`).
- **Table alteration:** Use `Table::alter().table(Entity::Table).drop_column(Entity::Column)` for column removal.
- **Owned statements:** All builder chains end with `.to_owned()` to produce an owned statement for the manager.

### General Rust Backend Conventions
- **Framework:** Axum for HTTP, SeaORM for database.
- **Module pattern:** Domain modules follow `model/ + service/ + endpoints/` structure.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Response types:** List endpoints return `PaginatedResults<T>`.
- **Testing:** Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Test Conventions

### Integration Test Pattern (from `tests/api/advisory.rs` and siblings)
- **Assertion style:** Use `assert_eq!` for status code checks and field-level validations.
- **Status code checks:** `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- **Database verification:** Tests verify database state changes by querying the database after operations.
- **Test naming:** Tests follow `test_<action>_<scenario>` pattern (e.g., `test_migration_up_drops_column`, `test_migration_down_readds_column`).
- **Test database:** Integration tests use a real PostgreSQL test database, not mocks.

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` file at the root. In a real implementation, this would be read for CI check commands and additional project conventions. No specific CI verification commands are known from the provided repository structure, so standard `cargo test` and `cargo build` would be used as fallback.
