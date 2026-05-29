## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `modules/fundamental/src/sbom/service/sbom.rs` (line 60):

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` tables using `self.db` directly. If any of the later updates fail after earlier ones succeed, the database is left in an inconsistent state with partially soft-deleted records.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `&txn` in each `.exec()` call

## Implementation Notes
- Use SeaORM's `self.db.transaction(|txn| { ... })` pattern to wrap all three UPDATE operations in a single transaction
- Replace `&self.db` with `&txn` (the transaction handle) in each `.exec()` call inside the closure
- The transaction closure should return `Ok(())` on success; any error inside the closure will automatically trigger a rollback
- Follow the existing error handling pattern in the codebase using `.context()` wrapping with anyhow

## Acceptance Criteria
- [ ] `SbomService::soft_delete` wraps all three UPDATE statements in a single database transaction
- [ ] Each `.exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing tests continue to pass with no behavioral change on the success path
