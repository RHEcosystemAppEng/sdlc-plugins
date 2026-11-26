# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: NOT MET**

## Reasoning
`threshold_applied` does not appear anywhere in the diff. The `AdvisorySummary` struct literal built in the handler sets only `critical`, `high`, `medium`, `low` and `total`. The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified. CI passes, and with Rust struct-literal rules that confirms `AdvisorySummary` has no such field. Neither the filtered nor the unfiltered response tells the client whether filtering was applied.

## Evidence
- `get.rs` (added): the `AdvisorySummary { critical, high, medium, low, total }` literal has no `threshold_applied`.
- `modules/fundamental/src/advisory/model/summary.rs` is not in the diff.
- A search of the diff for `threshold_applied` returns no matches.
