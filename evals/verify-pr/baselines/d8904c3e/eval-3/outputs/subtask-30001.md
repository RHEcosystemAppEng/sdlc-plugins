## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when one of the cascade updates fails. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently against `self.db`. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in a partially-deleted state. All three operations must execute atomically within `self.db.transaction(|txn| { ... })`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a database transaction using `self.db.transaction()`

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The three UPDATE statements to wrap are: (1) `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record, (2) `sbom_package::Entity::update_many()` setting `deleted_at` on related package rows, (3) `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory rows
- The `now` timestamp computation (`chrono::Utc::now()`) should remain outside the transaction closure or be moved inside it -- either is acceptable as long as all three rows receive the same timestamp
- Follow the existing error handling pattern: the transaction will automatically roll back on any `DbErr`

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] Each `exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three updates fails, the entire transaction rolls back (no partial state)
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The method returns `Ok(())` on successful transaction commit and propagates errors on failure

## Test Requirements
- [ ] Existing test `test_delete_sbom_returns_204` continues to pass with the transaction wrapper
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` continues to pass, confirming cascade behavior is preserved

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
