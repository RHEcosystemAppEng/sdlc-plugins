# File 1 (CREATE): `modules/fundamental/src/advisory/model/severity_summary.rs`

Purpose: response struct for `GET /api/v2/sbom/{id}/advisory-summary`.
Pattern source: `modules/fundamental/src/advisory/model/summary.rs` (derives, doc comments, ToSchema).

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Count of unique advisories linked to an SBOM, grouped by severity level.
///
/// Every level defaults to 0 when the SBOM has no advisories at that level.
/// `total` is the number of unique advisories linked to the SBOM.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}

impl SeveritySummary {
    /// Records one advisory with the given severity label (case-insensitive).
    ///
    /// Severities outside Critical/High/Medium/Low (or missing) only increase `total`.
    pub fn record(&mut self, severity: Option<&str>) {
        match severity.map(str::to_ascii_lowercase).as_deref() {
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

Notes:
- If `ToSchema` / `utoipa` is not used on sibling models, drop the derive and import.
- If Step 4's symbol search finds an existing `Severity` enum (e.g. on `AdvisorySummary.severity`), `record` takes that enum instead of `Option<&str>` and matches on its variants — no new severity type is declared.
- `PartialEq, Eq` let tests compare the whole deserialized body with `assert_eq!`.
