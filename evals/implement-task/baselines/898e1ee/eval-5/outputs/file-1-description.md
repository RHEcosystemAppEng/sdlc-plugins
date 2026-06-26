# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Pre-implementation inspection

Before creating this file, inspect the sibling migration `migration/src/m0001_initial/mod.rs` using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true` to understand:

- The exact imports used (SeaORM migration traits, schema types)
- The struct naming convention for the migration
- The `MigrationTrait` implementation pattern (method signatures, return types)
- How `Table::alter()` and column operations are used
- The `name()` method return value format

Also verify in `entity/src/advisory.rs` that:
- The `Advisory` enum exists with a `Table` variant (for table name) and a `Status` variant (for column name)
- The entity no longer has a `status` field in its model definition (confirming it is safe to drop)

## Detailed Changes

The file would implement the following structure, following the pattern discovered in `m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer referenced by any service or entity code.
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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key implementation decisions

- The `up` method uses `TableAlterStatement` to drop the column, as specified in the Implementation Notes
- The `down` method re-adds the column as a nullable string (`string().null()`) to allow rollback without data loss, as specified in Implementation Notes
- A local `Advisory` enum with `Iden` derive is defined to reference the table and column names, following SeaORM conventions
- The struct derives `DeriveMigrationName` for automatic migration naming, following the pattern from `m0001_initial`
- Documentation comment added to the struct explaining the migration's purpose

## Acceptance Criteria Coverage

- Migration drops the `status` column from the `advisory` table (via `up` method)
- Migration `down` method re-adds the column as nullable string for rollback
