## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` tables are updated in three separate `exec` calls against `self.db`. If the second or third UPDATE fails after a prior one succeeds, the database is left in an inconsistent state where some records are marked as deleted and others are not. Use `self.db.transaction(|txn| { ... })` and execute all three updates against `txn` instead of `self.db`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many().exec()` calls in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace all three `&self.db` references inside `soft_delete` with `txn`
- The three UPDATE statements that must be wrapped are:
  1. `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `deleted_at` on related package rows
  3. `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory rows
- Follow the existing transaction patterns used elsewhere in the codebase (e.g., in the ingestor module)
- Preserve the existing `chrono::Utc::now()` timestamp usage -- all three updates should share the same timestamp within the transaction

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial updates)
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_nonexistent_sbom_returns_404, test_delete_already_deleted_sbom_returns_409, test_list_sboms_include_deleted, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Verify that partial failure scenarios result in rollback (no inconsistent state)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
