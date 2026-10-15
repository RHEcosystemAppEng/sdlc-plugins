# Sub-Task for Review Comment 30001

**Issue Type:** Sub-task
**Parent:** TC-9103
**Summary:** Wrap soft_delete operations in a database transaction to prevent inconsistent state
**Labels:** ai-generated-jira, review-feedback

---

## Repository
trustify-backend

## Description
The `soft_delete` method in `SbomService` executes three sequential UPDATE statements (for `sbom`, `sbom_package`, and `sbom_advisory` tables) without transaction wrapping. If any UPDATE fails after a preceding one succeeds, the database is left in an inconsistent state -- for example, the SBOM record could be marked as deleted while its related `sbom_advisory` rows remain active. Wrap all three UPDATE operations inside a single database transaction so that either all succeed or all are rolled back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside a `self.db.transaction(|txn| { ... })` block and replace `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace each `.exec(&self.db)` with `.exec(txn)` inside the transaction closure
- The transaction ensures atomicity: if the `sbom_advisory` update fails, the `sbom` and `sbom_package` updates are rolled back
- Follow the existing transaction patterns used elsewhere in the service layer (check other service files for examples of `self.db.transaction()` usage)

## Acceptance Criteria
- [ ] All three UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, all preceding changes within the transaction are rolled back (no partial updates)
- [ ] The `soft_delete` method returns an error if the transaction fails
- [ ] All existing tests in `tests/api/sbom_delete.rs` continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."
