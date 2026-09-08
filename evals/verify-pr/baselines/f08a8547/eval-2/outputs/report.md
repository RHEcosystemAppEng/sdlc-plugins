## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | Missing task-required file: `tests/api/advisory_summary.rs` is listed in Files to Create but absent from the PR diff |
| Diff Size | PASS | 2 files changed; proportionate to a query parameter addition across endpoint and service layers |
| Commit Traceability | PASS | Commit references task TC-9102 |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met; 3 criteria failed (threshold filtering logic, invalid input validation, threshold_applied field) |
| Test Quality | N/A | No test files in PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

Three critical gaps prevent this PR from satisfying the task requirements:

---

### Scope Containment -- FAIL

**Unimplemented files:**
- `tests/api/advisory_summary.rs` -- listed in the task's "Files to Create" section but entirely absent from the PR diff. This file should contain integration tests for threshold filtering (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM ID).

**PR files vs Task files:**
| Category | Files |
|----------|-------|
| Task: Files to Modify | `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/service/advisory.rs` |
| Task: Files to Create | `tests/api/advisory_summary.rs` |
| PR: Files changed | `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/service/advisory.rs` |
| Missing from PR | `tests/api/advisory_summary.rs` |

---

### Acceptance Criteria -- FAIL (3 of 6 met)

| # | Criterion | Result | Gap |
|---|-----------|--------|-----|
| 1 | threshold=high returns critical and high only | FAIL | Filtering logic comparison is inverted (`threshold_idx <= N` instead of `N <= threshold_idx`); medium and low counts are incorrectly included |
| 2 | Without threshold returns all counts (backward compatible) | PASS | `None => summary` correctly returns unmodified response |
| 3 | threshold=invalid returns 400 Bad Request | FAIL | `.unwrap_or(0)` silently accepts invalid threshold values and treats them as "critical" instead of returning 400 |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | Array `["critical", "high", "medium", "low"]` correctly defines the ordering |
| 5 | Response includes threshold_applied boolean field | FAIL | `threshold_applied` field is entirely absent from the response struct; neither the `AdvisorySummary` struct nor the filtering logic includes this field |
| 6 | 404 for non-existent SBOM IDs (existing behavior) | PASS | Existing `SbomService::fetch()` error handling is preserved |

#### Detailed gap analysis

**Criterion 1 -- FAIL: Filtering logic is inverted**

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtering conditions use `threshold_idx <= N` where N is the hardcoded severity position. This comparison is backwards. For threshold=high (idx=1):
- `high: if 1 <= 1` -- true (correct, high should be included)
- `medium: if 1 <= 2` -- true (WRONG, medium should be excluded)
- `low: if 1 <= 3` -- true (WRONG, low should be excluded)

The correct condition should check `N <= threshold_idx` (severity position at or above threshold).

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, making the total inconsistent with individual filtered counts.

**Criterion 3 -- FAIL: Invalid threshold values silently accepted**

The code uses `.unwrap_or(0)` when looking up the threshold value in the severity array:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like "invalid" is provided, `.position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (critical). The task explicitly requires returning 400 Bad Request for invalid values and the implementation notes state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

**Criterion 5 -- FAIL: threshold_applied boolean field missing**

The `AdvisorySummary` struct returned in the response does not include a `threshold_applied` boolean field. The constructed struct contains only `critical`, `high`, `medium`, `low`, and `total` fields. Neither the struct definition (in `advisory/model/summary.rs`, unchanged) nor the filtering logic adds this field. API consumers have no way to determine whether the returned counts are filtered or unfiltered.

---

### Sensitive Patterns -- PASS

No secrets, API keys, credentials, private keys, or other sensitive patterns detected in the added lines. The diff adds only application logic (struct definitions, query parameter handling, filtering).

### CI Status -- PASS

All CI checks pass.

### Test Quality -- N/A

No test files are present in the PR diff. The required test file `tests/api/advisory_summary.rs` was not created. Eval Quality: N/A (no eval result reviews on this PR).

### Test Change Classification -- N/A

No test files are present in the PR diff. No test additions, modifications, or deletions to classify.

### Verification Commands -- N/A

No verification commands were specified in the task description.
