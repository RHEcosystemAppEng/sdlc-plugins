## Repository
trustify-backend

## Target Branch
TC-9103

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Issue Type
Sub-task

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the method executes three separate `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` without transactional guarantees. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related rows are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block

## Implementation Notes
- Replace `&self.db` with the transaction handle `txn` for each `exec` call inside the `soft_delete` method
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to create the transaction scope
- The transaction closure receives a `DatabaseTransaction` parameter; use it in place of `&self.db` for all three `update_many().exec()` calls
- Existing pattern: SeaORM transactions are created via `self.db.transaction(|txn| { Box::pin(async move { ... }) }).await`
- Ensure the return type remains `Result<()>` and errors inside the transaction propagate correctly via `?`

## Review Context
Reviewer **reviewer-a** commented on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back and no rows are modified
- [ ] Existing tests continue to pass (DELETE returns 204, cascade updates work)
- [ ] The method signature and return type remain unchanged

## Test Requirements
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` continues to pass, confirming cascade behavior within a transaction
