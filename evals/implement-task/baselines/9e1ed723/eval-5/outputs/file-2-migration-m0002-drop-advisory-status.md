# File 2 (CREATE): `migration/src/m0002_drop_advisory_status/mod.rs`

## Purpose
Drop the deprecated `status` column from the `advisory` table; the `down` method re-adds it as a nullable string.

## Content
```rust
use sea_orm_migration::prelude::*;

/// Drops the deprecated `status` column from the `advisory` table.
///
/// The column was superseded by the `severity` enum field and is no longer
/// read or written by any service or entity code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Removes `advisory.status`.
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

    /// Re-adds `advisory.status` as a nullable string so the migration can be rolled back.
    /// Previously stored values are not restored.
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
///
/// Declared locally (not shared with `m0001_initial`) so this migration stays
/// self-contained and unaffected by future schema changes.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}

#[cfg(test)]
mod tests {
    // Uses the project's test-DB bootstrap helper (same one used by tests/api/*.rs);
    // exact helper name confirmed during Step 4 via search_for_pattern.
    use super::*;
    use crate::Migrator;
    use sea_orm::{ConnectionTrait, Database, Statement};
    use sea_orm_migration::MigratorTrait;

    /// Returns true when the `advisory` table has a `status` column.
    async fn has_status_column(db: &sea_orm::DatabaseConnection) -> bool {
        let row = db
            .query_one(Statement::from_string(
                db.get_database_backend(),
                "SELECT 1 FROM information_schema.columns \
                 WHERE table_name = 'advisory' AND column_name = 'status'"
                    .to_owned(),
            ))
            .await
            .expect("information_schema query");
        row.is_some()
    }

    /// Verifies that applying all migrations removes `advisory.status`.
    #[tokio::test]
    async fn test_up_drops_advisory_status_column() {
        // Given a fresh test database
        let db = test_db().await;

        // When all migrations are applied
        Migrator::up(&db, None).await.expect("migrations apply");

        // Then the status column no longer exists
        assert_eq!(has_status_column(&db).await, false);
    }

    /// Verifies that rolling back m0002 re-adds `advisory.status` as a nullable varchar.
    #[tokio::test]
    async fn test_down_readds_nullable_status_column() {
        // Given a database with all migrations applied
        let db = test_db().await;
        Migrator::up(&db, None).await.expect("migrations apply");

        // When the latest migration (m0002) is rolled back
        Migrator::down(&db, Some(1)).await.expect("rollback succeeds");

        // Then the status column exists, is nullable and is a character varying
        let row = db
            .query_one(Statement::from_string(
                db.get_database_backend(),
                "SELECT is_nullable, data_type FROM information_schema.columns \
                 WHERE table_name = 'advisory' AND column_name = 'status'"
                    .to_owned(),
            ))
            .await
            .unwrap()
            .expect("status column re-added");
        assert_eq!(row.try_get::<String>("", "is_nullable").unwrap(), "YES");
        assert_eq!(row.try_get::<String>("", "data_type").unwrap(), "character varying");
    }
}
```

## Notes
- The pattern mirrors `m0001_initial/mod.rs`: `DeriveMigrationName`, `#[async_trait::async_trait]`, `sea_orm_migration::prelude::*`, and a `DeriveIden` enum.
- `test_db()` is a placeholder for the repository's existing test-database bootstrap. Reuse the existing helper rather than writing a new one. If the migration crate lacks dev-dependencies for `tokio`/test DB, adding them to `migration/Cargo.toml` is **out of scope** and would be flagged to the user (alternative: rely on the migration being exercised by the `tests/` crate's DB bootstrap).
- The tests assert on values (`false`, `"YES"`, `"character varying"`), not just on existence or counts.
- "Existing advisory queries still work" is covered by running the existing `tests/api/advisory.rs` suite (plus `search.rs`/`sbom.rs`) against the migrated DB. Those files are not modified.
