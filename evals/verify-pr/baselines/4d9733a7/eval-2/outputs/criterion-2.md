## Criterion 2: Without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

### Analysis

The handler uses a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code falls through to the `None => summary` branch, which returns the original unfiltered `AdvisorySummary` directly. This preserves backward compatibility -- the endpoint behavior is identical to before when no threshold parameter is supplied.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which correctly makes it optional in the query string:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-58 in the diff
- The `None` branch returns `summary` unchanged
- The `SummaryParams.threshold` field is `Option<String>`, making it optional
- No other changes affect the response structure when no threshold is provided

### Conclusion

Backward compatibility is preserved. The criterion is satisfied.
