# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Reasoning

The new query struct makes the parameter optional:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

So requests that omit `threshold` still deserialize, and the `Query<SummaryParams>` extractor does not reject them. When the parameter is absent, the handler returns the unmodified aggregate:

```rust
None => summary,
```

The response is the same `AdvisorySummary` the endpoint returned before the change, with all four severity counts and `total`. That makes it backward compatible.

Caveats:
- No test covers this path. The required test "no threshold returns all four severity counts" is missing.
- If criterion 5 is later fixed by adding `threshold_applied` to `AdvisorySummary`, the unfiltered response gains one field. That addition does not break compatibility.

## Evidence
- `get.rs`: `SummaryParams { threshold: Option<String> }`, and `None => summary` in the match
