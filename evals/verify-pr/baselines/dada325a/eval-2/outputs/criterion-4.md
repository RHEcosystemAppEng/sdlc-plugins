# Criterion 4 — FAIL

**Criterion:** Severity ordering is correct: critical > high > medium > low

## What was checked

- How the PR represents and compares severity order.
- Whether it follows the Implementation Notes, which ask for a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`.

## Findings

- No `Severity` enum and no `Ord` implementation were added. The order is a local string array: `["critical", "high", "medium", "low"]`.
- The array lists the severities in the right sequence, but the comparisons that use it are reversed (`threshold_idx <= N` instead of `>= N`). In practice the ordering behaves wrongly:
  - `threshold=critical` returns all four severities, when it should return critical only.
  - `threshold=high` returns all four, when it should return critical and high.
  - `threshold=medium` returns all four, when it should return critical, high and medium.
  - `threshold=low` returns critical and low only, when it should return all four.
- The order lives only inside the handler as a local array. It is not reusable or type-safe, and the aggregation query in `advisory.rs` was not given a WHERE clause on severity rank as the notes require.
- No tests exercise the ordering.

## Verdict

FAIL. The ordering is not modelled as the specified `Ord` enum, and the code applies it in reverse.
