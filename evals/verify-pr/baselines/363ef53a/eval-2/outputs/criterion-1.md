# Criterion 1: Threshold filtering returns only severities at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** PASS

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When a `threshold` query parameter is provided, the code defines a severity ordering array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx` would be `1`. The filtering logic then applies:

- `critical`: always included (no conditional) -- correct, critical is above high
- `high`: included if `threshold_idx <= 1` -- with idx=1, this is true, so high is included -- correct
- `medium`: included if `threshold_idx <= 2` -- with idx=1, this is false, so medium is zeroed -- correct
- `low`: included if `threshold_idx <= 3` -- with idx=1, this is false, so low is zeroed -- correct

The filtering logic correctly returns only critical and high counts when `threshold=high`.

**Note:** While the filtering behavior is correct for valid threshold values, there is a separate issue with the `total` field being computed from unfiltered counts (see broader correctness concerns). The criterion as stated -- returning counts for critical and high only -- is satisfied for the individual severity count fields.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-54 of the diff
- The `severity_order` array correctly orders severities as critical > high > medium > low
- The index-based comparison correctly filters severities below the threshold
