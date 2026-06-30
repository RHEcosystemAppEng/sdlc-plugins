## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Evidence

The diff constructs the filtered `AdvisorySummary` as follows:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the unfiltered case returns:

```rust
None => summary,
```

Neither branch includes a `threshold_applied` boolean field. The response struct `AdvisorySummary` is not modified anywhere in the diff to add this field. Searching the entire diff, there is no occurrence of `threshold_applied` in any file.

### Expected Behavior

The acceptance criterion requires that the response includes a `threshold_applied` boolean field:
- When a threshold parameter is provided: `threshold_applied: true`
- When no threshold parameter is provided: `threshold_applied: false`

This would require:
1. Adding `threshold_applied: bool` to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`)
2. Setting it to `true` in the filtered branch and `false` in the None branch

### Conclusion

This criterion fails. The `threshold_applied` boolean field is entirely absent from the diff. No changes to the `AdvisorySummary` model struct are included, and no such field appears in the response construction.
