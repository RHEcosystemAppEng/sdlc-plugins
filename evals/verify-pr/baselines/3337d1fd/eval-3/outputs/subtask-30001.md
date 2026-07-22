## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE operations in the `soft_delete` method inside a database transaction to ensure atomicity. Currently, the method executes three separate `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without a transaction boundary. If the second or third update fails after a previous one succeeds, the database will be left in an inconsistent state where some related rows are marked as deleted while others are not.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction(|txn| { ... })` block and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to open a transaction scope, following the SeaORM transaction pattern
- Replace `&self.db` with `txn` in all three `.exec()` calls within the `soft_delete` method (lines updating `sbom`, `sbom_package`, and `sbom_advisory` entities)
- The transaction closure should be `async move` and return `Ok(())` on success
- If any of the three updates fails, the transaction will automatically roll back all changes, preventing inconsistent state
- Existing patterns for transaction usage may exist in the `modules/ingestor/` module where multi-table writes are performed during SBOM ingestion

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations inside a single database transaction
- [ ] Each `.exec()` call uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all previous updates in the transaction are rolled back
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` pass without modification (the transaction wrapping is an internal implementation detail that does not change the API behavior)

## Issue Type
Sub-task
