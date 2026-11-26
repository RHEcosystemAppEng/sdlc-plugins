# Sub-task 1 (would be created under TC-9103)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Link:** Blocks — inward: <this sub-task>, outward: TC-9103

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` runs three separate UPDATE statements: it sets `deleted_at` on `sbom`, then on `sbom_package`, then on `sbom_advisory`. Each one runs directly on `self.db` with no transaction. If a later statement fails, the database is left partly soft-deleted: the SBOM is marked deleted but some of its join rows are not. A retried DELETE then returns 409 Conflict, so the system cannot repair this state through the API. Make the soft-delete atomic by running all three updates in one database transaction, so they either all commit or all roll back.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — run the three `update_many()` calls in `SbomService::soft_delete` inside a single transaction
- `tests/api/sbom_delete.rs` — extend the cascade test to also check `sbom_advisory` rows and that `deleted_at` is the same timestamp across all tables

## Implementation Notes
- In `SbomService::soft_delete` (`modules/fundamental/src/sbom/service/sbom.rs`), open a transaction, as the reviewer suggested: `self.db.transaction(|txn| { ... })`. Alternatively, use SeaORM's `self.db.begin().await?` with `txn.commit().await?`. Run each `.exec(...)` against `txn` instead of `self.db`.
- Keep the single `let now = chrono::Utc::now();` timestamp. All three tables must get the same value, as required by the parent task's Implementation Notes.
- Keep the current filters: `sbom::Column::Id.eq(id)`, `sbom_package::Column::SbomId.eq(id)` and `sbom_advisory::Column::SbomId.eq(id)`. Keep the `Expr::value(now)` column expressions.
- Keep the method signature (`pub async fn soft_delete(&self, id: i64) -> Result<()>`) so that `delete_sbom` in `modules/fundamental/src/sbom/endpoints/mod.rs` needs no change. Propagate errors with `?`, as today, so a failed statement rolls back the transaction.
- Optional hardening: do the "already deleted" check and the update in the same transaction. For example, add `.filter(sbom::Column::DeletedAt.is_null())` to the `sbom` update and check `rows_affected`. This avoids a race between two concurrent DELETE requests. Keep the 404/409 semantics in the endpoint.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — the existing cascade logic to wrap. Do not rewrite it.
- `modules/fundamental/src/sbom/endpoints/mod.rs::delete_sbom` — the caller. Its 204/404/409 behavior must stay the same.

## Acceptance Criteria
- [ ] `SbomService::soft_delete` runs the `sbom`, `sbom_package` and `sbom_advisory` updates inside one database transaction
- [ ] If any of the three updates fails, no `deleted_at` value is kept on any of the three tables (full rollback)
- [ ] On success, all three tables get the same `deleted_at` timestamp
- [ ] `DELETE /api/v2/sbom/{id}` still returns 204 / 404 / 409, as before

## Test Requirements
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` in `tests/api/sbom_delete.rs` to check that `sbom_advisory` rows are also marked deleted, not just `sbom_package` rows
- [ ] Check that the `deleted_at` values on the `sbom`, `sbom_package` and `sbom_advisory` rows are equal
- [ ] Existing tests in `tests/api/sbom_delete.rs` keep passing

## Review Context
- **PR file/line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (review comment 30001 by reviewer-a, review 20001)
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Dependencies
- Depends on: TC-9103 — Add SBOM deletion endpoint (PR #744 branch; add commits to the existing PR)
