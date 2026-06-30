# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New database migration that drops the deprecated `status` column from the `advisory` table.

## Pre-Implementation Inspection

Before creating this file, inspect:
- `migration/src/m0001_initial/mod.rs` -- to understand the exact pattern for implementing `MigrationTrait`, including use statements, struct definition, async method signatures, and SeaORM API usage.
- `entity/src/advisory.rs` -- to confirm the `Advisory` entity enum includes `Table` and `Status` variants (needed for the column/table references in the migration), and to verify `status` is no longer an active model field.

## Detailed Changes

The file implements the SeaORM `MigrationTrait` following the pattern found in `m0001_initial/mod.rs`:

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

1. **`up` method**: Uses `Table::alter().drop_column()` to remove the column, as specified in the Implementation Notes.
2. **`down` method**: Re-adds the column as `.string().null()` to allow rollback without breaking existing rows. The column is nullable because there is no default value to backfill.
3. **`Advisory` enum**: Defined locally in the migration file (not imported from `entity/src/advisory.rs`) because the entity module may no longer contain the `Status` variant. Migration files should be self-contained and stable over time -- the entity evolves but the migration should always reference the same identifiers.
4. **`#[derive(DeriveMigrationName)]`**: Automatically derives the migration name from the module path, following the SeaORM convention used by `m0001_initial`.

## Sibling Parity Check (Constraint 5.8)

Compared against `m0001_initial/mod.rs`:
- Same `MigrationTrait` implementation pattern
- Same use of `sea_orm_migration::prelude::*`
- Same async method signatures
- Same `DeriveIden` enum pattern for table/column identifiers
