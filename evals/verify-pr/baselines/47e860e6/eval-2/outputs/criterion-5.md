# Criterion 5 — FAIL

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

## What was checked
- The `AdvisorySummary` literal built in the `Some(threshold)` arm of `advisory_summary`
- Any change to the `AdvisorySummary` model (`modules/fundamental/src/advisory/model/summary.rs`)
- The `advisory.rs` service hunk

## What was found
- The struct literal sets only `critical`, `high`, `medium`, `low` and `total`. There is no `threshold_applied` field.
- The PR does not touch `modules/fundamental/src/advisory/model/summary.rs`, so the response struct has no new field. The diff contains no `threshold_applied` anywhere.
- The `None` arm returns the unmodified summary, so neither the filtered nor the unfiltered response tells the client whether filtering was applied.

**Verdict: FAIL.** The `threshold_applied` field is not implemented.
