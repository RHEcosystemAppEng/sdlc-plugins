## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the method executes three independent `update_many` calls (sbom, sbom_package, sbom_advisory) without transaction isolation. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state where some join table rows are marked deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `soft_delete` inside `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The three operations to wrap are:
  1. `sbom::Entity::update_many()` setting `deleted_at` on the SBOM record
  2. `sbom_package::Entity::update_many()` setting `deleted_at` on related package rows
  3. `sbom_advisory::Entity::update_many()` setting `deleted_at` on related advisory rows
- Follow existing transaction patterns in the codebase (check `modules/ingestor/` for examples of SeaORM transaction usage)
- The `chrono::Utc::now()` timestamp should be computed once before the transaction and passed into the closure to ensure all three tables receive the same timestamp

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial deletes)
- [ ] The `deleted_at` timestamp is identical across all three tables for a given soft-delete operation
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Verify that `soft_delete` still works correctly for the happy path (all three updates succeed)
- [ ] Verify that transaction rollback occurs on failure (e.g., if sbom_advisory update fails, sbom and sbom_package changes are not persisted)

## Review Context
**Original review comment (id: 30001):**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Target PR
https://github.com/trustify/trustify-backend/pull/744
