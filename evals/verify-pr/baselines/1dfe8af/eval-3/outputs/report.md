# Verification Report: PR #744

**Task**: [TC-9103](https://redhat.atlassian.net/browse/TC-9103) — Add SBOM deletion endpoint
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Verified**: 2026-06-26

---

## 1. Scope Containment

**Result: PASS**

All files changed in the PR are within the scope defined by the task description.

| PR File | Task Section | In Scope |
|---|---|---|
| `entity/src/sbom.rs` | Files to Modify | Yes |
| `migration/src/m0042_sbom_soft_delete/mod.rs` | Files to Create | Yes |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Files to Modify | Yes |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Files to Modify | Yes |
| `modules/fundamental/src/sbom/service/sbom.rs` | Files to Modify | Yes |
| `tests/api/sbom_delete.rs` | Files to Create | Yes |

Files listed in the task but not modified in the PR:
- `modules/fundamental/src/sbom/endpoints/get.rs` — listed in Files to Modify for `include_deleted` parameter support. The diff does not show changes to this file. However, reviewer comment 30004 raises this as a question about whether direct GET should filter by `deleted_at`. This is a design clarification, not a scope violation.

No files outside the task scope were modified.

## 2. Sensitive Patterns

**Result: PASS**

Scanned all added lines in the diff for:
- Hardcoded secrets, API keys, tokens: None found
- Credentials or passwords: None found
- Private keys or certificates: None found
- Internal URLs or connection strings: None found

## 3. CI Status

**Result: PASS**

All CI checks pass.

## 4. Acceptance Criteria

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` method in `sbom.rs` sets `deleted_at` to `chrono::Utc::now()` via `update_many` on the sbom entity |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | Handler uses `ok_or(AppError::NotFound("SBOM not found".into()))` when fetch returns None |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted | PASS | Handler checks `sbom.deleted_at.is_some()` and returns `Err(AppError::Conflict(...))` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list` method adds `.filter(sbom::Column::DeletedAt.is_null())` when `include_deleted` is false (the default) |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `list` method skips the `is_null` filter when `include_deleted` is true |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` method runs `update_many` on both `sbom_package` and `sbom_advisory` entities, setting `deleted_at` to the same timestamp |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration `m0042_sbom_soft_delete` adds `deleted_at` as `timestamp_with_time_zone().null()` |

## 5. Test Change Classification

**Result: ADDITIVE**

The PR adds one new test file:
- `tests/api/sbom_delete.rs` (new file, 62 lines)

No existing test files were modified. All test changes are purely additive — new test coverage for the new deletion endpoint.

Tests cover:
- DELETE returns 204 and SBOM excluded from list
- DELETE on non-existent SBOM returns 404
- DELETE on already-deleted SBOM returns 409
- GET with `include_deleted=true` returns deleted SBOMs
- Cascade update marks related join table rows

## 6. Eval Quality

**Result: N/A**

No eval result reviews exist. The 3-criteria detection found no matches.

## 7. Review Feedback

**Result: WARN — 1 code change request requires sub-task**

### Review Summary

The PR has 1 review from **reviewer-a** with state CHANGES_REQUESTED and 4 inline comments.

| Comment ID | File | Classification | Sub-task |
|---|---|---|---|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs` | Code change request | Yes — wrap `soft_delete` operations in a database transaction |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs` | Suggestion | No |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs` | Nit | No |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs` | Question | No |

### Sub-tasks Created

1. **Sub-task for comment 30001**: Wrap `soft_delete` UPDATE statements in a database transaction to prevent inconsistent state on partial failure. See `outputs/subtask-30001.md` for full task description.

### Comments Not Requiring Sub-tasks

- **Comment 30002** (suggestion): Reviewer suggests adding a partial index on `deleted_at`. Uses suggestive language ("should also", "would help") and no documented project convention backs an upgrade to a code change request. See `outputs/review-30002.md` for detailed reasoning.
- **Comment 30003** (nit): Reviewer notes misleading `.context()` message. Self-labeled as "Nit" with suggestive language ("Consider changing").
- **Comment 30004** (question): Reviewer asks whether direct GET returning soft-deleted SBOMs is intentional. Phrased entirely as questions ("Have you considered...", "Is that intentional?").

---

## Summary

| Check | Result |
|---|---|
| Scope Containment | PASS |
| Sensitive Patterns | PASS |
| CI Status | PASS |
| Acceptance Criteria | PASS (8/8) |
| Test Change Classification | ADDITIVE |
| Eval Quality | N/A |
| Review Feedback | WARN |

**Overall: WARN** — PR meets all acceptance criteria and passes all automated checks, but 1 code change request from reviewer feedback requires a sub-task before merge. The sub-task has been created in `outputs/subtask-30001.md`.
