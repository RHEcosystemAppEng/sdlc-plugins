# Sub-Task: Wrap soft-delete operations in a database transaction

**Issue Type:** Sub-task
**Parent:** TC-9103
**Labels:** ai-generated-jira, review-feedback

## Repository
trustify-backend

## Description
The `soft_delete` method in `SbomService` executes three separate UPDATE statements (sbom, sbom_package, sbom_advisory) without a database transaction. If one UPDATE fails after others succeed, the database is left in an inconsistent state — e.g., the SBOM is marked deleted but related sbom_advisory rows are not. Wrap all three operations in a single database transaction to ensure atomicity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many` calls in `self.db.transaction(|txn| { ... })` and use `txn` for each `exec` call

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- Follow the existing transaction patterns used elsewhere in the codebase (e.g., ingestor module's ingestion pipeline)
- The transaction ensures that either all three UPDATE statements succeed or none of them are committed

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations (sbom, sbom_package, sbom_advisory) in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back — no partial state
- [ ] The DELETE endpoint continues to return 204 on success and the correct error codes on failure
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` continue to pass

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
