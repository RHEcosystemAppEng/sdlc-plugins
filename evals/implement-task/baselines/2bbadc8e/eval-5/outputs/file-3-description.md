# File 3: Tests for the migration

## Test Requirements from Task

1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

## Test Location

Tests would be placed in one of these locations depending on the project's test
conventions (determined during Step 4 sibling analysis):

- **Option A**: Inline `#[cfg(test)] mod tests` block within `migration/src/m0002_drop_advisory_status/mod.rs`
- **Option B**: Integration test file in `tests/` directory (e.g., `tests/migration.rs`)
- **Option C**: Existing migration test infrastructure within the `migration` crate

Based on the repository structure showing integration tests in `tests/api/`, the
likely approach is integration-level tests that run against a PostgreSQL test database.

## Test Implementations

### Test 1: Migration up runs successfully

```rust
/// Verifies that the m0002 migration successfully drops the `status` column from the advisory table.
#[tokio::test]
async fn test_m0002_migration_up_drops_status_column() {
    // Given a database with the advisory table containing a status column
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0001_initial").await;

    // When running the m0002 migration
    let result = run_migration(&db, "m0002_drop_advisory_status").await;

    // Then the migration succeeds and the status column no longer exists
    assert!(result.is_ok(), "Migration up should succeed");
    let columns = get_table_columns(&db, "advisory").await;
    assert!(
        !columns.contains(&"status".to_string()),
        "status column should be dropped after migration"
    );
}
```

### Test 2: Migration down re-adds the column

```rust
/// Verifies that rolling back the m0002 migration re-adds the `status` column as a nullable string.
#[tokio::test]
async fn test_m0002_migration_down_readds_status_column() {
    // Given a database where m0002 has already been applied
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0002_drop_advisory_status").await;

    // When rolling back the m0002 migration
    let result = rollback_migration(&db, "m0002_drop_advisory_status").await;

    // Then the status column is re-added as a nullable string
    assert!(result.is_ok(), "Migration down should succeed");
    let columns = get_table_columns(&db, "advisory").await;
    assert!(
        columns.contains(&"status".to_string()),
        "status column should exist after rollback"
    );
    let column_info = get_column_info(&db, "advisory", "status").await;
    assert!(column_info.is_nullable, "re-added status column should be nullable");
    assert_eq!(column_info.data_type, "character varying", "re-added status column should be string type");
}
```

### Test 3: Advisory queries still work after column drop

```rust
/// Verifies that existing advisory queries (list, get by ID) continue to work after dropping the status column.
#[tokio::test]
async fn test_advisory_queries_work_after_status_column_dropped() {
    // Given a database with the m0002 migration applied and existing advisory records
    let db = setup_test_database().await;
    run_all_migrations(&db).await;
    insert_test_advisory(&db, "CVE-2024-0001", "critical").await;

    // When querying advisories through the service layer
    let advisories = AdvisoryService::list(&db, Default::default()).await;

    // Then queries return results without errors
    assert!(advisories.is_ok(), "Advisory list query should succeed after migration");
    let results = advisories.unwrap();
    assert_eq!(results.items.len(), 1);
    assert_eq!(results.items[0].severity, "critical");
}
```

## Test Conventions Applied

- Doc comment on every test function (skill requirement, overrides sibling patterns)
- Given/When/Then section comments for non-trivial tests
- Value-based assertions (assert on specific column names, types, values -- not just counts)
- `assert_eq!` with descriptive messages per repository convention
- `tokio::test` for async database tests per Rust async testing convention
- Tests run against a real PostgreSQL test database (matching `tests/api/` integration pattern)
