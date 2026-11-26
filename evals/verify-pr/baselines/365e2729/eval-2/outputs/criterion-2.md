# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: MET**

## Reasoning
`SummaryParams.threshold` is declared as `Option<String>`, so `Query<SummaryParams>` deserializes when no query string is present. When `params.threshold` is `None`, the handler returns the original `summary` from `aggregate_severities` unchanged. The fields and response shape match the pre-PR behavior, so existing clients are unaffected.

Caveat: no test covers the no-threshold case. The required test file `tests/api/advisory_summary.rs` is missing.

## Evidence
- `get.rs` (added): `pub struct SummaryParams { pub threshold: Option<String>, }`
- `get.rs` (added): `None => summary,`
- `get.rs` (added): `Ok(Json(filtered))`. In the `None` case `filtered` is the original summary.
