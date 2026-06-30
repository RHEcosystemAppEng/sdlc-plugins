## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE operations in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the sbom, sbom_package, and sbom_advisory updates execute as separate database calls. If an intermediate update fails (e.g., sbom_advisory update fails after sbom_package succeeds), the data will be left in an inconsistent state where some join table rows are marked as deleted while others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The transaction ensures all three updates (sbom, sbom_package, sbom_advisory) either all succeed or all roll back
- Follow the existing pattern in the ingestor module if transaction usage exists there (check `modules/ingestor/src/graph/sbom/mod.rs` for transaction patterns)
- The `now` timestamp should be computed before the transaction begins so all three tables receive the same `deleted_at` value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial updates)
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The cascade test (`test_delete_sbom_cascades_to_join_tables`) confirms atomicity

## Test Requirements
- [ ] Existing integration tests pass without modification (the transaction wrapping should not change observable behavior on success)

## Review Context
**Original review comment (ID 30001):**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
