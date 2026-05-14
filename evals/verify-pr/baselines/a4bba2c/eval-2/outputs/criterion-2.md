# Criterion 2: No threshold returns all severity counts (backward compatible)

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The code handles the `None` case for the threshold parameter correctly:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original unfiltered `summary` is returned directly. This preserves backward compatibility -- the response will contain all severity counts exactly as it did before this change.

The `SummaryParams` struct defines `threshold` as `Option<String>`, which means the query parameter is optional and defaults to `None` when not provided:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

## Evidence

- `SummaryParams.threshold` is `Option<String>` -- correctly optional
- The `None` match arm returns the unmodified `summary` object
- No structural changes to the `AdvisorySummary` response type are visible in the diff (though `threshold_applied` is missing -- that is a separate criterion)
