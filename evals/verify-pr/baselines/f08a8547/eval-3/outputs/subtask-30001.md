## Issue Type
Sub-task

## Parent
TC-9103

## Summary
Wrap soft_delete operations in a database transaction to prevent inconsistent state

## Labels
ai-generated-jira, review-feedback

## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three UPDATE statements in the `soft_delete` method in a single database transaction. Currently, the sbom, sbom_package, and sbom_advisory updates execute as independent queries. If any update fails after a preceding one succeeds, the database is left in an inconsistent state (e.g., sbom marked as deleted but sbom_advisory rows still active, or vice versa).

## Review Context
**Review comment ID:** 30001
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` in each `.exec()` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three operations to wrap are: sbom update_many, sbom_package update_many, and sbom_advisory update_many
- Follow the existing transaction pattern used elsewhere in the codebase (check ingestor module for examples of `db.transaction()` usage)
- Ensure the `now` timestamp is captured before the transaction begins so all three tables receive the same `deleted_at` value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three updates fails, all changes are rolled back (no partial updates persist)
- [ ] The method returns an error if the transaction fails
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Verify that the soft_delete method uses a transaction (code inspection)
- [ ] Existing integration tests in tests/api/sbom_delete.rs continue to pass
