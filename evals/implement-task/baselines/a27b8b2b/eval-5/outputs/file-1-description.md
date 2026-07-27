# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the existing migration pattern established in `migration/src/m0001_initial/mod.rs`.

## Pre-Implementation Inspection

Before writing this file, inspect `migration/src/m0001_initial/mod.rs` using Serena (`mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true`) to understand:
- The struct definition pattern for migrations
- The `MigrationName` trait implementation pattern
- The `MigrationTrait` `up` and `down` method signatures and SeaORM API usage

Also inspect `entity/src/advisory.rs` to verify the `Advisory` entity enum includes a `Table` variant and a `Status` variant (for use in the alter table statement), and to confirm that no active model code references the `status` column.

## Detailed Changes

The file implements a SeaORM migration with the following structure:

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
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
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

- **`up` method**: Uses `TableAlterStatement` to drop the `status` column, as specified in the Implementation Notes
- **`down` method**: Re-adds the column as a nullable string (`string().null()`) to allow rollback without data loss concerns. The column is nullable because existing rows will not have a value after rollback.
- **`Advisory` enum**: Defines local `DeriveIden` identifiers for the table and column names, following SeaORM conventions. This is a local enum specific to this migration, separate from the entity definition.
- **`DeriveMigrationName`**: Uses the derive macro which auto-generates the migration name from the module path, matching the pattern in m0001_initial.

## Conventions Applied

- Follows the exact struct and trait implementation pattern from `m0001_initial/mod.rs`
- Uses SeaORM's builder pattern for table alterations
- Places the migration in its own subdirectory under `migration/src/`
