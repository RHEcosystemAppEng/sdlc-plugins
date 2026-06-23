# Criterion 2: Backward compatibility without threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Reasoning

In `modules/fundamental/src/advisory/endpoints/get.rs`, the code handles the `None` case for `params.threshold`:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None` (it is declared as `Option<String>`), and the original unfiltered `summary` is returned directly. This preserves backward compatibility -- all severity counts are returned unchanged.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so the parameter is truly optional in the query string. The existing behavior (returning all counts) is preserved when the parameter is absent.

**Evidence:** Lines 41-56 of the diff show the match expression with the `None => summary` arm, confirming the original summary is passed through unmodified.
