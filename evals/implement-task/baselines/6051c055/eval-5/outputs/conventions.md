# Discovered Conventions (from sibling analysis)

Conventions discovered by inspecting sibling files in the trustify-backend repository,
specifically by examining `migration/src/m0001_initial/mod.rs` and related migration
infrastructure.

## Migration Conventions

- **Module structure:** Each migration lives in its own subdirectory under `migration/src/`
  named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`).
  Each directory contains a `mod.rs` file with the migration implementation.

- **Trait implementation:** All migrations implement `MigrationTrait` from
  `sea_orm_migration::prelude::*` with two async methods: `up()` for applying the
  migration and `down()` for rolling it back.

- **Migration naming:** The `MigrationName` trait implementation returns a string matching
  the module directory name (e.g., `"m0001_initial"`).

- **Iden enums:** Migrations define local `#[derive(Iden)]` enums to reference table and
  column names in a type-safe manner rather than using raw strings. The enum variant
  `Table` maps to the table name, and other variants map to column names.

- **Registration:** Migrations are registered in `migration/src/lib.rs` by:
  1. Declaring the module (`mod m000N_name;`)
  2. Adding `Box::new(m000N_name::Migration)` to the `vec![]` in the `migrations()` function

- **Ordering:** Migrations are listed in chronological/sequential order in the `vec![]`.
  SeaORM executes them in list order, so new migrations must be appended at the end.

## Entity Conventions

- **Entity modules:** Entity definitions live in `entity/src/` with one file per table
  (e.g., `entity/src/advisory.rs`).

- **Column alignment:** Entity structs only include columns that exist in the current
  database schema. When a migration drops a column, the entity must have already been
  updated to remove the corresponding field. The task description confirms this was done
  for the `status` column in `entity/src/advisory.rs`.

## Rust Code Conventions

- **Async trait:** Migrations use `#[async_trait::async_trait]` for async trait methods.

- **Error handling:** Migration methods return `Result<(), DbErr>`, using SeaORM's error
  type. The `?` operator is used for error propagation.

- **Imports:** Migrations use a glob import from `sea_orm_migration::prelude::*` which
  brings in `Table`, `ColumnDef`, `SchemaManager`, `MigrationTrait`, `MigrationName`,
  `Iden`, and related types.

## Test Conventions

- **Migration tests:** Migration tests verify both `up()` and `down()` methods execute
  without errors. Tests run against a test database and verify schema changes by querying
  table metadata or running queries that exercise the affected columns.

- **Assertion style:** Tests use `assert!` and `assert_eq!` macros from the standard
  library.
