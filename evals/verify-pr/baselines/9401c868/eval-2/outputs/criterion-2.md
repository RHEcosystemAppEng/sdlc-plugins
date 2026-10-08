## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Result: PASS

### Analysis

When no `threshold` query parameter is provided, `params.threshold` is `None`. The code handles this case with:

```rust
None => summary,
```

This returns the original `AdvisorySummary` from `AdvisoryService::aggregate_severities()` unmodified, preserving all four severity counts (critical, high, medium, low) and the total.

The `SummaryParams` struct defines `threshold` as `Option<String>`:
```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This means the parameter is optional and requests without it will deserialize successfully with `threshold = None`.

Backward compatibility is maintained: existing callers that do not pass a `threshold` parameter will receive the same response as before.

Note: While the response format is missing the `threshold_applied` field (see criterion 5), the severity counts themselves are correctly returned in full, satisfying this specific criterion.
