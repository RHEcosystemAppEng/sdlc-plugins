## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the soft-delete method executes three independent UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transactional guarantees. If the second or third UPDATE fails after a prior one succeeds, the database is left in an inconsistent state where some related records are marked deleted and others are not.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many().exec()` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each exec call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to create a transaction scope
- Inside the transaction closure, replace `&self.db` with the transaction handle (`txn`) for all three `exec()` calls
- The transaction should automatically commit on success and rollback on any error
- Follow the existing transaction patterns used elsewhere in the codebase (check ingestor module for examples of `self.db.transaction(|txn| { ... })` usage)
- The three UPDATE statements to wrap: sbom entity update, sbom_package cascade update, and sbom_advisory cascade update

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial updates)
- [ ] The method signature and return type remain unchanged
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` test continues to pass, confirming cascade behavior still works within a transaction
