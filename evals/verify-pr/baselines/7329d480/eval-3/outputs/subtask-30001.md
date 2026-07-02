## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the method executes three independent `update_many` calls on the `sbom`, `sbom_package`, and `sbom_advisory` tables in sequence without transactional wrapping. If the second or third UPDATE fails after an earlier one succeeds, the database is left in an inconsistent partially-deleted state where some related records are marked as deleted and others are not. The fix is to use `self.db.transaction(|txn| { ... })` and execute all three updates against `txn` instead of `self.db`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a database transaction

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Keep the same `chrono::Utc::now()` timestamp assignment -- all three tables should use the same `deleted_at` value
- Follow existing transaction patterns in the codebase (check `modules/ingestor/` for examples of transaction usage)
- The transaction ensures all three updates either succeed together or roll back together, preventing inconsistent state

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (sbom, sbom_package, sbom_advisory) inside a single database transaction
- [ ] Each `exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three updates fails, all changes are rolled back (no partial deletes)
- [ ] All existing tests continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Review comment #30001 by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
