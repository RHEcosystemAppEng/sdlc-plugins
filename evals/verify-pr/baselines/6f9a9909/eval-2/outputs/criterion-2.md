## Criterion 2

**Text:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**What I checked:** The `None` branch of the `match &params.threshold` expression in `modules/fundamental/src/advisory/endpoints/get.rs`.

**Code evidence:**

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the match arm returns the unmodified `summary` directly. This preserves the original behavior where all severity counts are returned.

**Verdict: PASS** -- The `None` branch returns the unmodified summary, maintaining backward compatibility for requests without a threshold parameter.
