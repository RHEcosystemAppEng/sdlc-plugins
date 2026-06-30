## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | Task requires creating `tests/api/advisory_summary.rs` but this file is entirely missing from the diff |
| Diff Size | PASS | 2 files changed with modest additions (~30 lines); proportionate to task scope (excluding the missing test file) |
| Commit Traceability | N/A | Commit data not available in fixture |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass per fixture data |
| Acceptance Criteria | FAIL | 3 of 6 criteria not met (see details below) |
| Test Quality | N/A | No test files present in the PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files present in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

---

### Scope Containment -- FAIL

**Files specified in task:**
- Files to Modify:
  - `modules/fundamental/src/advisory/endpoints/get.rs` -- PRESENT in diff
  - `modules/fundamental/src/advisory/service/advisory.rs` -- PRESENT in diff
- Files to Create:
  - `tests/api/advisory_summary.rs` -- **MISSING from diff**

**Out-of-scope files:** None

**Unimplemented files:**
- `tests/api/advisory_summary.rs` -- This file is listed under "Files to Create" in the task specification but is entirely absent from the PR diff. The task requires integration tests for threshold filtering, and no test file was created.

---

### Sensitive Patterns -- PASS

No sensitive patterns detected in added lines. Scanned all additions across 2 files for hardcoded passwords, API keys, tokens, private keys, environment files, cloud credentials, and database credentials. No matches found.

---

### CI Status -- PASS

All CI checks pass per the provided fixture data.

---

### Acceptance Criteria -- FAIL

3 of 6 acceptance criteria are not satisfied:

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `?threshold=high` returns counts for critical and high only | PASS | Filtering logic is implemented with severity ordering and index-based comparison |
| 2 | No threshold returns all severity counts (backward compatible) | PASS | `None => summary` branch returns unfiltered results |
| 3 | `?threshold=invalid` returns 400 Bad Request | **FAIL** | Invalid threshold values use `.unwrap_or(0)` which silently maps to index 0 instead of returning 400 |
| 4 | Severity ordering is correct: critical > high > medium > low | PASS | Array `["critical", "high", "medium", "low"]` establishes correct ordering |
| 5 | Response includes `threshold_applied` boolean field | **FAIL** | No `threshold_applied` field exists in the response struct or construction |
| 6 | Endpoint returns 404 for non-existent SBOM IDs | PASS | Existing SBOM fetch logic is unchanged; 404 behavior preserved |

#### Criterion 3 Detail: Missing 400 validation for invalid threshold values

The task explicitly requires returning 400 Bad Request for invalid threshold values and the implementation notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The actual implementation uses:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` for an unrecognized value like "invalid", `.unwrap_or(0)` silently maps it to index 0 (the "critical" position). This means `?threshold=invalid` is treated as `?threshold=critical` instead of returning a 400 error. No `AppError` validation is present.

#### Criterion 5 Detail: Missing `threshold_applied` boolean field

The response `AdvisorySummary` struct is constructed with only `critical`, `high`, `medium`, `low`, and `total` fields. The `threshold_applied` boolean field required by the acceptance criteria is completely absent. The `AdvisorySummary` model in `modules/fundamental/src/advisory/model/summary.rs` was not modified to add this field. API consumers cannot determine from the response whether threshold filtering was applied.

---

### Additional Finding: Incorrect total calculation

The `total` field in the filtered response is computed from unfiltered counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This uses the original `summary` values rather than the filtered values. When threshold filtering is active and some severity counts are set to 0, the `total` should reflect only the included (non-zeroed) counts. This is a correctness bug that would cause the `total` to be inconsistent with the individual severity counts in the filtered response.

---

### Test Quality -- N/A

No test files are present in the PR diff. The task required creating `tests/api/advisory_summary.rs` with integration tests covering:
- threshold=critical returns only critical count
- threshold=high returns critical and high counts
- threshold=medium returns critical, high, and medium counts
- No threshold returns all four severity counts
- Invalid threshold value returns 400
- Non-existent SBOM ID returns 404

None of these tests were implemented. This gap is captured under Scope Containment (missing file) and does not independently affect the Overall verdict through Test Quality, but it represents a significant gap in the PR's completeness.

Eval Quality: N/A

---

### Summary of Issues

1. **Missing 400 validation (Criterion 3):** Invalid threshold values are silently accepted via `unwrap_or(0)` instead of returning HTTP 400 Bad Request as required by the acceptance criteria and implementation notes.

2. **Missing `threshold_applied` field (Criterion 5):** The response does not include the required `threshold_applied` boolean field to indicate whether filtering is active.

3. **Missing test file (Scope Containment):** The file `tests/api/advisory_summary.rs` is specified under "Files to Create" in the task but is entirely absent from the diff. No integration tests were written for the threshold filtering feature.

4. **Incorrect total calculation (Additional finding):** The `total` field uses unfiltered counts even when threshold filtering zeroes out some severity counts, producing an inconsistent response.
