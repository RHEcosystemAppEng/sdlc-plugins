# Verification Report: PR #744 -- Add SBOM deletion endpoint

**Task**: TC-9103
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Review State**: CHANGES_REQUESTED (reviewer-a)
**CI Status**: All checks pass

---

## Summary Table

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | ACTION REQUIRED | 4 review comments classified; 1 code change request triggers sub-task creation (comment 30001: transaction wrapping) |
| Root-Cause Investigation | N/A | Not applicable in eval context |
| Scope Containment | PASS | All files in the diff match the task's Files to Modify and Files to Create sections |
| Sensitive Patterns | PASS | No passwords, API keys, private keys, or other sensitive patterns found in the diff |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | PASS | All 8 acceptance criteria met -- DELETE endpoint, 204/404/409 responses, soft-delete logic, cascade updates, list filtering, include_deleted parameter, and migration all implemented |
| Test Quality | PASS | Repetitive Test Detection: PASS. Test Documentation: PASS. Eval Quality: N/A -- no eval result reviews exist in the PR; 3-criteria detection found no matches (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) |
| Test Change Classification | ADDITIVE | Only new test files were added (tests/api/sbom_delete.rs is a new file); no existing tests modified or deleted |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: PASS (with action items)

All acceptance criteria are satisfied in the diff. One code change request from reviewer feedback requires a sub-task: wrapping the soft-delete operations in a database transaction for atomicity (comment 30001). The remaining review comments are classified as suggestion (30002), nit (30003), and question (30004) and do not require sub-tasks.

---

## Domain Findings

### Intent Alignment

**Scope Containment -- PASS**

All files in the PR diff are accounted for in the task specification:
- Modified: `modules/fundamental/src/sbom/endpoints/mod.rs` (Files to Modify)
- Modified: `modules/fundamental/src/sbom/endpoints/list.rs` (Files to Modify)
- Modified: `modules/fundamental/src/sbom/service/sbom.rs` (Files to Modify)
- Modified: `entity/src/sbom.rs` (Files to Modify)
- Created: `migration/src/m0042_sbom_soft_delete/mod.rs` (Files to Create)
- Created: `tests/api/sbom_delete.rs` (Files to Create)

No out-of-scope files. Note: `modules/fundamental/src/sbom/endpoints/get.rs` was listed as a file to modify but is not modified in this PR. Reviewer comment 30004 asks about this gap. The task description says the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", implying `get.rs` should be updated. However, the current behavior -- GET-by-ID always returning the SBOM regardless of soft-delete status -- could be considered acceptable for direct lookups. This is covered by the reviewer's question (classified as QUESTION, no sub-task).

**Diff Size -- PASS**

Diff size is appropriate for the scope of a soft-delete endpoint feature.

**Commit Traceability -- PASS**

Commits reference TC-9103.

### Security

**Sensitive Pattern Scan -- PASS**

No sensitive patterns detected. No credentials, secrets, API keys, `.env` files, or private keys in the diff.

### Correctness

**CI Status -- PASS**

All CI checks pass.

**Acceptance Criteria -- PASS**

All 8 acceptance criteria verified against the diff:

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` in `sbom.rs` uses `update_many` with `col_expr(sbom::Column::DeletedAt, Expr::value(now))` |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | Handler uses `.ok_or(AppError::NotFound("SBOM not found".into()))` |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted | PASS | Handler checks `sbom.deleted_at.is_some()` and returns `AppError::Conflict(...)` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list` applies `.filter(sbom::Column::DeletedAt.is_null())` when `include_deleted` is false |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `list` skips the `DeletedAt.is_null()` filter when `include_deleted` is true |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` updates both join tables with the same `deleted_at` timestamp |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration uses `ColumnDef::new(Sbom::DeletedAt).timestamp_with_time_zone().null()` |

### Style/Conventions

**Repetitive Test Detection -- PASS**

All 5 test functions cover distinct scenarios without duplication: 204 success, 404 not found, 409 conflict, include_deleted list, and cascade to join tables.

**Test Documentation -- PASS**

Test functions have descriptive names and doc comments explaining the scenario under test.

**Eval Quality -- N/A**

No eval result reviews exist in the PR. No reviews match the 3-criteria detection heuristic (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals).

**Test Change Classification -- ADDITIVE**

Only new test file added (`tests/api/sbom_delete.rs`). No existing test files modified or deleted.

**Convention Upgrade Eligibility -- Comment 30002**

Comment 30002 (index suggestion on `deleted_at` column) was evaluated for convention upgrade eligibility. The reviewer uses suggestive language ("should also add", "would help", "Something like"), which under standard classification rules places this as a suggestion. Convention upgrade was assessed as follows:

- **CONVENTIONS.md existence**: The repository structure shows a `CONVENTIONS.md` file at the root of `trustify-backend/`. However, the fixture data does not include its contents.
- **Documented convention check**: No documented project convention in the available fixture data explicitly requires indexes on columns used in WHERE clauses, or mandates index creation alongside column additions in migrations.
- **Codebase pattern check**: Without access to the actual CONVENTIONS.md content or other migration files to verify a consistent pattern of index creation, there is insufficient evidence to confirm an established convention.
- **Upgrade decision**: The suggestion is NOT upgraded. While adding a partial index is a database best practice and the reviewer's reasoning is sound, the convention upgrade mechanism requires a documented project convention that can be cited as evidence. No such documentation is present in the fixture data. The comment remains classified as SUGGESTION with no sub-task created.

---

## Review Comments Summary

| ID | File | Classification | Sub-task Created |
|----|------|---------------|-----------------|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs` | Code change request -- wrap updates in transaction | Yes (subtask-30001.md) |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs` | Suggestion -- add partial index on deleted_at | No |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs` | Nit -- rename context message for clarity | No |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs` | Question -- GET behavior for deleted SBOMs | No |

Detailed classification reasoning is in `review-30001.md` through `review-30004.md`.

---

## Sub-tasks Created

1. **subtask-30001.md** -- Wrap `soft_delete` operations in a database transaction to prevent inconsistent state on partial failure.

---

## Findings

### Critical
- **Transaction safety** (comment 30001): The `soft_delete` method executes three independent UPDATE statements without a transaction. A failure in any intermediate statement leaves the database in an inconsistent partially-deleted state. Sub-task created.

### Observation
- **Index suggestion** (comment 30002): The migration adds a `deleted_at` column but does not create an index. Since every default list query filters by `deleted_at IS NULL`, this could degrade list endpoint performance as data grows. Classified as suggestion -- no documented project convention supports upgrade. No sub-task created.
- **`get.rs` not modified**: The task description specifies adding `include_deleted` support to the GET-by-ID endpoint, but the PR does not modify `get.rs`. The reviewer asked about this (comment 30004). The team should clarify whether this is intentional.
- **Context message nit** (comment 30003): The `.context("SBOM not found")` message is slightly misleading since it wraps a database fetch error, not a not-found condition. Minor cosmetic improvement, no sub-task warranted.

---
*This comment was AI-generated by [sdlc-workflow/verify-pr](https://github.com/mrizzi/sdlc-plugins).*
