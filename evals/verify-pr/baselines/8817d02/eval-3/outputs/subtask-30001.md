## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent queries. If the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in an inconsistent state where packages are marked deleted but advisories are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements target: `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity`
- All three must use the same `now` timestamp, which is already computed before the updates
- Follow existing transaction patterns in the codebase (check `modules/ingestor/` for transaction usage examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates persist)
- [ ] The method continues to return `Result<()>` with the same error semantics
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_returns_204` test passes with the transaction wrapper
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test passes with the transaction wrapper

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
