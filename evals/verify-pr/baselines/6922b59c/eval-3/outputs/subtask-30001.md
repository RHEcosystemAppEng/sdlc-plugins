## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently against `self.db`. If a later update fails after an earlier one succeeds, the database is left in an inconsistent state (e.g., the SBOM is marked deleted but its related join table entries are not). This sub-task wraps all three operations in `self.db.transaction(|txn| { ... })` so they either all succeed or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a transaction block

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `.exec()` calls within the transaction closure
- The existing pattern for transactions can be found in the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) which uses the same `self.db.transaction()` API
- Preserve the existing `chrono::Utc::now()` timestamp logic -- all three updates should use the same `now` value, which is already the case
- The method signature and return type do not change

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, none of the changes are committed (atomicity)
- [ ] Successful soft-delete still sets `deleted_at` on `sbom`, `sbom_package`, and `sbom_advisory` rows
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing test `test_delete_sbom_cascades_to_join_tables` validates that all three tables are updated atomically

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
>
> -- reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs`, line 60
