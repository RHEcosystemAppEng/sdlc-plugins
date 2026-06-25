## Repository
trustify-backend

## Description
Wrap the three UPDATE statements in the `soft_delete` method (`SbomService::soft_delete` in `modules/fundamental/src/sbom/service/sbom.rs`) inside a single database transaction. Currently, the sbom, sbom_package, and sbom_advisory updates execute as independent queries. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state with some join table rows marked as deleted and others not. Use `self.db.transaction(|txn| { ... })` to wrap all three operations and replace `self.db` with `txn` for each `exec` call within the transaction closure.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a database transaction

## Implementation Notes
- Use `self.db.transaction(|txn| { ... })` to create the transaction scope (SeaORM transaction API)
- Inside the transaction closure, replace `&self.db` with `txn` in each `.exec()` call for `sbom::Entity::update_many`, `sbom_package::Entity::update_many`, and `sbom_advisory::Entity::update_many`
- The transaction ensures atomicity: if any of the three UPDATE statements fails, all changes are rolled back
- Follow the existing SeaORM transaction patterns used elsewhere in the codebase (check `modules/ingestor/` for examples of transaction usage)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE statements in a single database transaction
- [ ] If any UPDATE fails, the entire operation is rolled back (no partial updates)
- [ ] Existing tests continue to pass (the behavioral contract is unchanged; only atomicity is added)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
