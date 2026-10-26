# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

The file implements the SeaORM migration pattern following the sibling `m0001_initial/mod.rs`. It contains:

### 1. Module imports

```rust
use sea_orm_migration::prelude::*;
```

### 2. Migration struct

```rust
/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;
```

### 3. `MigrationTrait` implementation

```rust
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

    /// Re-adds the `status` column as a nullable string for rollback support.
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

### 4. Table/column identifier enum

Following the SeaORM pattern, a local enum identifies the table and column:

```rust
/// Identifiers for the advisory table and its status column used by this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- File structure matches `m0001_initial/mod.rs` (struct + MigrationTrait impl + Iden enum)
- Uses `#[derive(DeriveMigrationName)]` for automatic migration name derivation
- Uses `async_trait` for the async trait implementation
- Both `up` and `down` methods are implemented for reversibility
- Documentation comments on every public symbol (struct, methods, enum) per skill guidance
- The `Iden` enum is local to this migration module, scoped to only the table/column names needed
