## Criterion 2: Without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

### Analysis

The filtering logic correctly handles the absence of a threshold parameter. The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no threshold is provided, the match expression falls through to the `None` arm:

```rust
None => summary,
```

This returns the original, unmodified `summary` object from `AdvisoryService::aggregate_severities()`, preserving all severity counts exactly as they were before this feature was added.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, diff lines showing the `None => summary` branch
- **Behavior:** The original response is returned unmodified when no threshold parameter is present
- **Backward compatibility:** Existing API consumers that do not supply `?threshold=...` will continue to receive the same response format and data
