# Sub-task 1 (proposed; not created in Jira, offline eval)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** this sub-task Blocks TC-9103
- **Source:** review comment 30001 (code change request)

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` currently runs three separate `update_many()` statements against `self.db`, one each for `sbom`, `sbom_package` and `sbom_advisory`. They are not atomic. If a later update fails after an earlier one succeeds, the data is left inconsistent: for example, the SBOM is marked deleted while its `sbom_advisory` rows are not. This task wraps all three updates in one database transaction, so the soft-delete cascade either commits completely or rolls back completely.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — run the three `update_many()` calls in `soft_delete` inside one transaction, executing each against the transaction handle instead of `self.db`
- `tests/api/sbom_delete.rs` — extend the cascade test so it also asserts `sbom_advisory` rows are marked deleted

## Implementation Notes
- In `SbomService::soft_delete(&self, id: i64)` (`modules/fundamental/src/sbom/service/sbom.rs`), open a transaction with SeaORM, using `self.db.transaction(|txn| { ... })` as the reviewer suggested, or `self.db.begin()` followed by `txn.commit()`. Replace `.exec(&self.db)` with `.exec(txn)` on all three `update_many()` calls:
  - `sbom::Entity` (column `sbom::Column::DeletedAt`)
  - `sbom_package::Entity` (column `sbom_package::Column::DeletedAt`)
  - `sbom_advisory::Entity` (column `sbom_advisory::Column::DeletedAt`)
- Compute the timestamp once, before the transaction, with `chrono::Utc::now()`. All three tables must get the same `deleted_at` value, as the TC-9103 Implementation Notes require.
- Keep returning `Result<()>`, and keep the existing `.context("Failed to soft-delete SBOM")` wrapping in `delete_sbom` (`modules/fundamental/src/sbom/endpoints/mod.rs`). Errors must still map to `AppError` via `common/src/error.rs`.
- Check that `entity/src/sbom_package.rs` and `entity/src/sbom_advisory.rs` expose a `DeletedAt` column, and that the database schema has the matching `deleted_at` columns. The PR's migration `migration/src/m0042_sbom_soft_delete/mod.rs` only alters the `sbom` table. If the join tables lack the column, add it to the entities and to the migration.
- Do not change the endpoint's HTTP contract (204, 404, 409).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — the existing cascade logic to wrap
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — holds the `db` connection used to start the transaction
- `tests/api/sbom_delete.rs::test_delete_sbom_cascades_to_join_tables` — the existing cascade test to extend

## Acceptance Criteria
- [ ] All three updates in `SbomService::soft_delete` (`sbom`, `sbom_package`, `sbom_advisory`) run inside one database transaction
- [ ] If any of the three updates fails, none of the changes persist (the transaction rolls back)
- [ ] All three tables receive the same `deleted_at` timestamp
- [ ] `DELETE /api/v2/sbom/{id}` still returns 204, 404 and 409 as before

## Test Requirements
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` to assert that both `sbom_package` and `sbom_advisory` rows for the SBOM have `deleted_at` set
- [ ] Existing tests in `tests/api/sbom_delete.rs` keep passing

## Review Context
- **PR file/line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Reviewer:** reviewer-a (review 20001, CHANGES_REQUESTED)
- **Original comment (id 30001):**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Dependencies
- None
