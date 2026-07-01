# Sub-Task: Wrap soft_delete operations in a database transaction

## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method of `SbomService` inside a single database transaction to prevent inconsistent state. Currently, if the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in a partially-updated state where some join table rows are marked as deleted and others are not. The fix ensures atomicity: either all three updates succeed or none of them are applied.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations to wrap are: (1) update `sbom` entity setting `deleted_at`, (2) update `sbom_package` rows setting `deleted_at`, (3) update `sbom_advisory` rows setting `deleted_at`
- Follow the existing transaction patterns in the codebase (e.g., ingestor module's ingestion logic)
- Ensure the `now` timestamp is computed before entering the transaction so all three updates use the same value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, none of the changes are committed (atomicity)
- [ ] The method uses `txn` (the transaction handle) instead of `self.db` for each exec call
- [ ] Existing tests continue to pass with the transactional implementation

## Test Requirements
- [ ] Existing integration tests for SBOM deletion still pass (no behavioral change for the success path)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
