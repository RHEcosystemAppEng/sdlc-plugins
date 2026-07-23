## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently the method executes three separate `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transactional protection. If the second or third UPDATE fails after a prior one succeeds, the database is left in an inconsistent state with partially cascaded soft-delete timestamps.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction(|txn| { ... })` block, replacing `&self.db` with `txn` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The existing `update_many` pattern for `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity` remains unchanged -- only the executor reference changes from `&self.db` to `txn`
- Follow the existing error handling pattern: the transaction will automatically rollback on any error within the closure
- The `chrono::Utc::now()` timestamp computation should remain outside or at the top of the transaction closure so all three updates use the same timestamp

## Acceptance Criteria
- [ ] All three UPDATE statements in `soft_delete` execute within a single database transaction
- [ ] If any individual UPDATE fails, no changes are committed (full rollback)
- [ ] Existing tests continue to pass with no behavioral changes on the success path

## Test Requirements
- [ ] Verify existing test `test_delete_sbom_cascades_to_join_tables` still passes (confirms cascade behavior is preserved under transactional execution)

## Review Context
**PR Comment ID:** 30001
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Target PR
https://github.com/trustify/trustify-backend/pull/744
