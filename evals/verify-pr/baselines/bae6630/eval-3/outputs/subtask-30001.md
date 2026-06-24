## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the sbom, sbom_package, and sbom_advisory updates run as separate queries -- if the sbom_advisory update fails after sbom_package succeeds, the database will be left in an inconsistent state with some join table rows marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements that must be wrapped are:
  1. `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `deleted_at` on related package join rows
  3. `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory join rows
- Follow the existing transaction patterns in the codebase (e.g., ingestor module uses transactions for multi-table writes)
- The `chrono::Utc::now()` timestamp should be captured once before the transaction and reused for all three updates to ensure consistency

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing tests continue to pass (no behavioral change for the success path)

## Test Requirements
- [ ] Existing `test_delete_sbom_returns_204` and `test_delete_sbom_cascades_to_join_tables` tests pass without modification (transaction is transparent on the success path)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Comment #30001 by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
