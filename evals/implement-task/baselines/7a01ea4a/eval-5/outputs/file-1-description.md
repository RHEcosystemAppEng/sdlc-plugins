# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field in a previous migration (m0001_initial) and is no longer read or written by any service code.

## Pre-implementation Inspection

Before writing this file, inspect `migration/src/m0001_initial/mod.rs` to understand:
- The exact import statements used for SeaORM migration types
- How `MigrationTrait` is implemented (struct name, method signatures)
- How the `Migration` struct is defined (unit struct or with fields)
- How entity enums are referenced (e.g., `Advisory::Table`, `Advisory::Status`)
- The naming convention for the migration struct (e.g., `Migration` as the struct name)

Also verify in `entity/src/advisory.rs` that the `status` column is no longer present in the entity definition. If the entity still references `status`, flag this as a blocker before proceeding.

## Detailed Implementation

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the deprecated `status` column from the `advisory` table.
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

## Key Design Decisions

1. **Follow m0001_initial pattern**: The struct, trait implementation, and method signatures mirror the existing migration in `m0001_initial/mod.rs` as directed by Implementation Notes.

2. **Local `Advisory` enum**: Define a local `Iden` enum for `Advisory::Table` and `Advisory::Status` rather than importing from the entity crate. This is standard SeaORM migration practice -- migrations should be self-contained so they remain valid even as the entity definitions evolve.

3. **Nullable string in `down`**: The rollback re-adds `status` as `.string().null()` to avoid breaking existing rows that would have no value for this column. This matches the Implementation Notes specification.

4. **`DeriveMigrationName`**: Uses the derive macro to automatically generate the migration name from the module path, consistent with SeaORM conventions.

## Conventions Applied

- Documentation comments on the `up` and `down` methods explaining their purpose
- Use of `to_owned()` to finalize the builder pattern (SeaORM convention)
- Async trait implementation following SeaORM's `MigrationTrait` contract
