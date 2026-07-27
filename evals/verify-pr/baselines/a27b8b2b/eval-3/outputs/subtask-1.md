## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, if the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left with some related rows marked as deleted and others not. All three updates (sbom, sbom_package, sbom_advisory) must succeed or fail atomically.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` closure, replacing `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around the three UPDATE statements in the `soft_delete` method (lines ~136-157 in the current diff)
- Replace `&self.db` with `txn` as the connection argument in each `.exec()` call within the transaction closure
- The transaction closure must be async and return `Result<(), DbErr>`
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase — SeaORM's `TransactionTrait::transaction` method handles commit on success and rollback on error automatically
- The method's public signature (`pub async fn soft_delete(&self, id: i64) -> Result<()>`) should remain unchanged

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, all preceding changes within the transaction are rolled back — no partial updates persist
- [ ] The method's external behavior and return type remain unchanged for callers
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing integration tests (`test_delete_sbom_returns_204`, `test_delete_sbom_cascades_to_join_tables`) still pass with the transaction wrapping

## Review Context
**PR Comment ID:** 30001
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Reviewer:** reviewer-a
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
