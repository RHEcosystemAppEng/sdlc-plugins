# Criterion 2: Without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Analysis

When no `threshold` query parameter is provided, the `params.threshold` field is `None`. The code handles this case correctly via the `None` match arm:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

The `None` branch returns the original `summary` struct unmodified, which contains all four severity counts (critical, high, medium, low) and the total. This preserves backward compatibility -- callers that do not pass a `threshold` parameter receive the same response as before this change.

The `SummaryParams` struct defines `threshold` as `Option<String>`, so the absence of the query parameter correctly maps to `None`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

## Evidence
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-58
- The `None` branch at line 55 returns the original `summary` unchanged
- `SummaryParams.threshold` is `Option<String>`, so missing parameter = `None`
- No behavioral change for requests without `threshold` parameter
