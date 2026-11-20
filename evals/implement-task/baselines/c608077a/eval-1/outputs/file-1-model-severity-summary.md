# File 1 — CREATE `modules/fundamental/src/advisory/model/severity_summary.rs`

Purpose: response struct for `GET /api/v2/sbom/{id}/advisory-summary`.

Conventions applied: one struct per model file; derives match `AdvisorySummary` (`Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `utoipa::ToSchema`); `///` doc comments on struct and fields. `Default` derive guarantees every level is 0 when no advisories exist.

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Counts of unique advisories affecting an SBOM, grouped by severity level.
///
/// Returned by `GET /api/v2/sbom/{id}/advisory-summary` so dashboards can render
/// severity breakdowns without client-side counting.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories counted (sum of all levels).
    pub total: u64,
}

impl SeveritySummary {
    /// Increments the counter matching `severity` and the total.
    ///
    /// Severities outside Critical/High/Medium/Low (e.g. missing or unknown)
    /// are ignored so that `total` always equals the sum of the four levels.
    pub fn record(&mut self, severity: Option<&Severity>) {
        let slot = match severity {
            Some(Severity::Critical) => &mut self.critical,
            Some(Severity::High) => &mut self.high,
            Some(Severity::Medium) => &mut self.medium,
            Some(Severity::Low) => &mut self.low,
            _ => return,
        };
        *slot += 1;
        self.total += 1;
    }
}
```

Notes:
- `Severity` is imported from wherever the type of `AdvisorySummary.severity` is defined (determined via `mcp__serena_backend__find_symbol("AdvisorySummary/severity")`). Do not declare a new enum. If `severity` is a `String`/`Option<String>`, `record` instead matches case-insensitively on `"critical" | "high" | "medium" | "low"`.
- Design decision (record in PR): advisories with no/unknown severity are excluded from `total` so `total == critical + high + medium + low`, matching the documented response shape.
