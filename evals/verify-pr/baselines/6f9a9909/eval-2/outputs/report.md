## Verification Report for TC-9102 (commit f6a7b8c)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | PASS | Both expected files modified; however, `tests/api/advisory_summary.rs` (listed under "Files to Create") is absent from the diff |
| Diff Size | WARN | ~20 lines added across 2 files; undersized given that the required test file and model changes are entirely missing |
| Commit Traceability | WARN | Diff does not include commit messages; cannot verify TC-9102 reference from the diff alone |
| Sensitive Patterns | PASS | No secrets, credentials, API keys, or tokens found in added lines |
| CI Status | PASS | All CI checks pass per the prompt |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (details below) |
| Test Quality | FAIL | No test file exists in the diff; `tests/api/advisory_summary.rs` was required but not created. Eval Quality: N/A |
| Test Change Classification | N/A | No test files in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

---

### Acceptance Criteria Detail

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `threshold=high` returns counts for critical and high only | FAIL | Filtering logic comparison is inverted (`threshold_idx <= N` instead of `N <= threshold_idx`); `threshold=high` includes all four severity counts. Total also uses unfiltered sums. |
| 2 | Without threshold returns all severity counts (backward compatible) | PASS | `None` match arm returns unmodified `summary` |
| 3 | `threshold=invalid` returns 400 Bad Request | FAIL | `.unwrap_or(0)` silently treats invalid values as index 0 ("critical") instead of returning 400 |
| 4 | Severity ordering correct: critical > high > medium > low | FAIL | Array ordering is correct but comparison logic is inverted, producing wrong filtering results. `Severity` enum with `Ord` not implemented as specified. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | Field entirely absent from response struct and construction; `summary.rs` model not modified |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | SBOM fetch and error propagation unchanged in diff |

### Domain Findings

#### 1. Inverted filtering logic (Critical)

The filtering conditions in `get.rs` are reversed:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

This checks whether the threshold's index is less than or equal to each severity's index. The correct check is the opposite: include a severity if its index is less than or equal to the threshold's index (i.e., `1 <= threshold_idx`, `2 <= threshold_idx`, `3 <= threshold_idx`). With the current logic:
- `threshold=critical` (idx=0) returns ALL counts instead of only critical
- `threshold=high` (idx=1) returns ALL counts instead of critical + high
- `threshold=medium` (idx=2) excludes high but includes low (both wrong)

#### 2. No input validation for threshold parameter (Critical)

Invalid threshold values (e.g., `?threshold=invalid`, `?threshold=foo`) are silently accepted. The `.position()` call returns `None` and `.unwrap_or(0)` maps this to index 0, treating the invalid value as "critical". The task requires returning 400 Bad Request for invalid values, using `AppError` from `common/src/error.rs`.

#### 3. Missing `threshold_applied` boolean field (Major)

The task requires the response to include a `threshold_applied` boolean indicating whether filtering is active. This field is absent from the `AdvisorySummary` struct (the model file `modules/fundamental/src/advisory/model/summary.rs` is not modified in the diff) and from both response construction paths.

#### 4. Total computed from unfiltered values (Major)

In the filtered branch, the total is computed as:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums the original unfiltered values. The total should reflect only the counts that pass the threshold filter, e.g., for `threshold=high`: `summary.critical + summary.high`.

#### 5. Test file entirely absent (Major)

The task specifies creating `tests/api/advisory_summary.rs` with six test cases (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold returning 400, and non-existent SBOM returning 404). No test file appears in the diff. This means none of the test requirements are satisfied.

#### 6. No meaningful changes to advisory service (Minor)

The task specifies modifying `modules/fundamental/src/advisory/service/advisory.rs` to "add threshold filtering logic to the aggregation query." The diff for this file contains only a blank line addition -- no functional changes. All filtering logic was placed in the endpoint handler instead of the service layer, contrary to the module pattern documented in the repository conventions.
