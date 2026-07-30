# File 2: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose
Database migration that drops the deprecated `status` column from the `advisory` table.

## Full Implementation

```rust
use sea_orm_migration::prelude::*;

use entity::advisory::Advisory;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
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

    /// Re-adds the `status` column as a nullable string to allow rollback.
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
```

## Design Decisions

### Migration naming
- Named `m0002_drop_advisory_status` following the `m<NNNN>_<snake_case_description>` pattern established by `m0001_initial`
- Sequential numbering (`0002`) ensures correct migration ordering

### Up method
- Uses `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)` as specified in the Implementation Notes
- References `Advisory::Table` and `Advisory::Status` from the entity module for type-safe table/column identification
- Returns `Result<(), DbErr>` matching the `MigrationTrait` contract

### Down method
- Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` as specified in the Implementation Notes
- Column is nullable (`.null()`) to avoid breaking existing rows that were inserted after the column was dropped -- they would have no value for this column
- Type is `.string()` matching the original column type

### Documentation
- Module-level doc comment explains the purpose and context of the migration
- Method-level doc comments on `up` and `down` describe what each direction does
- Follows the skill's requirement that every new public symbol has a documentation comment

## Convention Compliance
- Implements `MigrationTrait` with both `up` and `down` methods (contract completeness)
- Uses `sea_orm_migration::prelude::*` import pattern
- References entity enums for type-safe DDL operations
- Follows the same structure as `m0001_initial/mod.rs`
- Uses `async_trait` attribute for async trait methods (SeaORM pattern)

## Verification Notes
- Before implementing, would verify via Serena or Grep that `entity/src/advisory.rs` does NOT reference a `Status` column variant (confirming it was already removed from the entity definition)
- Would search the codebase for any remaining references to `advisory.status` or `Advisory::Status` in service/query code to confirm the column is truly unused
- The `Advisory::Status` enum variant must still exist in the entity for the migration to compile -- if it was removed from the entity, the migration would need to define its own column identifier enum
