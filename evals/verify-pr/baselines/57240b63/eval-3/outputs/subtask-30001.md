## Repository
trustify-backend

## Target Branch
TC-9103

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID**: 30001
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Original comment**: The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Description
Wrap the three UPDATE operations in `SbomService::soft_delete` inside a single database transaction to prevent inconsistent state if one of the cascade updates fails partway through. Currently the sbom, sbom_package, and sbom_advisory updates each execute independently against `self.db`. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state with partially-applied soft deletes.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction()` block

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create a transaction scope
- Replace `&self.db` with `txn` for each of the three `exec()` calls inside the transaction block
- Follow the existing SeaORM transaction pattern used elsewhere in the codebase
- The transaction should encompass all three UPDATE statements: sbom, sbom_package, and sbom_advisory
- If any statement fails, the transaction rolls back all changes automatically

## Acceptance Criteria
- [ ] All three UPDATE operations in `soft_delete` execute within a single database transaction
- [ ] If any UPDATE fails, none of the changes are committed (atomic rollback)
- [ ] Existing tests continue to pass with the transactional implementation
- [ ] The `soft_delete` method signature and return type remain unchanged
