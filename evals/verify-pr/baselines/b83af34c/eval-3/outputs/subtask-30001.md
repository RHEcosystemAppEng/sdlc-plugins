# Sub-Task: Wrap soft_delete cascade operations in a database transaction

**Issue Type:** Sub-task
**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback

---

## Repository
trustify-backend

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three sequential UPDATE statements in the `soft_delete` method within a single database transaction to ensure atomicity. Currently, the method executes three independent `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If any intermediate operation fails after preceding ones succeed, the database is left in an inconsistent state where some related records are marked as deleted but others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `&txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) })` to wrap the three UPDATE operations
- Replace `&self.db` with `txn` in each `.exec()` call within the transaction closure
- The three operations that must be atomic:
  1. Update `sbom` entity setting `deleted_at` to current timestamp
  2. Update `sbom_package` rows where `sbom_id` matches
  3. Update `sbom_advisory` rows where `sbom_id` matches
- Follow the existing transaction patterns in the codebase (e.g., ingestor module uses transactions for multi-table operations)
- Ensure the `chrono::Utc::now()` timestamp is captured once before the transaction and reused for all three updates (already the case in current code)

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back (no partial updates)
- [ ] The method signature and return type remain unchanged
- [ ] Existing tests continue to pass without modification

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass (transaction wrapping is transparent to the API layer)

## Review Context
**Comment #30001 by reviewer-a** on `modules/fundamental/src/sbom/service/sbom.rs`, line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
