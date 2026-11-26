# File 1 (CREATE): `migration/src/m0002_drop_advisory_status/mod.rs`

Pattern source: `migration/src/m0001_initial/mod.rs`. It uses the `DeriveMigrationName` struct, an `#[async_trait] impl MigrationTrait` with `up`/`down`, and a `DeriveIden` enum for table and column identifiers.

## Content

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The column was superseded by the `severity` enum field and is no longer read or
/// written by any service code. `down` re-adds it as a nullable string for rollback.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops `advisory.status`.
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

    /// Re-adds `advisory.status` as a nullable string column (data is not restored).
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

/// Identifiers for the `advisory` table columns touched by this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}

#[cfg(test)]
mod tests {
    use super::*;
    // Test DB bootstrap helper: reuse whatever the migration crate / test crate already
    // provides (discovered in Step 4); shown here as `test_db()` placeholder.

    /// Verifies that applying the migration removes the `status` column from `advisory`.
    #[tokio::test]
    async fn up_drops_advisory_status_column() {
        // Given a database migrated up to m0001_initial
        let db = test_db().await;
        let manager = SchemaManager::new(&db);
        assert!(manager.has_column("advisory", "status").await.unwrap());

        // When the m0002 migration is applied
        Migration.up(&manager).await.unwrap();

        // Then the status column no longer exists
        assert!(!manager.has_column("advisory", "status").await.unwrap());
    }

    /// Verifies that rolling back the migration re-adds `status` as a nullable column.
    #[tokio::test]
    async fn down_readds_advisory_status_column() {
        // Given a database with m0002 applied
        let db = test_db().await;
        let manager = SchemaManager::new(&db);
        Migration.up(&manager).await.unwrap();

        // When the migration is rolled back
        Migration.down(&manager).await.unwrap();

        // Then the status column exists again
        assert!(manager.has_column("advisory", "status").await.unwrap());
    }
}
```

## Notes
- The `Advisory` Iden is declared locally rather than imported from `m0001_initial`. Migrations are immutable snapshots and should not couple to each other. If Step 4 shows the project keeps a shared Iden module, reuse that instead (symbol dedup rule).
- The `up` body matches the exact call given in the Implementation Notes.
- `down` matches the Implementation Notes exactly: `ColumnDef::new(Advisory::Status).string().null()`.
- The test helper (`test_db()`) and the DB-backed test harness would be adapted to whatever the repo already uses. If the repo has no DB harness reachable from the migration crate, tests that need a separate file would be flagged as out of scope for user approval (see plan.md Step 7).
