# Acceptance Criterion 2

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result**: PASS

## Evidence

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` uses `Option<String>` for the threshold parameter:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the match arm returns the original unmodified summary:

```rust
None => summary,
```

This preserves backward compatibility -- the endpoint returns all severity counts unchanged when no threshold is specified. The `SummaryParams` struct uses `Option`, so the parameter is not required, and existing clients that do not supply it will receive the same response as before.

**Verdict**: PASS -- backward compatibility is preserved when no threshold is supplied.
