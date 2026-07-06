# File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table. The `down` method re-adds the column as a nullable string to support rollback.

## File Path

`migration/src/m0002_drop_advisory_status/mod.rs`

Note: This requires creating the directory `migration/src/m0002_drop_advisory_status/` as well.

## Full File Content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code. Removing it
/// reduces confusion and prevents accidental usage.
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

/// Iden enum for type-safe table and column references.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

### Pattern adherence

- Follows the exact pattern from `m0001_initial/mod.rs`: struct definition, `MigrationName` impl, `MigrationTrait` impl with `up` and `down` methods
- Uses `#[async_trait::async_trait]` for the async trait implementation, matching the existing migration

### Column definition in `down`

- The `down` method re-adds `status` as `.string().null()` (nullable string), as specified in the Implementation Notes
- This allows rollback without data loss concerns -- the column will be empty but the schema will be restored
- Using `.null()` means existing rows will have `NULL` in the re-added column, which is safe since no code reads this column

### Entity references

- Defines a local `Advisory` Iden enum with `Table` and `Status` variants for type-safe references
- This is self-contained within the migration module rather than depending on the entity crate, which is the standard SeaORM migration pattern (migrations should be self-contained so they remain valid even as entities evolve)

### Schema operation

- Uses `Table::alter()` with `drop_column()` for the `up` migration, as specified in the Implementation Notes
- Uses `Table::alter()` with `add_column()` for the `down` migration to reverse the operation

### Documentation

- Doc comments on the struct explain what the migration does and why
- Doc comments on `up` and `down` methods describe their specific operations
- This follows the skill's requirement that every new struct and public function has a documentation comment
