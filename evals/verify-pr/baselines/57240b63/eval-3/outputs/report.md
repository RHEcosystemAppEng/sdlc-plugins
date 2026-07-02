# PR Verification Report

**Task**: TC-9103 -- Add SBOM deletion endpoint
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Review state**: CHANGES_REQUESTED (reviewer-a)

---

## Summary Table

| Domain | Check | Result |
|---|---|---|
| Intent Alignment | Scope Containment | PASS |
| Intent Alignment | Diff Size | PASS |
| Intent Alignment | Commit Traceability | PASS |
| Security | Sensitive Pattern Scan | PASS |
| Correctness | CI Status | PASS |
| Correctness | Acceptance Criteria | PASS (8/8) |
| Correctness | Verification Commands | N/A |
| Style/Conventions | Convention Upgrade | NO UPGRADE |
| Style/Conventions | Repetitive Test Detection | PASS |
| Style/Conventions | Test Documentation | PASS |
| Style/Conventions | Eval Quality | N/A |
| Style/Conventions | Test Change Classification | ADDITIVE |

## Review Comment Summary

| Comment ID | File | Classification | Sub-task |
|---|---|---|---|
| 30001 | `sbom/service/sbom.rs` | Code Change Request | YES |
| 30002 | `m0042_sbom_soft_delete/mod.rs` | Suggestion | NO |
| 30003 | `sbom/endpoints/mod.rs` | Nit | NO |
| 30004 | `sbom/endpoints/get.rs` | Question | NO |

**Sub-tasks created**: 1 (subtask-30001.md)

---

## Intent Alignment

### Scope Containment: PASS

All modified and created files are within the scope defined by the task description:

- `entity/src/sbom.rs` -- listed in Files to Modify (add `deleted_at` column)
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- listed in Files to Create (migration)
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- listed in Files to Modify (register DELETE route)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- listed in Files to Modify (filter soft-deleted)
- `modules/fundamental/src/sbom/service/sbom.rs` -- listed in Files to Modify (soft-delete logic)
- `tests/api/sbom_delete.rs` -- listed in Files to Create (integration tests)

No files outside the task scope were modified. One file listed in Files to Modify (`modules/fundamental/src/sbom/endpoints/get.rs`) does not appear in the diff, which is noted by review comment 30004 -- the `include_deleted` parameter support for GET by ID is not yet implemented.

### Diff Size: PASS

The diff adds approximately 100 lines across 6 files. This is appropriately sized for a single endpoint feature with migration, service logic, endpoint handler, and integration tests.

### Commit Traceability: PASS

PR #744 is linked to Jira task TC-9103. The task status is "In Review" which is consistent with a PR awaiting review feedback.

---

## Security

### Sensitive Pattern Scan: PASS

No hardcoded credentials, API keys, tokens, secrets, or sensitive configuration values detected in the diff. The changes involve:
- Database schema changes (migration)
- Entity model updates
- Service logic for soft-delete operations
- HTTP endpoint handlers
- Integration tests

No security-sensitive patterns found.

---

## Correctness

### CI Status: PASS

All CI checks pass (per context provided).

### Acceptance Criteria: PASS (8/8)

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | DELETE sets `deleted_at` on the SBOM record | PASS | `soft_delete` method in `sbom.rs` sets `DeletedAt` via `Expr::value(now)` |
| 2 | DELETE returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` |
| 3 | DELETE returns 404 for non-existent SBOM | PASS | `ok_or(AppError::NotFound(...))` when SBOM not found |
| 4 | DELETE returns 409 Conflict if already deleted | PASS | `if sbom.deleted_at.is_some()` returns `AppError::Conflict(...)` |
| 5 | GET /api/v2/sbom excludes soft-deleted by default | PASS | `list` method filters `DeletedAt.is_null()` when `include_deleted` is false |
| 6 | GET with `include_deleted=true` includes soft-deleted | PASS | `list` method skips the filter when `include_deleted` is true |
| 7 | Related sbom_package and sbom_advisory cascade-updated | PASS | `soft_delete` updates both `sbom_package` and `sbom_advisory` rows |
| 8 | Migration adds `deleted_at` column with NULL default | PASS | Migration adds `.timestamp_with_time_zone().null()` column |

### Verification Commands: N/A

No verification commands were specified in the task description. The test file covers all acceptance criteria scenarios.

---

## Style/Conventions

### Convention Upgrade: NO UPGRADE

Review comment 30002 (suggestion to add an index on `deleted_at`) was evaluated for convention upgrade eligibility. The repository structure includes a `CONVENTIONS.md` file, but no convention content was available in the fixture data to determine whether a project convention mandates database indexes on nullable filter columns. Without an applicable convention backing an upgrade, comment 30002 remains classified as a suggestion and does not trigger sub-task creation.

### Repetitive Test Detection: PASS

The five test functions in `tests/api/sbom_delete.rs` each test a distinct scenario:
1. `test_delete_sbom_returns_204` -- happy path deletion and list exclusion
2. `test_delete_nonexistent_sbom_returns_404` -- error case for missing SBOM
3. `test_delete_already_deleted_sbom_returns_409` -- error case for double deletion
4. `test_list_sboms_include_deleted` -- include_deleted parameter behavior
5. `test_delete_sbom_cascades_to_join_tables` -- cascade update verification

No repetitive or redundant test patterns detected.

### Test Documentation: PASS

All test functions include doc comments (`///`) that clearly describe what each test verifies. Tests follow the Given/When/Then pattern with inline comments.

### Eval Quality: N/A

No eval result reviews exist for this PR.

### Test Change Classification: ADDITIVE

The test file `tests/api/sbom_delete.rs` is entirely new (created from `/dev/null`). No existing tests were modified or removed. All test changes are purely additive.

---

## Review Comments Detail

### Comment 30001 -- Code Change Request
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Reviewer**: reviewer-a
**Issue**: The `soft_delete` method executes three independent UPDATE statements without transaction wrapping. If one fails after others succeed, the database is left in an inconsistent state.
**Action**: Sub-task created (subtask-30001.md) to wrap operations in a database transaction.

### Comment 30002 -- Suggestion
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Reviewer**: reviewer-a
**Issue**: Suggests adding a partial index on `deleted_at` for query performance.
**Action**: No sub-task. This is a performance optimization suggestion with no backing convention. The PR author may choose to adopt it.

### Comment 30003 -- Nit
**File**: `modules/fundamental/src/sbom/endpoints/mod.rs`, line 18
**Reviewer**: reviewer-a
**Issue**: The `.context("SBOM not found")` message is misleading in error logs since the actual 404 is handled by `ok_or`. Suggests changing to `"Failed to fetch SBOM"`.
**Action**: No sub-task. Minor cosmetic feedback.

### Comment 30004 -- Question
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Reviewer**: reviewer-a
**Issue**: Asks whether direct GET returning soft-deleted SBOMs without `include_deleted=true` is intentional, since `get.rs` does not filter by `deleted_at`.
**Action**: No sub-task. Requires clarification from the PR author. Note: the task description mentions `get.rs` should support `include_deleted` parameter, suggesting this may be a gap.

---

## Outcome

**Verdict**: CHANGES REQUESTED

One code change request (comment 30001: transaction wrapping) requires action before the PR can be merged. A sub-task has been created to address it. The reviewer's question (comment 30004) about GET endpoint behavior for deleted SBOMs also warrants a response from the PR author, as the task description lists `get.rs` in Files to Modify but it does not appear in the diff.
