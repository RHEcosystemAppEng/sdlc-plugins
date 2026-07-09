## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently. If any update fails after a prior one succeeds, the database is left in an inconsistent state where some related rows are marked as deleted while others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations to wrap are: (1) update `sbom` entity setting `deleted_at`, (2) update `sbom_package` rows where `sbom_id` matches, (3) update `sbom_advisory` rows where `sbom_id` matches
- Follow the existing error handling pattern: the transaction will automatically roll back on any `DbErr`
- The `now` timestamp should be computed before the transaction begins so all three updates share the same value

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all prior UPDATEs in the same `soft_delete` call are rolled back
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` continues to pass (transaction wrapping is transparent to the API)
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` continues to pass (cascade behavior is preserved)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
