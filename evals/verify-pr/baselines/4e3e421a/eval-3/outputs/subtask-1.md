# Sub-task 1 (planned — not created; eval mode)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `["ai-generated-jira", "review-feedback"]`
- **Link:** Blocks — inward: <this sub-task>, outward: TC-9103

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` currently runs three independent UPDATE statements against `self.db`: `sbom`, `sbom_package`, and `sbom_advisory`. If a later statement fails, for example the `sbom_advisory` update, the earlier updates are already committed. The SBOM is then marked deleted while some of its join-table rows are not, which leaves the soft-delete cascade inconsistent. Run all three updates inside one database transaction so the soft delete is atomic: either every row gets the same `deleted_at` timestamp, or none does.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — run the three `update_many()` calls in `soft_delete` inside a single transaction, executing each against the transaction handle instead of `self.db`

## Implementation Notes
- In `SbomService::soft_delete(&self, id: i64)` (`modules/fundamental/src/sbom/service/sbom.rs`), open a transaction on `self.db` (SeaORM `TransactionTrait`). Use either `self.db.transaction(|txn| { ... })`, as the reviewer suggested, or `let txn = self.db.begin().await?; ... txn.commit().await?;`.
- Pass `txn` instead of `&self.db` to each `.exec(...)` call for `sbom::Entity::update_many()`, `sbom_package::Entity::update_many()` and `sbom_advisory::Entity::update_many()`.
- Keep the single `chrono::Utc::now()` timestamp computed once before the transaction, so all three tables receive an identical `deleted_at` value.
- Propagate errors with `?` so a failure in any statement rolls back the whole transaction. The endpoint handler `delete_sbom` in `modules/fundamental/src/sbom/endpoints/mod.rs` already wraps the service error with `.context("Failed to soft-delete SBOM")?`, and no handler change is needed.
- Do not change the method signature or the 204/404/409 semantics of the DELETE endpoint.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — existing method to be wrapped in a transaction
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — holds the `db` connection used to start the transaction

## Acceptance Criteria
- [ ] All three UPDATE statements in `SbomService::soft_delete` (sbom, sbom_package, sbom_advisory) execute within a single database transaction
- [ ] If any of the three updates fails, none of the `deleted_at` changes are persisted (transaction rolled back)
- [ ] On success, the SBOM and all related `sbom_package` and `sbom_advisory` rows share the same `deleted_at` timestamp
- [ ] `DELETE /api/v2/sbom/{id}` continues to return 204 / 404 / 409 as before

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] Extend the cascade test (`test_delete_sbom_cascades_to_join_tables`) to also assert that related `sbom_advisory` rows have `deleted_at` set, and that the SBOM and join rows share the same timestamp

## Dependencies
- Depends on: TC-9103 — Add SBOM deletion endpoint (PR #744 branch)

## Review Context
- **Reviewer:** reviewer-a (review 20001, state CHANGES_REQUESTED)
- **Comment ID:** 30001
- **PR file/line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
