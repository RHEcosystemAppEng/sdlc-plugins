## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three sequential UPDATE operations in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional guarantees. If the second or third update fails after an earlier one succeeds, the database is left in an inconsistent state where some entities are marked as deleted while related entities are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.begin().await?` to start a transaction, then pass the transaction handle to each `.exec()` call instead of `&self.db`
- Alternatively, use the closure-based `self.db.transaction(|txn| { Box::pin(async move { ... }) })` pattern if the project prefers that style
- The three operations that must be wrapped are:
  1. `sbom::Entity::update_many()...exec(&self.db)` (set `deleted_at` on the SBOM)
  2. `sbom_package::Entity::update_many()...exec(&self.db)` (cascade to packages)
  3. `sbom_advisory::Entity::update_many()...exec(&self.db)` (cascade to advisories)
- Replace `&self.db` with `&txn` (or the transaction variable name) in all three `.exec()` calls
- Ensure the transaction commits on success and rolls back on any error
- Check other service methods in the codebase (e.g., in `modules/ingestor/`) for existing transaction patterns to follow

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial state)
- [ ] The existing integration tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The method signature and external behavior remain unchanged (still returns `Result<()>`)

## Test Requirements
- [ ] Existing tests pass without modification (transaction wrapping is an internal implementation change)

## Review Context
Reviewer reviewer-a (comment 30001) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
