# File 1 — CREATE `modules/fundamental/src/advisory/model/severity_summary.rs`

**Purpose**: the response type for `GET /api/v2/sbom/{id}/advisory-summary`.

**Pattern followed**: `advisory/model/summary.rs` (`AdvisorySummary`): one public struct per file,
serde + utoipa derives.

**Pre-checks**: grep the workspace for `SeveritySummary|SeverityCount|severity_summary` to make sure no equivalent type already exists (symbol deduplication). Inspect the type of `AdvisorySummary.severity` (`find_symbol`) so that the mapping helper matches it.

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated count of unique vulnerability advisories linked to an SBOM, grouped by severity.
///
/// Every level defaults to `0`, so a level with no advisories still appears in the response.
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
    /// Sum of the four severity buckets above.
    pub total: u64,
}

impl SeveritySummary {
    /// Adds `count` advisories to the bucket matching `severity`.
    ///
    /// Severity matching is case-insensitive. Unknown severities are ignored, so `total`
    /// always equals critical + high + medium + low.
    pub fn add(&mut self, severity: &str, count: u64) {
        match severity.to_ascii_lowercase().as_str() {
            "critical" => self.critical += count,
            "high" => self.high += count,
            "medium" => self.medium += count,
            "low" => self.low += count,
            _ => return,
        }
        self.total += count;
    }
}
```

Notes:
- If `AdvisorySummary.severity` is a `Severity` enum rather than a string, `add` takes `Severity`
  and matches on its variants instead of strings (reuse the existing enum, do not redeclare it).
- The serde field names are already lowercase, so the JSON is exactly `{ "critical", "high", "medium", "low", "total" }`. No `rename_all` is needed.
- `Default` covers AC #4 (every level defaults to 0).
- If `fundamental` has a `#[cfg(test)]` unit test convention for models, add a small unit test for
  `add` (unknown severity is ignored, case-insensitive matching).
