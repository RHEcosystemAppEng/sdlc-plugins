## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently. If any intermediate update fails (e.g., `sbom_advisory` fails after `sbom_package` succeeds), the database is left in an inconsistent state with partially-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many().exec()` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each exec call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements remain the same (sbom, sbom_package, sbom_advisory) -- only the execution context changes from direct connection to transaction
- Follow the existing error handling pattern in the service layer: the `?` operator propagates errors, and the transaction will automatically roll back on any failure
- Check if other service methods in the codebase (e.g., in `modules/ingestor/`) use transactions for multi-table updates as a reference pattern

## Acceptance Criteria
- [ ] The `soft_delete` method executes all three UPDATE statements within a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back -- no partial updates remain
- [ ] Existing tests continue to pass with no behavior change for the success path
- [ ] The method signature and return type remain unchanged

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID**: 30001
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment text**: "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
