## Repository
trustify-backend

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three database UPDATE operations in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent operations. If any update after the first one fails (e.g., network error, constraint violation), the database is left in an inconsistent state where the SBOM is marked as deleted but some related join table rows are not.

## Review Context
**Review comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.begin().await?` to start a transaction, then use the transaction handle for all three `exec` calls, and `txn.commit().await?` at the end
- Alternatively, use the closure-based API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Follow existing transaction patterns in the codebase if any exist (check ingestor module for examples)
- Ensure the `now` timestamp is captured before the transaction begins so all three tables receive the same timestamp

## Acceptance Criteria
- [ ] The three `update_many` operations in `soft_delete` execute within a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial cascade state)
- [ ] The existing integration tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The `soft_delete` method signature and return type remain unchanged
