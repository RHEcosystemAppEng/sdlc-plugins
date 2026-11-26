# Criterion 5 — FAIL

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

## What was checked
- The full PR diff, searched for `threshold_applied`.
- How `AdvisorySummary` is built in the handler (`modules/fundamental/src/advisory/endpoints/get.rs`), and whether the model (`modules/fundamental/src/advisory/model/summary.rs`) was changed.

## What was found
- `threshold_applied` does not appear anywhere in the diff.
- The handler builds `AdvisorySummary { critical, high, medium, low, total }`, with no boolean flag.
- `modules/fundamental/src/advisory/model/summary.rs` is not in the diff, so no field was added to the response struct. A wrapper response type was not added either.

## Conclusion
The response has no `threshold_applied` field. The criterion is not satisfied.

**Verdict: FAIL**
