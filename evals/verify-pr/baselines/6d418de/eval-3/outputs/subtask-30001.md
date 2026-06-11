## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently — if one fails after another succeeds, the database is left in an inconsistent state with partially-marked soft-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope around all three UPDATE operations in the `soft_delete` method
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction block
- Follow the SeaORM transaction pattern: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- The existing `chrono::Utc::now()` timestamp and `Expr::value(now)` usage should remain unchanged — only the execution context changes from direct DB to transaction
- Ensure the transaction rolls back all changes if any individual UPDATE fails

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing soft-delete behavior is preserved (same timestamp applied to all three tables)

## Test Requirements
- [ ] Test that a failed cascade update (e.g., sbom_advisory update failure) rolls back the sbom and sbom_package updates
- [ ] Existing soft-delete tests continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
