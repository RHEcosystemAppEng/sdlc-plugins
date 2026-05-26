# File 3: tests/api/advisory.rs (MODIFY — add migration tests)

## Purpose

Add integration tests that satisfy the Test Requirements from TC-9205:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (`down`) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

## Convention basis

From sibling test analysis (Step 4):
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` for HTTP assertions
- Each test function has a `///` doc comment
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- Integration tests hit a real PostgreSQL test database
- Test naming: `test_<action>_<scenario>`

## Tests to add

These tests are appended to `tests/api/advisory.rs`.

```rust
// ── Migration tests for m0002_drop_advisory_status ─────────────────────────

/// Verifies that the m0002_drop_advisory_status migration successfully drops
/// the `status` column from the `advisory` table.
#[tokio::test]
async fn test_migration_up_drops_status_column() {
    // Given a test database with m0001_initial applied (status column present)
    let db = setup_test_db_at_migration("m0001_initial").await;

    // When m0002_drop_advisory_status is applied
    apply_migration(&db, m0002_drop_advisory_status::Migration).await;

    // Then the `status` column no longer exists in the `advisory` table
    let columns = list_columns(&db, "advisory").await;
    assert!(
        !columns.contains(&"status".to_string()),
        "Expected `status` column to be absent after migration up, but it was present"
    );
}

/// Verifies that the m0002_drop_advisory_status rollback re-adds the `status`
/// column to the `advisory` table as a nullable string.
#[tokio::test]
async fn test_migration_down_readds_status_column() {
    // Given a test database with m0002_drop_advisory_status applied
    let db = setup_test_db_at_migration("m0002_drop_advisory_status").await;

    // When the migration is rolled back
    rollback_migration(&db, m0002_drop_advisory_status::Migration).await;

    // Then the `status` column is present in the `advisory` table
    let columns = list_columns(&db, "advisory").await;
    assert!(
        columns.contains(&"status".to_string()),
        "Expected `status` column to be present after migration down, but it was absent"
    );

    // And the column is nullable (no NOT NULL constraint)
    let is_nullable = column_is_nullable(&db, "advisory", "status").await;
    assert!(
        is_nullable,
        "Expected `status` column to be nullable after migration down"
    );
}

/// Verifies that existing advisory queries (list and get) still succeed after
/// the `status` column is dropped by m0002_drop_advisory_status.
#[tokio::test]
async fn test_advisory_queries_work_after_status_column_dropped() {
    // Given a test database with all migrations applied and an advisory record
    let (app, db) = setup_test_app_with_all_migrations().await;
    let advisory_id = seed_test_advisory(&db).await;

    // When fetching the advisory list
    let list_resp = app
        .get("/api/v2/advisory")
        .send()
        .await;

    // Then the list endpoint returns OK with the seeded advisory
    assert_eq!(list_resp.status(), StatusCode::OK);
    let body: serde_json::Value = list_resp.json().await;
    assert!(
        body["total_count"].as_u64().unwrap_or(0) > 0,
        "Expected at least one advisory in the list response"
    );
    let items = body["items"].as_array().expect("items should be an array");
    assert!(
        !items.is_empty(),
        "Expected at least one item in the advisory list"
    );
    // Verify the severity field is present (replaced status)
    let first = &items[0];
    assert!(
        first.get("severity").is_some(),
        "Expected `severity` field in advisory response; `status` has been dropped"
    );

    // When fetching the advisory by ID
    let get_resp = app
        .get(&format!("/api/v2/advisory/{}", advisory_id))
        .send()
        .await;

    // Then the get endpoint returns OK
    assert_eq!(get_resp.status(), StatusCode::OK);
}
```

## Notes on test helpers

The tests assume the following helpers exist or will be added in the test support module:

- `setup_test_db_at_migration(migration_name)` — creates a fresh test database with all
  migrations up to and including the named one applied
- `apply_migration(db, migration)` — runs a single migration's `up` method
- `rollback_migration(db, migration)` — runs a single migration's `down` method
- `list_columns(db, table_name)` — queries `information_schema.columns` and returns
  column names for the given table
- `column_is_nullable(db, table_name, column_name)` — returns true if the column allows NULL
- `setup_test_app_with_all_migrations()` — creates a full test app with all migrations applied
- `seed_test_advisory(db)` — inserts a minimal advisory record and returns its ID

If these helpers do not exist, they should be added to `tests/api/mod.rs` or a
`tests/support/` module following the project's existing test setup pattern.
