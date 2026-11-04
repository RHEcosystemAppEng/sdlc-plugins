# Sub-task for Review Comment 30001

**Jira create_issue parameters**

- **Project:** TC
- **Issue Type:** Sub-task (issueTypeName `Sub-task`, not a standalone Task, so it sits under the parent task)
- **Parent:** TC-9103
- **Summary:** Wrap SBOM soft-delete cascade updates in a single database transaction
- **Labels:** `ai-generated-jira`, `review-feedback`
- **Issue link:** `jira.create_issue_link(type="Blocks", inwardIssue=<this sub-task>, outwardIssue=TC-9103)`

**Description**

---

## Repository
trustify-backend

## Target Branch
main

## Description
`SbomService::soft_delete` runs three separate UPDATE statements:
1. set `deleted_at` on the `sbom` row
2. cascade to `sbom_package`
3. cascade to `sbom_advisory`

Each one executes directly against `self.db`, with no shared transaction. If a later UPDATE fails after an earlier one succeeds, the database is left inconsistent. Because the `sbom` row is already marked deleted at that point, a retry of `DELETE /api/v2/sbom/{id}` returns 409 Conflict and the cascade can never be completed.

Make the three updates atomic by running them inside a single database transaction. Either all three tables are updated with the same `deleted_at` timestamp, or none are.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs`: wrap the three `update_many()` calls in `SbomService::soft_delete` in one transaction and execute each against the transaction handle instead of `self.db`
- `tests/api/sbom_delete.rs`: extend cascade coverage so `sbom_advisory` rows are asserted too, not just `sbom_package`

## Implementation Notes
- Change only `SbomService::soft_delete` in `modules/fundamental/src/sbom/service/sbom.rs`. The handler `delete_sbom` in `modules/fundamental/src/sbom/endpoints/mod.rs` keeps its signature and behaviour (204 / 404 / 409).
- Follow the reviewer's guidance: wrap the three operations in `self.db.transaction(|txn| { ... })`, the SeaORM `TransactionTrait` API, and pass `txn` to each `.exec(...)` call in place of `&self.db`.
  - Alternatively, use `let txn = self.db.begin().await?;` and finish with `txn.commit().await?`.
  - Either way, an error on any statement must roll back all of them.
- Compute `let now = chrono::Utc::now();` once, before the transaction, and use the same value for all three `col_expr(..., Expr::value(now))` calls, as the existing code does.
- Keep the existing `.context()` error-wrapping style used by handlers. Errors from the transaction should still propagate to `AppError` through the handler's `.context("Failed to soft-delete SBOM")`.
- Existing symbols involved:
  - `sbom::Entity` / `sbom::Column::DeletedAt` (`entity/src/sbom.rs`)
  - `sbom_package::Entity` / `sbom_package::Column::{SbomId, DeletedAt}` (`entity/src/sbom_package.rs`)
  - `sbom_advisory::Entity` / `sbom_advisory::Column::{SbomId, DeletedAt}` (`entity/src/sbom_advisory.rs`)

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::soft_delete`: the existing method to refactor. Its three `update_many` statements stay the same and only the executor changes.
- `modules/ingestor/src/graph/sbom/mod.rs`: SBOM ingestion writes the SBOM and links packages across several tables. Check it for an existing transaction pattern to mirror before introducing a new style.
- `tests/api/sbom_delete.rs::test_delete_sbom_cascades_to_join_tables`: existing cascade test to extend with an advisory assertion.

## Acceptance Criteria
- [ ] `SbomService::soft_delete` runs the `sbom`, `sbom_package`, and `sbom_advisory` updates inside a single database transaction
- [ ] All three updates use the transaction handle, not `self.db` directly
- [ ] If any of the three updates fails, none of the changes are persisted (the transaction rolls back)
- [ ] All three tables receive the same `deleted_at` timestamp on success
- [ ] Existing DELETE behaviour is unchanged: 204 on success, 404 when not found, 409 when already deleted

## Test Requirements
- [ ] Extend `test_delete_sbom_cascades_to_join_tables` (or add a sibling test with a `///` doc comment) to assert that related `sbom_advisory` rows also have `deleted_at` set after deletion
- [ ] Existing tests in `tests/api/sbom_delete.rs` continue to pass

## Review Context
- **PR:** https://github.com/trustify/trustify-backend/pull/744
- **Review comment ID:** 30001 (review 20001, reviewer-a, CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Original comment:**

  > The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

- **Classification:** code change request

## Target PR
https://github.com/trustify/trustify-backend/pull/744

Add the fix as commits on the existing PR branch. Do not open a new PR.

## Dependencies
- Depends on: TC-9103 (parent task; the fix lands on its PR branch)
