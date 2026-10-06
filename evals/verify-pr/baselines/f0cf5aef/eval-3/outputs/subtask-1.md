## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Wrap the three UPDATE statements in the `soft_delete` method inside a single database transaction to ensure atomicity. Currently, if the `sbom_advisory` update fails after the `sbom_package` update succeeds, the database is left in an inconsistent state where some join table entries are marked as deleted but others are not. Use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each exec call inside the transaction block.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- wrap the three `update_many` calls in `soft_delete` inside a `self.db.transaction()` block

## Implementation Notes
- Use the SeaORM transaction API: `self.db.transaction::<_, (), DbErr>(|txn| { Box::pin(async move { ... }) }).await?`
- Replace `&self.db` with `txn` for each `.exec()` call inside the transaction closure
- The three operations to wrap: updating `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity`
- Follow the existing transaction pattern used elsewhere in the codebase (check `modules/ingestor/src/` for transaction usage examples)

## Acceptance Criteria
- [ ] The `soft_delete` method wraps all three UPDATE operations in a single database transaction
- [ ] If any of the three updates fails, none of the updates are committed (atomicity)
- [ ] The method still returns `Result<()>` with proper error propagation from within the transaction

## Test Requirements
- [ ] Verify that the existing `test_delete_sbom_returns_204` test still passes with the transaction wrapper
- [ ] Verify that the existing `test_delete_sbom_cascades_to_join_tables` test still passes

## Review Context
**Original review comment (ID: 30001) by reviewer-a on `modules/fundamental/src/sbom/service/sbom.rs` line 60:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
