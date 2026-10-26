# File 3: Tests for the migration

## Action: WOULD WRITE / VERIFY

## Purpose

Implement the three test requirements specified in the task:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

## Test Location

Tests would be placed in one of two locations depending on the project's existing test infrastructure:

- **Option A (inline module tests)**: `migration/src/m0002_drop_advisory_status/mod.rs` using `#[cfg(test)] mod tests { ... }` -- if sibling `m0001_initial/mod.rs` contains inline tests.
- **Option B (integration tests)**: `tests/api/advisory.rs` or a dedicated `tests/migration.rs` -- if the project uses integration tests with a real PostgreSQL test database (which the repo structure suggests with `tests/api/advisory.rs`).

The repo conventions indicate integration tests in `tests/api/` hit a real PostgreSQL test database. Migration tests likely follow the same pattern. Would inspect `m0001_initial/mod.rs` and `tests/` to determine the established pattern.

## Test Implementations

### Test 1: Migration runs successfully

```rust
/// Verifies that the m0002 migration successfully drops the `status` column from the advisory table.
#[tokio::test]
async fn test_migration_up_drops_status_column() {
    // Given a database with the advisory table containing a status column
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0001_initial").await;

    // When the m0002 migration runs
    run_migration_up(&db, "m0002_drop_advisory_status").await;

    // Then the status column should no longer exist on the advisory table
    let columns = get_table_columns(&db, "advisory").await;
    assert!(!columns.contains(&"status".to_string()),
        "status column should have been dropped but was found in: {:?}", columns);
}
```

### Test 2: Rollback re-adds the column

```rust
/// Verifies that rolling back the m0002 migration re-adds the status column as a nullable string.
#[tokio::test]
async fn test_migration_down_readds_status_column() {
    // Given a database where m0002 has been applied (status column dropped)
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0002_drop_advisory_status").await;

    // When the m0002 migration is rolled back
    run_migration_down(&db, "m0002_drop_advisory_status").await;

    // Then the status column should exist again as a nullable string
    let columns = get_table_columns(&db, "advisory").await;
    assert!(columns.contains(&"status".to_string()),
        "status column should have been re-added after rollback");

    let column_info = get_column_info(&db, "advisory", "status").await;
    assert!(column_info.is_nullable, "re-added status column should be nullable");
    assert_eq!(column_info.data_type, "varchar", "re-added status column should be a string type");
}
```

### Test 3: Existing advisory queries work after migration

```rust
/// Verifies that existing advisory queries continue to work after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_work_after_status_drop() {
    // Given a database with the m0002 migration applied
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0002_drop_advisory_status").await;

    // And an advisory record exists
    insert_test_advisory(&db, "ADV-001", "critical").await;

    // When querying advisories through the service layer
    let advisories = AdvisoryService::list(&db, Default::default()).await.unwrap();

    // Then the query should succeed and return the advisory
    assert_eq!(advisories.items.len(), 1);
    assert_eq!(advisories.items[0].id, "ADV-001");
}
```

## Conventions Applied

- Test function naming: `test_<what_is_being_tested>` pattern
- Assertion style: `assert_eq!` and `assert!` with descriptive messages (matching `tests/api/` pattern)
- Documentation comment on every test function per skill guidance
- Given-when-then section comments for non-trivial tests per skill guidance
- Value-based assertions (checking actual column names and properties, not just counts) per skill guidance
- Uses the project's test database infrastructure for integration tests
