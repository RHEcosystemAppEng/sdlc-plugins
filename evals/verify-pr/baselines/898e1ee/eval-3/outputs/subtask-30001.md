## Repository
trustify-backend

## Target Branch
TC-9103-sbom-soft-delete

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three separate `exec(&self.db)` calls sequentially without a transaction boundary. If the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in an inconsistent state where some related rows are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations to wrap are: (1) update `sbom::Entity` to set `deleted_at`, (2) update `sbom_package::Entity` for matching `sbom_id`, (3) update `sbom_advisory::Entity` for matching `sbom_id`
- All three operations should use the same `now` timestamp, which is already captured before the updates
- Follow the existing error handling pattern -- the `?` operator inside the transaction closure will cause the transaction to roll back on any failure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, the entire operation is rolled back (no partial updates)
- [ ] The method continues to return `Result<()>` with the same error semantics
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` continues to pass (verifies basic soft-delete still works)
- [ ] Existing `test_delete_sbom_cascades_to_join_tables` continues to pass (verifies cascade still works)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**Comment ID:** 30001
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
