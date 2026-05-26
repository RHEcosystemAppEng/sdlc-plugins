## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state. Currently, if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left with partially applied soft-delete markers. All three operations (sbom, sbom_package, sbom_advisory) must succeed or fail atomically.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in all three `.exec()` calls within the `soft_delete` method
- The transaction ensures atomicity: if any of the three UPDATE statements fails, all changes are rolled back
- Follow the existing transaction patterns used elsewhere in the trustify-backend codebase (e.g., in the ingestor module's `graph/sbom/mod.rs` which handles multi-table writes)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-delete state)
- [ ] Existing tests continue to pass (no behavioral change for the success path)

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes with the transaction wrapper

## Review Context
Reviewer reviewer-a (comment 30001) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
