## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method in `SbomService` inside a single database transaction. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent queries. If any update fails after a preceding one succeeds, the database is left in an inconsistent state (e.g., `sbom_package` rows marked as deleted but `sbom_advisory` rows not).

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction(|txn| { Box::pin(async move { ... }) })` to wrap all three UPDATE operations
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- The transaction ensures atomicity: if any of the three updates fails, all changes are rolled back
- Follow the existing error handling pattern using `Result<()>` with the `?` operator inside the transaction closure
- The `chrono::Utc::now()` timestamp assignment should remain inside the transaction to ensure all three tables receive the same timestamp

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial state)
- [ ] The method returns an error if the transaction fails
- [ ] Existing tests continue to pass (DELETE returns 204, cascade to join tables works)

## Test Requirements
- [ ] Verify that existing `test_delete_sbom_returns_204` and `test_delete_sbom_cascades_to_join_tables` tests still pass after the transaction wrapping change

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
