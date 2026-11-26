# File 1 (CREATE): `modules/fundamental/src/advisory/model/severity_summary.rs`

Pattern followed: `modules/fundamental/src/advisory/model/summary.rs` (one struct per file, serde
derives, utoipa `ToSchema` if siblings derive it, `///` docs).

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated counts of unique advisories affecting an SBOM, grouped by severity level.
///
/// Returned by `GET /api/v2/sbom/{id}/advisory-summary` so dashboards can render
/// severity breakdowns without counting on the client.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total unique advisories counted across all severity levels.
    pub total: u64,
}

impl SeveritySummary {
    /// Increments the bucket matching `severity` (case-insensitive) and the total.
    ///
    /// Unknown or missing severities are ignored so that `total` always equals
    /// `critical + high + medium + low`.
    pub fn record(&mut self, severity: Option<&str>) {
        let bucket = match severity.map(str::to_ascii_lowercase).as_deref() {
            Some("critical") => &mut self.critical,
            Some("high") => &mut self.high,
            Some("medium") => &mut self.medium,
            Some("low") => &mut self.low,
            _ => return,
        };
        *bucket += 1;
        self.total += 1;
    }
}
```

Notes:
- `Default` guarantees all levels are 0 when no advisories exist (acceptance criterion).
- Serialized shape is exactly `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.
- If Step 4's symbol-dedup search finds an existing `Severity` enum on `AdvisorySummary.severity`,
  `record` takes `Option<&Severity>` and matches enum variants instead of strings.
- Derive `ToSchema` only if sibling models do (OpenAPI convention parity).
