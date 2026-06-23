## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the method executes three independent UPDATE queries (sbom, sbom_package, sbom_advisory) without transactional guarantees. If the sbom_advisory update fails after sbom_package succeeds, the database will be left in an inconsistent state where some related records are marked as deleted and others are not.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three UPDATE statements in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations to wrap: (1) update sbom.deleted_at, (2) update sbom_package.deleted_at, (3) update sbom_advisory.deleted_at
- Follow the existing error handling pattern using `Result<(), DbErr>` return type within the transaction
- The `now` timestamp variable should be computed before the transaction begins so all three updates use the same timestamp

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial updates)
- [ ] Each `.exec()` call within the transaction uses the transaction handle, not `self.db`
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` continue to pass with the transactional implementation
