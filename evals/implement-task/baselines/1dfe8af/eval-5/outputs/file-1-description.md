# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file at `migration/src/m0002_drop_advisory_status/mod.rs` following the pattern established by `m0001_initial/mod.rs`.

### Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in migration
//! m0001_initial and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

/// Drops the deprecated `status` column from the `advisory` table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
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

    /// Re-adds the `status` column as a nullable string for rollback.
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

/// Enum referencing the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **Follow m0001_initial pattern**: The struct implements `MigrationTrait` with `up` and `down` methods, exactly matching the sibling migration's structure.

2. **`up` method**: Uses `TableAlterStatement` via `Table::alter()` to drop the column, as specified in the Implementation Notes. This is the SeaORM-idiomatic way to perform DDL changes.

3. **`down` method**: Re-adds the `status` column as `string().null()` (nullable string), as specified in the Implementation Notes. This allows safe rollback without data loss concerns -- the column will be empty after rollback since the data was not preserved.

4. **Advisory enum**: Defines a local `DeriveIden` enum for `Advisory::Table` and `Advisory::Status` to reference the table and column by name. This follows SeaORM conventions for type-safe schema manipulation. The entity in `entity/src/advisory.rs` no longer references `Status`, so we define the identifier locally in the migration.

5. **Documentation**: Every public symbol has a doc comment, per the skill's code quality requirements. The module-level doc comment explains the motivation for the migration.

6. **DeriveMigrationName**: Uses the `#[derive(DeriveMigrationName)]` attribute on the Migration struct to automatically derive the migration name from the module path, following the same pattern as m0001_initial.
