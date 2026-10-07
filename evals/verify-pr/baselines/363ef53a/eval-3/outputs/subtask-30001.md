## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` tables are updated in separate database calls without transactional guarantees. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related rows are marked deleted but others are not. The fix wraps all three operations in `self.db.transaction(|txn| { ... })` and uses `txn` instead of `self.db` for each `exec` call.

## Issue Type
Sub-task

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around the three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` (the transaction handle) in each `.exec()` call within the transaction block
- The transaction pattern is standard SeaORM usage: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Ensure the transaction rolls back automatically if any of the three updates fails, preventing partial soft-delete state
- The `chrono::Utc::now()` timestamp calculation should remain outside or at the start of the transaction block since it does not depend on the database

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (`sbom`, `sbom_package`, `sbom_advisory`) inside a single database transaction
- [ ] Each `.exec()` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three updates fails, the entire operation is rolled back (no partial deletes)
- [ ] Existing tests continue to pass (DELETE returns 204, cascade works correctly)

## Test Requirements
- [ ] Test that a simulated failure during cascade update does not leave partial soft-delete state (sbom marked deleted but related rows not marked)
