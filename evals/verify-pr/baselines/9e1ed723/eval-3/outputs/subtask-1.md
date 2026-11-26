# Sub-task 1 (would be created)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** Blocks (inward: this sub-task, outward: TC-9103)
- **Source:** review comment 30001 (code change request)

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` runs three separate UPDATE statements: it sets `deleted_at` on `sbom`, then on `sbom_package`, then on `sbom_advisory`. Each one executes directly on `self.db`. If a later update fails, the database is left inconsistent: the SBOM is marked deleted but its join-table rows are not. The `DELETE /api/v2/sbom/{id}` handler then returns 409 Conflict on retry, so the cascade can never be completed through the API. Run all three updates in one database transaction so the soft-delete either commits completely or rolls back completely.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many()` calls in `soft_delete` in a single transaction and run each `exec` on the transaction handle instead of `self.db`
- `tests/api/sbom_delete.rs` — extend the cascade test to also assert `sbom_advisory` rows are marked deleted

## Implementation Notes
- In `SbomService::soft_delete(&self, id: i64)` (`modules/fundamental/src/sbom/service/sbom.rs`), follow the reviewer's guidance: wrap the three operations in `self.db.transaction(|txn| { ... })` (SeaORM `TransactionTrait`) and pass `txn` instead of `&self.db` to each `.exec(...)` call for `sbom::Entity`, `sbom_package::Entity`, and `sbom_advisory::Entity`.
- Keep a single `chrono::Utc::now()` timestamp shared across all three updates so the rows keep the same `deleted_at` value.
- Propagate transaction errors with the existing error convention (`Result<T, AppError>` with `.context()` wrapping) so the `delete_sbom` handler in `modules/fundamental/src/sbom/endpoints/mod.rs` still maps failures correctly. Leave the 204/404/409 behavior unchanged.
- Do not change the public signature of `soft_delete`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — existing cascade logic to wrap
- `tests/api/sbom_delete.rs::test_delete_sbom_cascades_to_join_tables` — existing cascade test to extend
- `common/src/error.rs::AppError` — error type returned by handlers

## Acceptance Criteria
- [ ] The `sbom`, `sbom_package`, and `sbom_advisory` updates in `soft_delete` run inside one database transaction
- [ ] If any of the three updates fails, none of the `deleted_at` changes persist (the transaction rolls back)
- [ ] `DELETE /api/v2/sbom/{id}` still returns 204 on success, 404 for a non-existent SBOM, and 409 for an already-deleted SBOM
- [ ] All three tables receive the same `deleted_at` timestamp

## Test Requirements
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` to assert that related `sbom_advisory` rows also have `deleted_at` set
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Review Context
- **PR file/line:** `modules/fundamental/src/sbom/service/sbom.rs:60` (PR #744, review 20001, comment 30001, reviewer-a)
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
