## Repository
trustify-backend

## Target Branch
TC-9103

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a later update fails after an earlier one succeeds. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates each execute independently against `self.db`. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with some join table rows marked as deleted and others not. Use `self.db.transaction(|txn| { ... })` to wrap all three operations and replace `self.db` with `txn` in each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction()` block

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` call inside the `soft_delete` method with `.exec(txn)` so all three UPDATE statements execute within the same transaction
- The three updates to wrap are: `sbom::Entity::update_many()`, `sbom_package::Entity::update_many()`, and `sbom_advisory::Entity::update_many()`
- Follow the existing error handling pattern using `Result<()>` return type
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and passed in, ensuring all three tables receive the same `deleted_at` value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial soft-deletes)
- [ ] The `deleted_at` timestamp is consistent across `sbom`, `sbom_package`, and `sbom_advisory` rows
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with transaction wrapping
- [ ] Verify that `test_delete_sbom_returns_204` still passes

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
