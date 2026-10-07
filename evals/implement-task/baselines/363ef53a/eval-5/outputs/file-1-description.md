# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the pattern established in `migration/src/m0001_initial/mod.rs`.

## Pre-implementation inspection

Before writing this file, read `migration/src/m0001_initial/mod.rs` to extract:
- The exact `use` imports for SeaORM migration traits
- How `MigrationTrait` is implemented (struct definition, trait impl block)
- The `MigrationName` trait implementation pattern
- How `up()` and `down()` methods are structured
- How `SchemaManager` is used to execute table operations

Also read `entity/src/advisory.rs` to:
- Confirm the `status` column is NOT referenced in the current entity definition
- Identify the `Advisory` enum and its variants (especially `Table` and any former `Status` variant)
- Understand how column identifiers are defined

## Detailed changes

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
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
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions followed

- Module naming: `m0002_drop_advisory_status` follows the `m####_descriptive_name` pattern from `m0001_initial`
- Struct: uses `pub struct Migration` with `DeriveMigrationName` derive macro (matches m0001 pattern)
- Trait implementation: `MigrationTrait` with async `up()` and `down()` methods
- `down()` method re-adds the column as `string().null()` for safe rollback (per Implementation Notes)
- Local `Iden` enum for table/column identifiers (scoped to this migration module)
- Documentation comment on the struct explaining the migration purpose
