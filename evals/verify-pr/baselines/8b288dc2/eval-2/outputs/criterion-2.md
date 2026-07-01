## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Analysis

The diff handles the case where no threshold parameter is provided via the `None` branch of the match statement:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None`, the original `summary` object is returned unmodified. This preserves backward compatibility -- the endpoint returns the same `AdvisorySummary` with all severity counts (critical, high, medium, low, total) as it did before the change.

The `SummaryParams` struct declares threshold as `Option<String>`, so the query parameter is optional and Axum will correctly deserialize a request without `?threshold=...` as `None`.

### Evidence

Lines 41 and 55-56 of the diff in `get.rs` show the `None => summary` passthrough, confirming backward compatibility is maintained.

### Verdict

PASS -- Requests without a threshold parameter return the full, unfiltered summary as before.
