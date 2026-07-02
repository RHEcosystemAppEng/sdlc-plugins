# Verification Report: PR #743 for TC-9102

**Task**: TC-9102 -- Add severity threshold filter to advisory summary endpoint
**PR**: #743 (trustify-backend)
**Overall Result**: FAIL

---

## Summary Table

| Domain                     | Check                    | Result |
|----------------------------|--------------------------|--------|
| Review Feedback            | Review Comments          | N/A    |
| Root-Cause Investigation   | Sub-task Analysis        | N/A    |
| Intent Alignment           | Scope Containment        | FAIL   |
| Intent Alignment           | Diff Size                | WARN   |
| Intent Alignment           | Commit Traceability      | WARN   |
| Security                   | Sensitive Patterns       | PASS   |
| Correctness                | CI Status                | PASS   |
| Correctness                | Acceptance Criteria      | FAIL   |
| Style/Conventions          | Test Quality             | FAIL   |
| Style/Conventions          | Test Change Classification | N/A  |
| Correctness                | Verification Commands    | N/A    |
| Style/Conventions          | Eval Quality             | N/A    |

---

## Detailed Findings

### Review Feedback
**Result**: N/A

No review comments exist on this PR.

---

### Root-Cause Investigation
**Result**: N/A

No sub-tasks defined for TC-9102.

---

### Scope Containment
**Result**: FAIL

**Files to Modify (per task)**:
| File | In Diff? |
|------|----------|
| `modules/fundamental/src/advisory/endpoints/get.rs` | Yes |
| `modules/fundamental/src/advisory/service/advisory.rs` | Yes |

**Files to Create (per task)**:
| File | In Diff? |
|------|----------|
| `tests/api/advisory_summary.rs` | **No -- MISSING** |

The task requires creating `tests/api/advisory_summary.rs` with integration tests for threshold filtering. This file is entirely absent from the PR diff. No test file of any kind was added.

Additionally, the changes to `modules/fundamental/src/advisory/service/advisory.rs` are minimal (no substantive logic added), despite the task specifying that threshold filtering logic should be added to the aggregation query. Instead, the filtering was implemented entirely in the endpoint handler, which is an architectural deviation from the task specification.

---

### Diff Size
**Result**: WARN

The diff adds approximately 30 lines across 2 files. For a feature that includes a new query parameter, filtering logic, validation, a new response field, and a full integration test suite, this is disproportionately small. The small size is explained by missing components: no test file, no validation logic, no model changes for `threshold_applied`.

---

### Commit Traceability
**Result**: WARN

The PR diff output does not include commit messages, so traceability to TC-9102 cannot be confirmed from the diff alone. The PR is linked to TC-9102 via the Jira task's PR URL field.

---

### Sensitive Patterns
**Result**: PASS

No secrets, credentials, API keys, tokens, or other sensitive patterns detected in the added lines. The changes are limited to query parameter handling and filtering logic.

---

### CI Status
**Result**: PASS

All CI checks pass.

---

### Acceptance Criteria
**Result**: FAIL (3 of 6 criteria fail)

| # | Criterion | Result | Reason |
|---|-----------|--------|--------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | `total` field is computed from unfiltered counts instead of filtered counts, making the response internally inconsistent |
| 2 | No threshold returns all severity counts (backward compatible) | PASS | `None` branch returns original summary unchanged |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | `unwrap_or(0)` silently accepts invalid values, treating them as "critical" instead of returning 400 |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | Ordering array `["critical", "high", "medium", "low"]` is correct |
| 5 | Response includes `threshold_applied` boolean field | FAIL | No such field exists in the response; `AdvisorySummary` struct was not modified |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | SBOM fetch and error handling path is unchanged |

#### Criterion 3 -- Critical Finding

The most significant defect is the silent acceptance of invalid threshold values. The code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid`, `position()` returns `None`, and `unwrap_or(0)` maps it to index 0 (critical). This means any invalid input is silently treated as `?threshold=critical`. The task implementation notes explicitly require using `AppError` for validation errors and returning 400.

#### Criterion 5 -- Missing Feature

The `AdvisorySummary` struct was not modified to include a `threshold_applied: bool` field. Neither the model definition nor the response construction includes this field.

#### Criterion 1 -- Incorrect Total

The `total` field is computed as:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This sums all unfiltered severity counts regardless of the threshold. When `threshold=high`, `medium` and `low` are zeroed in the response but still included in `total`.

---

### Test Quality
**Result**: FAIL

No test file was created. The task requires `tests/api/advisory_summary.rs` with 6 specific test cases:
- Test threshold=critical returns only critical count
- Test threshold=high returns critical and high counts
- Test threshold=medium returns critical, high, and medium counts
- Test no threshold returns all four severity counts
- Test invalid threshold value returns 400
- Test non-existent SBOM ID returns 404

None of these tests exist in the PR diff.

---

### Test Change Classification
**Result**: N/A

No test files appear in the PR diff.

---

### Verification Commands
**Result**: N/A

No verification commands specified in the task.

---

### Eval Quality
**Result**: N/A

No eval result reviews exist.

---

## Overall Assessment

**FAIL** -- This PR does not satisfy the acceptance criteria for TC-9102. Three of six acceptance criteria fail:

1. **Invalid threshold values are silently accepted** (criterion 3): The `unwrap_or(0)` pattern converts unrecognized threshold values to index 0 (critical) instead of returning 400 Bad Request. This is a correctness bug that could mask client errors.

2. **Missing `threshold_applied` boolean field** (criterion 5): The response does not include a `threshold_applied` field, which is explicitly required by the acceptance criteria.

3. **Incorrect `total` computation** (criterion 1): The `total` field sums unfiltered counts, producing an inconsistent response when filtering is active.

Additionally, the required test file `tests/api/advisory_summary.rs` is entirely absent from the PR, and the service-layer changes in `advisory.rs` are minimal despite the task specifying that filtering logic should be added there.
