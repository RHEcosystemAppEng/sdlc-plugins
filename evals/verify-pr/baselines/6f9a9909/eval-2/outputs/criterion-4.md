## Criterion 4

**Text:** Severity ordering is correct: critical > high > medium > low

**What I checked:** The severity ordering array and how it is used in the filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. Also checked whether a `Severity` enum with `Ord` was implemented as specified in the implementation notes.

**Code evidence:**

The severity order array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This correctly encodes the ordering critical > high > medium > low (index 0 is highest severity, index 3 is lowest).

However, the filtering logic that uses this ordering is inverted:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For `threshold=critical` (idx=0): high is included (0 <= 1 = true), medium is included (0 <= 2 = true), low is included (0 <= 3 = true). This returns ALL counts when only critical should be returned.

For `threshold=medium` (idx=2): high is EXCLUDED (2 <= 1 = false), medium is included (2 <= 2 = true), low is included (2 <= 3 = true). This excludes high but includes low, which is incorrect -- high is above medium in severity and should be included.

The comparison should be reversed: `severity_position <= threshold_idx` instead of `threshold_idx <= severity_position`.

Additionally, the task's implementation notes specify defining a `Severity` enum with `Ord` trait, which was not done. The code uses raw string comparison and hardcoded index comparisons instead.

**Verdict: FAIL** -- While the ordering array itself is correct, the comparison logic using the ordering is inverted, causing the filtering to produce incorrect results. The specified `Severity` enum with `Ord` was not implemented.
