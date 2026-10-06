## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the method executes three independent UPDATE queries (for `sbom`, `sbom_package`, and `sbom_advisory`). If any update after the first succeeds fails, the database is left in an inconsistent state with some rows marked as deleted and others not. This sub-task addresses review comment 30001 on PR #744.

## Issue Type
Sub-task

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations that must be wrapped are:
  1. `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `deleted_at` on related package rows
  3. `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory rows
- The `now` timestamp should be computed before the transaction begins (or inside, either is acceptable since the time difference is negligible)
- SeaORM transactions auto-rollback on error, so no explicit rollback handling is needed

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any one of the three updates fails, none of the updates are committed (rollback)
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The endpoint continues to return 204 No Content on successful deletion

## Test Requirements
- [ ] Existing test `test_delete_sbom_returns_204` passes (verifies basic deletion still works)
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` passes (verifies cascade still works within transaction)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
