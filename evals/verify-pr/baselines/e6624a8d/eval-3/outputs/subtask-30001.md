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
The `soft_delete` method in `SbomService` executes three separate UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If any intermediate UPDATE fails after a prior one succeeds, the database is left in an inconsistent state with partially applied soft-deletion. Wrap all three operations in a single database transaction to ensure atomicity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three UPDATE statements in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `exec` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap the three `update_many().exec()` calls in `soft_delete`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The transaction ensures that if the `sbom_advisory` update fails after `sbom_package` succeeds, all changes are rolled back to prevent inconsistent state
- Return type remains `Result<()>` -- transaction errors propagate via `?`

## Acceptance Criteria
- [ ] The three UPDATE statements in `soft_delete` are wrapped in a single database transaction
- [ ] Each `exec` call within the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, all preceding UPDATEs in the transaction are rolled back
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
