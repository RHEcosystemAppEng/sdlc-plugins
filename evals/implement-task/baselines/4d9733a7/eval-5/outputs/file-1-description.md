# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Sibling Reference

This file is modeled after the sibling migration `migration/src/m0001_initial/mod.rs`, which was inspected during Step 4 to understand the established migration pattern.

## Detailed Changes

This file is created from scratch. It contains:

### 1. Imports

```rust
use sea_orm_migration::prelude::*;
```

Import the SeaORM migration prelude, which provides `SchemaManager`, `Table`, `ColumnDef`, `MigrationTrait`, `MigrationName`, `Iden`, `DbErr`, and related types.

### 2. Iden enum (self-contained identifiers)

```rust
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

Define a local `Advisory` enum with `Table` and `Status` variants. Following the SeaORM migration convention, migrations define their own identifier enums rather than importing from the entity crate (`entity/src/advisory.rs`). This ensures migrations remain self-contained and stable even if entity definitions evolve over time.

### 3. Migration struct

```rust
/// Migration to drop the deprecated `status` column from the `advisory` table.
pub struct Migration;
```

A unit struct that serves as the migration entry point.

### 4. MigrationName implementation

```rust
impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}
```

Returns the migration's unique identifier, matching the module directory name.

### 5. MigrationTrait implementation

```rust
#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the `advisory` table.
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

- **`up` method**: Uses SeaORM's `TableAlterStatement` to drop the `status` column from the `advisory` table.
- **`down` method**: Re-adds the `status` column as a nullable string (`string().null()`) to allow rollback. Using nullable ensures no data constraint issues on rollback.

## Documentation

- Module-level doc comment explaining the migration's purpose
- Doc comments on both `up` and `down` methods

## Conventions Applied

- Follows the same module structure as `m0001_initial/mod.rs`
- Uses SeaORM migration API consistently with the existing codebase
- Migration name follows the `m<NNNN>_<snake_case_description>` numbering pattern
- Self-contained `#[derive(Iden)]` enums (does not depend on entity crate definitions)
- Returns `Result<(), DbErr>` directly using `?` operator pattern
