# File 2: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

Implement a SeaORM migration that drops the deprecated `status` column from the `advisory` table. The `down` method re-adds the column as a nullable string to support rollback.

## Pattern Source

This file follows the exact pattern established by `migration/src/m0001_initial/mod.rs`, which implements `MigrationTrait` with `up()` and `down()` methods using SeaORM's schema manager.

## Full File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

/// Migration that removes the `status` column from the `advisory` table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the `status` column from the `advisory` table.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .drop_column(Advisory::Status)
                    .to_owned(),
            )
            .await
    }

    /// Re-add the `status` column as a nullable string for rollback.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`#[derive(DeriveMigrationName)]`**: Uses SeaORM's derive macro to automatically generate the migration name from the module path, following the sibling pattern in `m0001_initial`.

2. **`Advisory` Iden enum**: Defines a local `Iden` enum for `Advisory::Table` and `Advisory::Status` to provide type-safe table/column identifiers for the alter statements. This is scoped to this migration module only -- it does not conflict with the entity definition in `entity/src/advisory.rs`.

3. **Nullable string for down()**: The `down` method re-adds `status` as `.string().null()` per the Implementation Notes. This ensures rollback does not break existing rows (they will have NULL in the re-added column).

4. **Documentation comments**: Every public item has a `///` doc comment per the skill's code quality practices (Step 6). The module-level `//!` comment explains why this migration exists.

## Conventions Followed

- File follows the same structure as `m0001_initial/mod.rs`: imports, Migration struct with derive, MigrationTrait impl, local Iden enum
- Uses `async_trait::async_trait` attribute on the impl block (matching sibling)
- Returns `Result<(), DbErr>` from both `up` and `down` methods
- Uses SeaORM's builder pattern for table alterations (`Table::alter().table(...).drop_column(...).to_owned()`)
- Module directory named `m0002_drop_advisory_status` following the `m<NNNN>_<description>` pattern

## Verification

- `cargo build` must compile the migration crate with the new module
- `cargo test` in the migration crate (if tests exist) must pass
- The `up` migration should successfully drop the `status` column when run against a test database
- The `down` migration should re-add the `status` column as a nullable string
- Existing advisory queries (in `tests/api/advisory.rs`) must still work after the column is dropped
