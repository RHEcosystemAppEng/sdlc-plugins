## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates each execute independently against `self.db`. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with some join table rows marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around all three UPDATE operations in the `soft_delete` method (lines ~44-60 in the current diff).
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure so all three updates use the same transactional connection.
- The transaction pattern should follow SeaORM's `TransactionTrait::transaction` API. The closure receives a `DatabaseTransaction` reference that implements `ConnectionTrait`, so the existing `Entity::update_many().exec()` calls will work with the transaction handle.
- Ensure the return type of the closure is compatible -- the three `.exec()` calls should propagate errors via `?` and the closure should return `Ok(())` on success.

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial updates)
- [ ] Existing tests continue to pass -- the functional behavior remains the same
- [ ] The transaction uses `txn` (the transaction handle) instead of `self.db` for each exec call

## Test Requirements
- [ ] Existing soft-delete integration tests pass without modification (behavior is unchanged for the success path)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
