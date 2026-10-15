## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the method executes three independent update operations (sbom, sbom_package, sbom_advisory) without transactional guarantees. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state where some related rows are marked as deleted and others are not.

## Issue Type
Sub-task

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three update operations in `soft_delete` inside a database transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap the three `update_many().exec()` calls in the `soft_delete` method
- Replace `&self.db` with `txn` for each `.exec()` call inside the transaction closure
- Follow the SeaORM transaction pattern: the closure receives a `TransactionTrait` handle that is committed on success and rolled back on error
- The existing `chrono::Utc::now()` timestamp and filter logic remain unchanged; only the execution context changes from direct database connection to transaction handle

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial updates)
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)
- [ ] The transaction uses `txn` instead of `self.db` for each exec call

## Test Requirements
- [ ] Verify that the existing cascade test (`test_delete_sbom_cascades_to_join_tables`) still passes with the transactional implementation
