# File 1: migration/src/m0002_drop_advisory_status/mod.rs

**Action**: Create new file
**Purpose**: SeaORM migration that drops the deprecated `status` column from the `advisory` table

## Detailed Changes

This file implements a new SeaORM migration module following the exact pattern established by `migration/src/m0001_initial/mod.rs`.

### File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **`DeriveMigrationName`**: Uses the derive macro to automatically generate the migration name from the module path, consistent with SeaORM conventions and the existing `m0001_initial` migration.

2. **`Advisory` enum with `DeriveIden`**: Defines local table/column identifiers within the migration module rather than importing from the entity crate. This is the standard SeaORM migration pattern — migrations must be self-contained so they remain valid even if entity definitions change in the future.

3. **`up` method**: Uses `Table::alter().drop_column()` as specified in the Implementation Notes. This generates the SQL `ALTER TABLE advisory DROP COLUMN status`.

4. **`down` method**: Re-adds the column as `string().null()` (nullable VARCHAR) as specified in the Implementation Notes. The column is nullable because existing rows will not have values after rollback, and forcing a NOT NULL constraint would require a default value.

5. **Documentation comments**: Module-level doc comment explains the purpose and rationale. Each method has a doc comment describing what it does, following the skill's code quality requirement that every new public function must have documentation.
