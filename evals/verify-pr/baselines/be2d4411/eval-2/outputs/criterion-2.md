# Criterion 2: No threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Evidence from Diff

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` handles the absence of a threshold parameter via the `None` arm of the match:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

## Detailed Reasoning

When no `threshold` query parameter is provided, `params.threshold` is `None`. The match expression falls through to the `None =>` arm, which returns the original `summary` unchanged. This preserves the original response exactly as it was before this change.

The `SummaryParams` struct declares `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

Serde will deserialize a missing query parameter as `None`, so the endpoint behaves identically to the pre-change version when no threshold is specified.

## Conclusion

The backward-compatible behavior is correctly preserved. The endpoint returns the full, unfiltered advisory summary when no threshold parameter is provided.
