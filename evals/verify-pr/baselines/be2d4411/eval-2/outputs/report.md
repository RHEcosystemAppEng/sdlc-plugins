# PR Verification Report

| Field | Value |
|---|---|
| PR | #743 |
| Task | TC-9102 |
| Repository | trustify-backend |
| Title | Add severity threshold filter to advisory summary endpoint |
| Result | **FAIL** |

---

## Verification Summary

| Check | Verdict | Details |
|---|---|---|
| Scope Containment | FAIL | Missing required file: `tests/api/advisory_summary.rs` (task specifies it under "Files to Create"). Only 2 of 3 expected files are present in the diff. |
| Diff Size | WARN | The diff is small (two files changed with modest additions). Proportionate for the service/endpoint changes, but disproportionately small given the missing test file. |
| Commit Traceability | N/A | Commit messages are not available in the diff output; cannot verify TC-9102 references. |
| Sensitive Patterns | PASS | No secrets, credentials, API keys, or tokens found in added lines. |
| CI Status | PASS | All CI checks pass (per prompt). |
| Acceptance Criteria | FAIL | 3 of 6 criteria fail (criteria 1, 3, 5). See detailed breakdown below. |
| Eval Quality | N/A | No eval result reviews exist. |
| Test Change Classification | N/A | No test files are present in the PR diff. |
| Verification Commands | N/A | No verification commands specified in the task. |
| Review Feedback | N/A | No review comments on this PR. |
| Root-Cause Investigation | N/A | No sub-tasks to investigate. |

---

## Acceptance Criteria Breakdown

| # | Criterion | Verdict | Summary |
|---|---|---|---|
| 1 | `threshold=high` returns counts for critical and high only | **FAIL** | Filtering logic has inverted comparison (`threshold_idx <= N` instead of `N <= threshold_idx`), causing `threshold=high` to include all severity levels. Additionally, the `total` field uses unfiltered counts. See [criterion-1.md](criterion-1.md). |
| 2 | No threshold returns all severity counts (backward compatible) | PASS | The `None` branch returns the original summary unchanged. See [criterion-2.md](criterion-2.md). |
| 3 | `threshold=invalid` returns 400 Bad Request | **FAIL** | `.unwrap_or(0)` silently maps invalid values to index 0 (critical) instead of returning 400. No validation or error handling for unrecognized threshold values. See [criterion-3.md](criterion-3.md). |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | The ordering array `["critical", "high", "medium", "low"]` correctly ranks severities. The filtering bug that misuses this ordering is covered under criterion 1. See [criterion-4.md](criterion-4.md). |
| 5 | Response includes `threshold_applied` boolean field | **FAIL** | No `threshold_applied` field exists in the response struct or handler code. The `AdvisorySummary` model is not modified in the diff. See [criterion-5.md](criterion-5.md). |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | SBOM fetch logic is unchanged; existing 404 behavior is preserved. See [criterion-6.md](criterion-6.md). |

---

## Scope Containment

### Files expected by task

| File | Expected Action | Present in Diff |
|---|---|---|
| `modules/fundamental/src/advisory/endpoints/get.rs` | Modify | Yes |
| `modules/fundamental/src/advisory/service/advisory.rs` | Modify | Yes |
| `tests/api/advisory_summary.rs` | Create | **No** |

### Finding

The task explicitly requires creating `tests/api/advisory_summary.rs` with integration tests covering six test scenarios (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM). This file is entirely absent from the diff. No test code of any kind was added.

The diff to `modules/fundamental/src/advisory/service/advisory.rs` is minimal -- only a blank line was added. The actual filtering logic was placed entirely in the endpoint handler rather than in the service layer as the task suggested.

### Out-of-scope changes

No out-of-scope files were modified.

---

## Detailed Findings

### 1. Inverted filtering comparison (Critical)

The filtering logic in `get.rs` uses the condition `threshold_idx <= N` (where N is a hardcoded severity position) to decide whether to include each severity. This is inverted -- it should be `N <= threshold_idx`. As a result:

- `threshold=critical` (idx=0): includes ALL severities (should include only critical)
- `threshold=high` (idx=1): includes ALL severities (should include critical + high)
- `threshold=medium` (idx=2): excludes high (should include critical + high + medium)
- `threshold=low` (idx=3): excludes high and medium (should include all)

Every threshold value produces incorrect results except the degenerate cases.

### 2. Missing 400 validation (Critical)

Invalid threshold values are silently accepted via `.unwrap_or(0)`. The task notes explicitly require using `AppError` for validation errors. A misspelled threshold (e.g., "hig") silently returns critical-only results with no error indication.

### 3. Missing threshold_applied field (Critical)

The `AdvisorySummary` response struct is not modified to include a `threshold_applied: bool` field. Callers cannot determine from the response whether filtering was applied.

### 4. Total uses unfiltered counts (Moderate)

The `total` field in the filtered response is computed as `summary.critical + summary.high + summary.medium + summary.low`, using the original unfiltered values. Even with correct filtering, the total would not match the sum of the filtered counts.

### 5. No test coverage (Critical)

The required test file `tests/api/advisory_summary.rs` is entirely missing. None of the six required test scenarios are covered.

---

## Conclusion

The PR fails verification due to three failing acceptance criteria (1, 3, 5), a missing required test file, and additional implementation bugs (inverted comparison logic, incorrect total computation). The PR should not be merged in its current state.
