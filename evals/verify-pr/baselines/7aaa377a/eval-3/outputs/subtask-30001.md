## Issue Type
Sub-task

## Parent
TC-9103

## Summary
Wrap soft_delete cascade updates in a database transaction

## Labels
ai-generated-jira, review-feedback

## Repository
trustify-backend

## Target Branch
main

## Description
The `soft_delete` method in `SbomService` executes three separate UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transactional wrapping. If any intermediate UPDATE fails after a previous one succeeds, the database is left in an inconsistent state with partially applied soft-deletes. Wrap all three operations in a single database transaction so they either all succeed or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Inside the transaction closure, execute all three `update_many` operations using `txn` instead of `&self.db`
- The existing `chrono::Utc::now()` timestamp generation should remain outside the transaction closure (or inside -- it does not affect correctness) since it is a pure computation
- Follow the transactional patterns used elsewhere in the codebase (e.g., ingestor module's multi-table operations)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) in a single database transaction
- [ ] If the `sbom` update succeeds but the `sbom_package` or `sbom_advisory` update fails, all changes are rolled back
- [ ] If the `sbom_package` update succeeds but the `sbom_advisory` update fails, all changes are rolled back
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] The DELETE endpoint still returns 204 on successful soft-delete

## Test Requirements
- [ ] Existing cascade test (`test_delete_sbom_cascades_to_join_tables`) continues to pass with transactional wrapping

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**File:** `modules/fundamental/src/sbom/service/sbom.rs`
**Line:** 60
**Reviewer:** reviewer-a
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
