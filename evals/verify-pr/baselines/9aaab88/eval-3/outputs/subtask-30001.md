## Repository
trustify-backend

## Target Branch
main

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction. Currently, the `sbom`, `sbom_package`, and `sbom_advisory` updates execute independently. If the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with partially-applied soft-delete markers. Using a transaction ensures atomicity -- either all three tables are updated or none are.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in the `soft_delete` method inside `self.db.transaction(|txn| { ... })` and replace `&self.db` with `txn` for each `.exec()` call

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to wrap the three `Entity::update_many().exec()` calls in the `soft_delete` method
- Replace `&self.db` with `txn` as the executor argument for each `.exec()` call inside the transaction closure
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The `chrono::Utc::now()` timestamp assignment remains the same; only the executor changes

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] Each `.exec()` call inside the transaction uses the transaction handle (`txn`) instead of `self.db`
- [ ] If any of the three updates fails, all changes are rolled back (no partial soft-delete state)
- [ ] Existing tests (`tests/api/sbom_delete.rs`) continue to pass

## Test Requirements
- [ ] Existing integration tests for SBOM deletion continue to pass with the transaction wrapper
