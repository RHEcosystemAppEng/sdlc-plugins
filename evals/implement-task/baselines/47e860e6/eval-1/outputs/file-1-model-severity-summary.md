# File 1 — CREATE `modules/fundamental/src/advisory/model/severity_summary.rs`

Response model for the advisory severity summary. Follows sibling `summary.rs` / `details.rs` derive set and doc-comment style.

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // only if sibling models derive ToSchema

/// Aggregated count of unique advisories affecting an SBOM, grouped by severity level.
///
/// Returned by `GET /api/v2/sbom/{id}/advisory-summary`. All counts default to zero.
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
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}

impl SeveritySummary {
    /// Increments the counter matching `severity` by `count` and adds it to `total`.
    ///
    /// Severity matching reuses the existing severity type used by `AdvisorySummary.severity`;
    /// unrecognised severities only contribute to `total`.
    pub fn add(&mut self, severity: Option<&Severity>, count: u64) {
        match severity {
            Some(Severity::Critical) => self.critical += count,
            Some(Severity::High) => self.high += count,
            Some(Severity::Medium) => self.medium += count,
            Some(Severity::Low) => self.low += count,
            _ => {}
        }
        self.total += count;
    }
}
```

Notes:
- `Severity` is imported from wherever `AdvisorySummary.severity`'s type is defined (located with `mcp__serena_backend__find_symbol` before writing; no new enum is declared — symbol deduplication rule). If `severity` is a `String`, match case-insensitively on `"critical" | "high" | "medium" | "low"`.
- `Default` gives all-zero counts (AC: levels default to 0).
