## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some related records are marked as deleted and others are not.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction(|txn| { ... }).await?`
- Replace `&self.db` with `txn` in all three `exec()` calls within the `soft_delete` method
- The transaction ensures atomicity: either all three tables are updated or none are
- Follow the existing error handling pattern -- the `?` operator inside the transaction closure will cause an automatic rollback on failure
- The method signature and return type do not need to change

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire operation rolls back (no partial updates)
- [ ] Successful deletion still updates all three tables (`sbom`, `sbom_package`, `sbom_advisory`) with the same `deleted_at` timestamp
- [ ] Existing tests continue to pass with the transactional implementation

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer `reviewer-a` (comment id 30001) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

Issue Type: Sub-task
Parent: TC-9103
Labels: ai-generated-jira, review-feedback
