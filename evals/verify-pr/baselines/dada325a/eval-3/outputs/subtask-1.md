# Sub-task 1 (would be created under TC-9103)

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
`SbomService::soft_delete` runs three separate `UPDATE` statements against `sbom`, `sbom_package`, and `sbom_advisory`, all on `self.db`, with no transaction. If a later statement fails (for example, the `sbom_advisory` update) after an earlier one succeeded, the database is left inconsistent: the SBOM is marked deleted while some of its join-table rows are not. Run all three updates inside one database transaction so the soft-delete cascade is atomic. Either every row gets the same `deleted_at` timestamp or none do.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many()` calls in `soft_delete` in a single transaction and run each `exec` on the transaction handle instead of `self.db`
- `tests/api/sbom_delete.rs` — extend the cascade test to also assert `sbom_advisory` rows are marked deleted

## Implementation Notes
- Use SeaORM's transaction API on the service's connection, e.g. `self.db.transaction::<_, (), DbErr>(|txn| Box::pin(async move { ... })).await`, or `let txn = self.db.begin().await?; ...; txn.commit().await?;`. Pass `txn` to each `.exec(...)` call in place of `&self.db`.
- Compute `let now = chrono::Utc::now();` once, before the transaction, and use the same value for all three `col_expr(..., Expr::value(now))` updates so the timestamps stay identical.
- Keep the `SbomService::soft_delete(&self, id: i64) -> Result<()>` signature unchanged so the `delete_sbom` handler in `modules/fundamental/src/sbom/endpoints/mod.rs` does not need to change.
- Map transaction errors through the existing `Result`/`AppError` handling with `.context()` wrapping, following the repository's error-handling convention (`common/src/error.rs`).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — the existing cascade logic to wrap. Its three `update_many()` statements stay the same.
- `common/src/error.rs::AppError` — the existing error type for propagating transaction failures

## Acceptance Criteria
- [ ] `SbomService::soft_delete` runs the `sbom`, `sbom_package`, and `sbom_advisory` updates inside a single database transaction
- [ ] If any of the three updates fails, the transaction rolls back and no rows get `deleted_at`
- [ ] On success, all three tables' affected rows share the same `deleted_at` timestamp
- [ ] `DELETE /api/v2/sbom/{id}` behavior (204 / 404 / 409) is unchanged

## Test Requirements
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` (or add a test) to assert that both `sbom_package` and `sbom_advisory` rows for the deleted SBOM have `deleted_at` set

## Review Context
- **PR:** https://github.com/trustify/trustify-backend/pull/744
- **Comment ID:** 30001 (review 20001, reviewer-a)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
