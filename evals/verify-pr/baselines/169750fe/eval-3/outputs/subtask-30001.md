## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates run independently against `self.db` — if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with partially-applied soft-delete markers.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** (comment [#30001](https://github.com/trustify/trustify-backend/pull/744#discussion_r30001)) on `modules/fundamental/src/sbom/service/sbom.rs` line 60:

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction()` closure, replacing `&self.db` with `&txn` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope — this is the SeaORM transaction API pattern
- Replace each `.exec(&self.db)` call inside `soft_delete` with `.exec(&txn)` so all three updates share the same transaction
- The transaction ensures atomicity: if any UPDATE fails, all three are rolled back
- Follow the existing error handling pattern — the `?` operator inside the transaction closure will cause automatic rollback on failure

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) inside a single database transaction
- [ ] Each `.exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial soft-delete state)
- [ ] Existing tests continue to pass — `test_delete_sbom_returns_204`, `test_delete_nonexistent_sbom_returns_404`, `test_delete_already_deleted_sbom_returns_409`, `test_list_sboms_include_deleted`, `test_delete_sbom_cascades_to_join_tables`

## Issue Type
Sub-task (parent: TC-9103)

## Labels
- ai-generated-jira
- review-feedback
