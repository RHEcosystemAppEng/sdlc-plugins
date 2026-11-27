# File 1 (CREATE): `modules/fundamental/src/advisory/model/severity_summary.rs`

Purpose: response struct for `GET /api/v2/sbom/{id}/advisory-summary`.
Pattern: mirrors `advisory/model/summary.rs` (one struct per file, serde derives, `///` docs).

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if sibling models derive ToSchema

/// Aggregated counts of unique advisories affecting an SBOM, grouped by severity level.
///
/// Used by dashboard widgets to render severity breakdowns without client-side counting.
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
    /// Sum of all severity-level counts above.
    pub total: u64,
}

impl SeveritySummary {
    /// Increments the counter matching `severity` (case-insensitive) and the total.
    /// Unrecognized or missing severities are ignored so all levels stay consistent with `total`.
    pub fn record(&mut self, severity: Option<&str>) {
        let slot = match severity.map(str::to_ascii_lowercase).as_deref() {
            Some("critical") => &mut self.critical,
            Some("high") => &mut self.high,
            Some("medium") => &mut self.medium,
            Some("low") => &mut self.low,
            _ => return,
        };
        *slot += 1;
        self.total += 1;
    }
}
```

Notes:
- `Default` gives all-zero counts -> satisfies "All severity levels default to 0".
- JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.
- Reuse check (Step 6): before writing `record`, search for an existing severity enum /
  ordering (`Severity`, `SEVERITY_ORDER`, `severity_order`) in `advisory/model/summary.rs`,
  `entity/src/advisory.rs`, and `common/`. If a `Severity` enum exists (type of the
  `AdvisorySummary.severity` field), match on its variants instead of strings.
