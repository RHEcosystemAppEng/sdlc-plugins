## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state when a partial failure occurs. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute as independent queries. If one fails after another succeeds, the database is left in an inconsistent state with some records marked as deleted and others not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's `TransactionTrait::transaction()` method on `self.db` to wrap all three UPDATE operations in a single database transaction
- Replace `&self.db` with `txn` (the transaction handle) inside the closure for each `.exec()` call
- The transaction should encompass: (1) updating `sbom::Entity` to set `deleted_at`, (2) updating `sbom_package::Entity` for matching `sbom_id`, and (3) updating `sbom_advisory::Entity` for matching `sbom_id`
- Follow the existing pattern in the ingestor module which uses `self.db.transaction()` for multi-table operations
- If any of the three UPDATE statements fails, the entire transaction rolls back, ensuring atomicity

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back (no partial updates)
- [ ] Existing tests continue to pass with the transactional implementation
- [ ] The `deleted_at` timestamp is consistent across `sbom`, `sbom_package`, and `sbom_advisory` rows after a successful delete

## Test Requirements
- [ ] Existing soft-delete tests pass without modification (transaction is transparent to callers)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

**Issue Type:** Sub-task
**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback
