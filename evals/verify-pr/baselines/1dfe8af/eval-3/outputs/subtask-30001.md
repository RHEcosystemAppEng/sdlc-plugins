## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the sbom, sbom_package, and sbom_advisory updates execute independently — if one fails after the others succeed, the database is left in a partially-deleted state.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction` method on `self.db` to wrap all three UPDATE operations in a single database transaction
- Replace `&self.db` with the transaction handle `txn` in each of the three `.exec()` calls inside `soft_delete`
- The transaction closure pattern in SeaORM is: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- All three updates (sbom, sbom_package, sbom_advisory) must use the same transaction handle so they either all commit or all roll back
- No changes to the method signature are needed — the caller does not need to know about the internal transaction

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three updates fails, none of the updates are committed (all roll back)
- [ ] Existing tests continue to pass with the transactional implementation

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** (comment 30001 on `modules/fundamental/src/sbom/service/sbom.rs`, line 60):

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
