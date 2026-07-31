# Sub-task for Review Comment 30001

**Issue Type:** Sub-task
**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback

## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three separate `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without a transaction boundary. If the second or third UPDATE fails after the first succeeds, the database is left in an inconsistent state where the SBOM is marked as deleted but some related join table rows are not.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The three UPDATE statements (sbom, sbom_package, sbom_advisory) must all use the same transaction handle
- Follow existing transaction patterns in the codebase if any exist (check ingestor module for examples)
- The `now` timestamp computation can remain outside the transaction since it is a pure value

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any of the three UPDATEs fails, none of the changes are committed (rollback on error)
- [ ] On success, all three tables (sbom, sbom_package, sbom_advisory) have their `deleted_at` set atomically
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
