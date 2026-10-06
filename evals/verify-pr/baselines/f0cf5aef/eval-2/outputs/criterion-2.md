# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The code handles the absence of a threshold parameter with a `None` match arm:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code returns the original `summary` unchanged. This preserves the existing behavior -- all severity counts (critical, high, medium, low) and the total are returned exactly as they were before the change.

This is correct and satisfies the backward compatibility requirement.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` arm passes through the unfiltered `AdvisorySummary` from `aggregate_severities`
- No fields are modified or omitted in the no-threshold case
