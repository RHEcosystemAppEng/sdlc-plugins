# Criterion 1 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

**Analysis:**

The filtering logic in `get.rs` uses an inverted comparison that does not correctly restrict the returned severity counts.

Code at lines 41–56:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    ...
}
```

For `threshold=high`, `threshold_idx = 1`. The conditions evaluate as:
- `high`: `1 <= 1` → true → included (correct)
- `medium`: `1 <= 2` → true → **included** (incorrect — should be excluded)
- `low`: `1 <= 3` → true → **included** (incorrect — should be excluded)

The comparison is inverted. The correct condition to include a severity at position `i` only when it is at or above the threshold would be `i <= threshold_idx`, not `threshold_idx <= i`. As written, `threshold=high` returns all four severity counts instead of only critical and high.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 43–52
- The conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` are always true when threshold_idx is 0 or 1, causing medium and low to be included when they should be zeroed.
