# File 3: Test Implementation

## Purpose

Implement the tests described in the Test Requirements section of TC-9205 to verify the migration works correctly.

## Test Strategy

The tests verify three aspects per the task's Test Requirements:
1. The migration runs successfully against a test database (up)
2. The rollback (down) re-adds the column
3. Existing advisory queries still work after the column is dropped

### Test Location

Based on the repository structure and test conventions, migration tests would be added to either:
- A new test file in the migration crate (e.g., `migration/tests/m0002_test.rs`), or
- Within the existing integration test infrastructure at `tests/api/advisory.rs` if migration testing is done as part of integration tests

Following the project's convention of integration tests against a real PostgreSQL database, these tests would live alongside the existing test infrastructure.

### Test File Content

```rust
/// Tests for m0002_drop_advisory_status migration.

use sea_orm_migration::prelude::*;
use sea_orm::DatabaseConnection;

/// Verifies that the migration successfully drops the `status` column from the advisory table.
#[tokio::test]
async fn test_m0002_up_drops_status_column() {
    // Given a test database with m0001 applied (advisory table has status column)
    let db = setup_test_database().await;
    let manager = SchemaManager::new(&db);

    // Verify the status column exists before migration
    let has_column = check_column_exists(&db, "advisory", "status").await;
    assert!(has_column, "status column should exist before migration");

    // When running the migration up
    let migration = m0002_drop_advisory_status::Migration;
    migration.up(&manager).await.expect("migration up should succeed");

    // Then the status column should no longer exist
    let has_column = check_column_exists(&db, "advisory", "status").await;
    assert!(!has_column, "status column should not exist after migration");
}

/// Verifies that the migration rollback re-adds the `status` column as a nullable string.
#[tokio::test]
async fn test_m0002_down_readds_status_column() {
    // Given a test database with m0002 applied (status column dropped)
    let db = setup_test_database().await;
    let manager = SchemaManager::new(&db);
    let migration = m0002_drop_advisory_status::Migration;
    migration.up(&manager).await.expect("migration up should succeed");

    // When rolling back the migration
    migration.down(&manager).await.expect("migration down should succeed");

    // Then the status column should be re-added as nullable
    let has_column = check_column_exists(&db, "advisory", "status").await;
    assert!(has_column, "status column should exist after rollback");

    let is_nullable = check_column_nullable(&db, "advisory", "status").await;
    assert!(is_nullable, "status column should be nullable after rollback");
}

/// Verifies that existing advisory queries continue to work after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_work_after_migration() {
    // Given a test database with m0002 applied and existing advisory data
    let db = setup_test_database_with_data().await;
    let manager = SchemaManager::new(&db);
    let migration = m0002_drop_advisory_status::Migration;
    migration.up(&manager).await.expect("migration up should succeed");

    // When querying advisories through the service layer
    let advisories = AdvisoryService::list(&db, Default::default())
        .await
        .expect("listing advisories should succeed");

    // Then results should be returned without errors
    assert!(!advisories.items.is_empty(), "should return existing advisories");

    // And advisory details should still include the severity field
    let first = &advisories.items[0];
    assert!(first.severity.is_some(), "severity field should still be present");
}
```

### Design Decisions

1. **Doc comments on every test**: Each test function has a `///` documentation comment explaining what it verifies, per the skill's requirement for AI-generated tests.
2. **Given-When-Then structure**: Each test uses `// Given`, `// When`, `// Then` section comments for non-trivial tests with distinct setup/action/assertion phases.
3. **Value-based assertions**: Tests assert on specific values and states (column existence, nullability, query results) rather than just length checks.
4. **Real database testing**: Following the project convention, tests run against a real PostgreSQL test database rather than mocking.
5. **Assertion style**: Uses `assert!` and `assert_eq!` consistent with the Rust testing conventions observed in sibling test files.
6. **Test naming**: Follows the `test_<action>_<scenario>` convention from sibling tests.
