## Repository
trustify-backend

## Target Branch
main

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to prevent inconsistent state if any individual update fails partway through.

Currently, the `soft_delete` method in `SbomService` executes three sequential `update_many` calls (for `sbom`, `sbom_package`, and `sbom_advisory`) without transaction wrapping. If the second or third update fails after a previous one succeeds, the database is left in an inconsistent state where some tables are marked as deleted and others are not.

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three update_many calls in `soft_delete` inside a `self.db.transaction()` block, using the transaction handle (`txn`) for each `.exec()` call instead of `self.db`

## Implementation Notes
- Use SeaORM's transaction API: `self.db.transaction::<_, _, DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` in each of the three `exec()` calls inside the transaction closure
- The three operations to wrap are: (1) update sbom entity setting deleted_at, (2) update sbom_package rows, (3) update sbom_advisory rows
- Follow existing transaction patterns in the codebase if any exist (check ingestor module for examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any UPDATE fails, the entire transaction is rolled back (no partial state)
- [ ] The method signature and return type remain unchanged
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass after the refactor
