## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, the `soft_delete` method in `modules/fundamental/src/sbom/service/sbom.rs` executes three sequential UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction isolation. If a later update fails after an earlier one succeeds, the database is left in an inconsistent state where some tables are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Follow the existing transaction pattern used elsewhere in the codebase (check `modules/ingestor/` for transaction usage examples)
- The `chrono::Utc::now()` timestamp assignment should remain inside the transaction to ensure all three tables receive the same timestamp

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back (no partial updates)
- [ ] Existing tests (`tests/api/sbom_delete.rs`) continue to pass
- [ ] The `soft_delete` method signature remains unchanged (callers are not affected)

## Test Requirements
- [ ] Test that a simulated failure in one of the cascade updates rolls back all changes (if testable with the existing test infrastructure)
- [ ] Verify that the existing delete integration tests still pass after the transaction wrapping

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Comment #30001 by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
"The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
