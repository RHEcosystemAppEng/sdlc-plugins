# Criterion 2: Without threshold returns all severity counts (backward compatible)

## Result: PASS

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Analysis

The handler defines the threshold parameter as `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no threshold query parameter is provided, `params.threshold` is `None`. The match arm for `None` returns the unmodified summary:

```rust
None => summary,
```

This preserves the original behavior exactly -- the full `AdvisorySummary` with all severity counts (critical, high, medium, low, total) is returned without any filtering.

## Verdict

PASS -- The `None` branch correctly returns the unmodified summary, preserving backward compatibility for requests without a threshold parameter.
