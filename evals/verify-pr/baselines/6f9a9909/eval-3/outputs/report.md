# Verification Report: PR #744 — TC-9103

**Task:** TC-9103 — Add SBOM deletion endpoint
**PR:** https://github.com/trustify/trustify-backend/pull/744
**Repository:** trustify-backend

---

## Review Feedback

**Status: WARN**

One reviewer (reviewer-a) submitted a CHANGES_REQUESTED review with four inline comments. Classification results:

| ID | Comment | Classification | Sub-task |
|---|---|---|---|
| 30001 | Transaction wrapping for `soft_delete` | code change request | Yes — subtask-30001 |
| 30002 | Add index on `deleted_at` column | suggestion | No |
| 30003 | Nit: misleading `.context()` message | nit | No |
| 30004 | Question about GET behavior for deleted SBOMs | question | No |

**Sub-tasks created:** 1

- **subtask-30001**: Wrap the three UPDATE statements in `soft_delete` inside a database transaction to prevent inconsistent state on partial failure.

**Comment 30002 — Convention upgrade evaluation:** The index suggestion was evaluated for convention upgrade eligibility. No documented project convention (CONVENTIONS.md content not available in fixture data) or demonstrated codebase pattern requires indexes on new nullable columns or soft-delete columns. The suggestion remains classified as a suggestion and does not produce a sub-task.

See individual review classification files (review-30001.md through review-30004.md) for detailed reasoning.

---

## Scope Containment

**Status: PASS**

All files changed in the PR are within the scope defined by TC-9103:

| File | Task Scope | Status |
|---|---|---|
| `entity/src/sbom.rs` | Files to Modify | Modified |
| `migration/src/m0042_sbom_soft_delete/mod.rs` | Files to Create | Created |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Files to Modify | Modified |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Files to Modify | Modified |
| `modules/fundamental/src/sbom/service/sbom.rs` | Files to Modify | Modified |
| `tests/api/sbom_delete.rs` | Files to Create | Created |

**Note:** `modules/fundamental/src/sbom/endpoints/get.rs` was listed in Files to Modify but has no changes in the PR. The task description mentions adding `include_deleted` parameter support to `get.rs`. This is addressed by reviewer comment 30004 (question), which asks about the GET behavior for deleted SBOMs. No out-of-scope files were modified.

---

## Diff Size

**Status: PASS**

Approximate changes: +130 lines added, -2 lines removed across 6 files. The diff is appropriately sized for a single task adding a new endpoint with supporting migration and tests.

---

## Commit Traceability

**Status: N/A**

Commit-level traceability cannot be verified from the available fixture data.

---

## Sensitive Patterns

**Status: PASS**

No secrets, credentials, API keys, tokens, or other sensitive data patterns detected in the diff. No `.env` files, certificate files, or credential configurations are included.

---

## CI Status

**Status: PASS**

All CI checks pass (per eval input).

---

## Acceptance Criteria

**Status: PASS**

All acceptance criteria from TC-9103 are addressed by the PR diff:

- [x] `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record — implemented in `soft_delete` method
- [x] `DELETE /api/v2/sbom/{id}` returns 204 No Content on success — `Ok(StatusCode::NO_CONTENT)` in handler
- [x] `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM — `AppError::NotFound` when fetch returns None
- [x] `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted — `AppError::Conflict` when `deleted_at.is_some()`
- [x] `GET /api/v2/sbom` excludes soft-deleted SBOMs by default — filter `DeletedAt.is_null()` in list method
- [x] `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs — conditional filter based on `include_deleted` param
- [x] Related `sbom_package` and `sbom_advisory` rows are cascade-updated — `update_many` on both tables in `soft_delete`
- [x] Migration adds `deleted_at` column with NULL default to `sbom` table — migration uses `.null()` on column definition

---

## Test Quality

**Status: PASS**

All test requirements from TC-9103 are covered by `tests/api/sbom_delete.rs`:

| Test Requirement | Test Function | Status |
|---|---|---|
| DELETE returns 204 and SBOM excluded from list | `test_delete_sbom_returns_204` | Covered |
| DELETE on non-existent SBOM returns 404 | `test_delete_nonexistent_sbom_returns_404` | Covered |
| DELETE on already-deleted SBOM returns 409 | `test_delete_already_deleted_sbom_returns_409` | Covered |
| GET with `include_deleted=true` returns deleted SBOMs | `test_list_sboms_include_deleted` | Covered |
| Cascade update marks related join table rows | `test_delete_sbom_cascades_to_join_tables` | Covered |

---

## Test Change Classification

**Status: ADDITIVE**

- `tests/api/sbom_delete.rs` is a new file (created, not modified). All test changes are purely additive — new tests for new functionality. No existing tests were modified or removed.

---

## Eval Quality

**Status: N/A**

No eval result reviews exist for this verification.

---

## Verification Commands

The following commands can be used to verify the implementation in the target repository:

- `cargo test --test api sbom_delete` — run the new SBOM deletion integration tests
- `cargo test` — run the full test suite to confirm no regressions

---

## Root-Cause Investigation

Not required. The review feedback identified one code change request (transaction wrapping) which has been captured as a sub-task (subtask-30001). The remaining comments are a suggestion, a nit, and a question — none requiring sub-tasks.

---

## Summary

| Check | Status |
|---|---|
| Scope Containment | PASS |
| Diff Size | PASS |
| Commit Traceability | N/A |
| Sensitive Patterns | PASS |
| CI Status | PASS |
| Acceptance Criteria | PASS |
| Test Quality | PASS |
| Test Change Classification | ADDITIVE |
| Review Feedback | WARN |
| Eval Quality | N/A |
| **Overall** | **WARN** |

**Overall: WARN** — The PR passes all standard verification checks. One code change request (comment 30001 — transaction wrapping) requires a follow-up sub-task before the PR can be merged. The sub-task has been created as subtask-30001.
