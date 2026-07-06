## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the method executes three independent UPDATE operations (on `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If any intermediate update fails, the database is left in an inconsistent state where some tables have `deleted_at` set and others do not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to create a transaction scope
- The three `Entity::update_many()...exec()` calls for `sbom`, `sbom_package`, and `sbom_advisory` must all use the transaction connection (`txn`) instead of `&self.db`
- Follow the existing error handling pattern: the `?` operator inside the transaction closure will cause an automatic rollback on failure
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and shared across all three updates (as it is currently)
- Pattern reference: SeaORM transaction usage: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial state)
- [ ] The method still sets `deleted_at` on `sbom`, `sbom_package`, and `sbom_advisory` rows matching the given SBOM ID
- [ ] The method returns `Ok(())` on success and propagates errors on failure
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Verify that the `soft_delete` method successfully updates all three tables within a transaction
- [ ] Verify that existing integration tests for SBOM deletion continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
