# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: NOT MET (FAIL)**

## Reasoning

- Neither response path sets `threshold_applied`:
  - The `Some(threshold)` branch builds `AdvisorySummary { critical, high, medium, low, total }`, which has no `threshold_applied`.
  - The `None` branch returns the original `summary` unchanged, with nothing marking that no filter was applied.
- `AdvisorySummary` is defined in `modules/fundamental/src/advisory/model/summary.rs`, which is not in the diff, so the response struct gained no new field. The struct literal in the handler names only the five existing fields, and CI passes, so the struct cannot contain a required `threshold_applied` field.
- The handler adds no wrapper type or extra JSON field anywhere else.

Clients cannot tell from the response whether filtering was applied, so the criterion is not met.

## Test coverage
No test checks this field.
