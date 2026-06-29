## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` tables without transactional guarantees. If any intermediate update fails (e.g., due to a database constraint violation or connection interruption), the system is left in an inconsistent state where the SBOM may be marked as deleted while related join table rows remain active.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.begin()` transaction block, replacing `&self.db` with the transaction handle (`&txn`) for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: call `self.db.begin().await?` to start a transaction, execute all three `update_many` operations using `&txn` instead of `&self.db`, then call `txn.commit().await?` on success
- Follow the existing transaction pattern used in the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) which uses the same `begin()`/`commit()` approach for multi-table writes
- The `soft_delete` method signature does not need to change -- the transaction is an internal implementation detail
- Ensure the `?` operator properly triggers transaction rollback on any intermediate failure (SeaORM transactions auto-rollback on drop if not committed)

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Test Requirements
- [ ] Existing cascade test (`test_delete_sbom_cascades_to_join_tables`) validates that all three tables are updated together

## Review Context
Reviewer @reviewer-a (comment 30001) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
