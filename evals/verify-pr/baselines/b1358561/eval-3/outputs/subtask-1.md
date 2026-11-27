# Sub-task 1 (would be created via jira.create_issue)

- **Issue Type:** Sub-task
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Issue link:** sub-task **Blocks** TC-9103 (`jira.create_issue_link(type="Blocks", inwardIssue=<sub-task-id>, outwardIssue=TC-9103)`)

---

## Repository
trustify-backend

## Target Branch
The PR #744 head branch (the existing TC-9103 PR branch). Add commits to that branch; do not open a new PR.

## Description
`SbomService::soft_delete` currently issues three independent `update_many()` statements, against `sbom`, `sbom_package` and `sbom_advisory`, each executed directly on `self.db`. If a later statement fails after an earlier one succeeds (e.g. the `sbom_advisory` update fails after `sbom` and `sbom_package` were updated), the database is left inconsistent: the SBOM is marked deleted, but some join-table rows are not. Run all three updates inside a single database transaction so the soft-delete cascade is atomic: either every row is marked with the same `deleted_at` timestamp, or none is.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — wrap the three `update_many()` calls in `soft_delete` in one transaction and execute each against the transaction handle instead of `self.db`
- `tests/api/sbom_delete.rs` — extend cascade coverage to assert `sbom_advisory` rows are marked as well as `sbom_package` rows

## Implementation Notes
- In `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete`, use SeaORM's transaction support, as the reviewer suggested: `self.db.transaction(|txn| { ... })`, or `let txn = self.db.begin().await?; ...; txn.commit().await?;`. Pass `txn` to each `.exec(...)` call in place of `&self.db`.
- Compute `let now = chrono::Utc::now();` once, before the transaction, so all three tables get the identical timestamp (as today).
- Keep the existing filters: `sbom::Column::Id.eq(id)`, `sbom_package::Column::SbomId.eq(id)`, `sbom_advisory::Column::SbomId.eq(id)`, together with `col_expr(<Column>::DeletedAt, Expr::value(now))`.
- Propagate errors with `?` so any failure rolls the transaction back (drop without commit, or `Err` returned from the closure). The handler in `modules/fundamental/src/sbom/endpoints/mod.rs::delete_sbom` already wraps service errors with `.context("Failed to soft-delete SBOM")` and needs no change.
- Do not change the endpoint contract: 204 on success, 404 if not found, 409 if already deleted.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete` — the method being made transactional
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::list` — existing service method showing how queries are executed against `self.db`
- `tests/api/sbom_delete.rs::test_delete_sbom_cascades_to_join_tables` — existing cascade test and `ctx.seed_sbom_with_relations` fixture helper to extend

## Acceptance Criteria
- [ ] `SbomService::soft_delete` executes the `sbom`, `sbom_package` and `sbom_advisory` updates inside a single database transaction
- [ ] All three updates are executed against the transaction handle, not `self.db`
- [ ] A failure in any of the three updates leaves no rows modified (transaction rolled back)
- [ ] On success, `sbom`, `sbom_package` and `sbom_advisory` rows for the SBOM share the same `deleted_at` timestamp
- [ ] `DELETE /api/v2/sbom/{id}` still returns 204 / 404 / 409 as before

## Test Requirements
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` (or add a sibling test) to assert that related `sbom_advisory` rows have `deleted_at` set, in addition to `sbom_package` rows
- [ ] Assert that the `sbom`, `sbom_package` and `sbom_advisory` rows share the same `deleted_at` value after deletion
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Review Context
- **PR:** https://github.com/trustify/trustify-backend/pull/744
- **Review comment:** id 30001 by reviewer-a (review 20001, CHANGES_REQUESTED)
- **Location:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT side)
- **Original comment:**
  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.
- **Classification:** code change request

## Target PR
https://github.com/trustify/trustify-backend/pull/744

---

_Eval coverage propagation: not applicable. No `plugins/<plugin>/skills/<skill>/SKILL.md` file is in Files to Modify._
