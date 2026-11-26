# File 1 (CREATE): `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose
This file holds the response struct for `GET /api/v2/sbom/{id}/advisory-summary`.

## Conventions followed
- One struct per model file, with the same derives as `AdvisorySummary` in `model/summary.rs`.
- Every public symbol has a `///` doc comment.
- `Default` makes every severity count start at 0 (acceptance criterion: "All severity levels
  default to 0").

## Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated count of unique advisories per severity level for a single SBOM.
///
/// Returned by `GET /api/v2/sbom/{id}/advisory-summary` so that dashboard widgets can render
/// severity breakdowns without counting on the client.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}

impl SeveritySummary {
    /// Adds one advisory with the given severity label to the counts.
    ///
    /// Matching ignores case (`"CRITICAL"`, `"critical"`, `"Critical"`). Advisories whose
    /// severity is missing or not one of the four known levels count only toward `total`.
    pub fn record(&mut self, severity: Option<&str>) {
        match severity.map(|s| s.trim().to_ascii_lowercase()).as_deref() {
            Some("critical") => self.critical += 1,
            Some("high") => self.high += 1,
            Some("medium") => self.medium += 1,
            Some("low") => self.low += 1,
            _ => {}
        }
        self.total += 1;
    }
}
```

## Notes
- JSON output is `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`, which matches
  the API contract. No `serde(rename_all)` is needed because the field names are already lowercase.
- If `AdvisorySummary.severity` turns out to be an enum rather than a string, `record` would take
  that enum and match on its variants. This would be confirmed with
  `mcp__serena_backend__find_symbol(name_path_pattern="AdvisorySummary", include_body=true)` before
  writing the code. Symbol-dedup check: grep the `fundamental` crate for `SeveritySummary` and
  `Severity` first, and reuse an existing severity enum if one exists.
- Design choice: `total` counts every unique advisory, including ones with unknown or missing
  severity. That makes `total >= critical + high + medium + low`. This is recorded in the PR
  description.
