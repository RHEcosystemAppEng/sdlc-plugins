# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New SeaORM migration that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field and is no longer referenced by any entity or service code.

## Pre-Creation Inspection

Before creating this file, inspect the sibling migration to understand the established pattern:
- **Read `migration/src/m0001_initial/mod.rs`** — understand how `MigrationTrait` is implemented, what imports are used, how `up` and `down` methods are structured, and what naming conventions apply to the `Migration` struct

Also verify the assumption that the column is unused:
- **Read `entity/src/advisory.rs`** — confirm the Advisory entity no longer includes a `status` field or column reference

## File Content

The file implements `MigrationTrait` following the pattern from `m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in m0001_initial
/// and is no longer read or written by any service code.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null()
                            .to_owned(),
                    )
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

## Key Design Decisions

1. **`Iden` enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for type-safe table/column references, following SeaORM migration conventions
2. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes
3. **`down` method**: Re-adds the column as `string().null()` so rollback does not break existing rows that would have no value for the column
4. **Documentation**: Every public symbol has a doc comment explaining its purpose

## Conventions Applied

- Same `use sea_orm_migration::prelude::*;` import pattern as `m0001_initial`
- Same `Migration` struct name as `m0001_initial`
- Same `MigrationTrait` implementation structure (async `up`/`down` methods)
- Same error return type pattern (`Result<(), DbErr>`)
- Migration name string matches the directory name (`m0002_drop_advisory_status`)
