# Sub-task: Wrap soft-delete cascade operations in a database transaction

**Issue Type:** Sub-task
**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback

## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in `SbomService::soft_delete` inside a single database transaction to ensure atomicity. Currently, the method executes three separate `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` without a transaction boundary. If the second or third UPDATE fails after the first succeeds, the database is left in an inconsistent state (e.g., SBOM marked deleted but related join table rows not updated).

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each `.exec()` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The existing `let now = chrono::Utc::now()` timestamp should remain outside the transaction (it does not need to be computed inside)
- Follow the transaction pattern used in the ingestor module (`modules/ingestor/src/graph/sbom/mod.rs`) for reference on SeaORM transaction usage

## Acceptance Criteria
- [ ] All three UPDATE statements (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any UPDATE fails, all changes are rolled back (no partial cascade state)
- [ ] The `soft_delete` method returns the transaction error if any step fails
- [ ] Existing tests continue to pass (test_delete_sbom_returns_204, test_delete_sbom_cascades_to_join_tables)

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
