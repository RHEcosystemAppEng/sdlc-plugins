## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the SBOM record, sbom_package rows, and sbom_advisory rows are updated in separate database calls without transactional isolation. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state with some related rows marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations that must be wrapped: (1) update sbom.deleted_at, (2) update sbom_package.deleted_at, (3) update sbom_advisory.deleted_at
- Follow existing transaction patterns in the codebase (check ingestor module for examples of multi-table transactional writes)
- Ensure the `now` timestamp variable is computed before the transaction begins and captured by the closure

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] Existing tests continue to pass with the transactional implementation
- [ ] The method signature and return type remain unchanged

## Test Requirements
- [ ] Verify that the soft_delete method still passes existing integration tests (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Issue Type
Sub-task

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
