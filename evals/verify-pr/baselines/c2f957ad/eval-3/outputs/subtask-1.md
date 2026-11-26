# Sub-task 1 (would be created under TC-9103)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** Blocks (inward: this sub-task, outward: TC-9103)

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` currently runs three independent UPDATE statements (`sbom`, `sbom_package`, `sbom_advisory`) directly against `self.db`. If a later statement fails after an earlier one succeeds, the database is left inconsistent. For example, the SBOM is marked deleted but its `sbom_advisory` rows are not. This sub-task makes the soft-delete cascade atomic by running all three updates inside one database transaction, so they either all commit or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs`: run the three `update_many()` calls in `soft_delete` inside a single transaction, executing each against the transaction handle instead of `self.db`

## Implementation Notes
- In `SbomService::soft_delete(&self, id: i64)`, open a transaction on `self.db` (SeaORM `TransactionTrait`, e.g. `self.db.transaction(|txn| { ... })`, or `let txn = self.db.begin().await?; ... txn.commit().await?;`).
- Run `sbom::Entity::update_many()`, `sbom_package::Entity::update_many()` and `sbom_advisory::Entity::update_many()` with `.exec(txn)` / `.exec(&txn)` instead of `.exec(&self.db)`.
- Compute the `chrono::Utc::now()` timestamp once, before the transaction, and use the same value for all three updates (keeps the existing same-timestamp behavior from the Implementation Notes of TC-9103).
- Propagate errors with `?` so any failure rolls back the whole transaction. Keep the existing `Result<()>` signature so the `delete_sbom` handler in `modules/fundamental/src/sbom/endpoints/mod.rs` needs no change.
- Follow the existing error-handling convention (`.context()` wrapping in handlers, `Result<T, AppError>`).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete`: the method to make transactional
- `modules/fundamental/src/sbom/endpoints/mod.rs::delete_sbom`: the caller, whose contract (204/404/409) must be preserved

## Acceptance Criteria
- [ ] The `sbom`, `sbom_package` and `sbom_advisory` updates in `soft_delete` run inside a single database transaction
- [ ] If any of the three updates fails, none of the changes are persisted (the transaction rolls back)
- [ ] All three tables receive the same `deleted_at` timestamp on success
- [ ] Existing `DELETE /api/v2/sbom/{id}` behavior (204 / 404 / 409) is unchanged

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] Extend the cascade test (`test_delete_sbom_cascades_to_join_tables`) to also assert that related `sbom_advisory` rows have `deleted_at` set, and that the SBOM, package and advisory timestamps are equal

## Review Context
- **PR comment:** https://github.com/trustify/trustify-backend/pull/744, comment id 30001 by reviewer-a (review 20001, CHANGES_REQUESTED)
- **File/line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
