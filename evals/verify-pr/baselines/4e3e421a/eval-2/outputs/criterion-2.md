# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: MET (PASS)**

## Reasoning

- The new query struct makes the parameter optional:
  ```rust
  #[derive(Debug, Deserialize)]
  pub struct SummaryParams {
      pub threshold: Option<String>,
  }
  ```
  It is extracted with `Query(params): Query<SummaryParams>`. When `threshold` is missing, it deserializes to `None` and the extractor does not reject the request.
- The `None` branch returns the original aggregate unchanged:
  ```rust
  None => summary,
  ```
  `summary` comes from the unmodified `AdvisoryService::aggregate_severities`. It has all four severity counts, and its `total` is `counts.values().sum()`. Callers that send no threshold get exactly the response they got before.

## Caveat
This was confirmed by reading the code only. The required test "no threshold returns all four severity counts" was not added. If criterion 5 is implemented by adding a `threshold_applied` field, this path must set it to `false`.
