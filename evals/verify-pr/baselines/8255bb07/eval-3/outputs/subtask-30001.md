## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the method executes three separate `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transaction wrapping. If any operation fails after a preceding one succeeds, the database is left in an inconsistent state where some tables are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap all three UPDATE operations in a single transaction, following SeaORM's transaction API
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction block
- The transaction ensures that if the `sbom_advisory` update fails after `sbom_package` succeeds, all changes are rolled back
- The `chrono::Utc::now()` timestamp should be captured once before the transaction and reused for all three updates (existing behavior, just moved inside the transaction)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (`sbom`, `sbom_package`, `sbom_advisory`) inside a single database transaction
- [ ] If any UPDATE fails, all preceding changes within the transaction are rolled back
- [ ] The method continues to return `Result<()>` with the same error propagation behavior
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing cascade test (`test_delete_sbom_cascades_to_join_tables`) still passes with transaction wrapping

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Original review comment by **reviewer-a** on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
