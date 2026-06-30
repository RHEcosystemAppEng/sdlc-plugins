## Repository
trustify-backend

## Target Branch
main

## Description
Define the license report response model that represents the output of the license compliance report endpoint. The report groups packages by license type and includes a compliance flag for each group based on the license policy. This model is the API contract returned to callers.

## Files to Create
- `modules/fundamental/src/license/model/report.rs` — LicenseReport and LicenseGroup response structs

## Files to Modify
- `modules/fundamental/src/license/model/mod.rs` — register the report submodule

## Implementation Notes
The response model should follow the structure described in the feature requirements:

```rust
#[derive(Debug, Clone, Serialize)]
pub struct LicenseReport {
    pub sbom_id: String,
    pub groups: Vec<LicenseGroup>,
    pub summary: ComplianceSummary,
}

#[derive(Debug, Clone, Serialize)]
pub struct LicenseGroup {
    pub license: String,
    pub packages: Vec<PackageLicenseInfo>,
    pub compliant: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct PackageLicenseInfo {
    pub name: String,
    pub version: String,
    pub purl: Option<String>,
    pub transitive: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ComplianceSummary {
    pub total_packages: usize,
    pub compliant_count: usize,
    pub non_compliant_count: usize,
    pub unknown_license_count: usize,
}
```

Follow the existing model patterns from `modules/fundamental/src/sbom/model/details.rs` and `modules/fundamental/src/package/model/summary.rs` for struct conventions and serde derive usage. The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field that will be referenced during report generation.

Per CONVENTIONS.md §Response Types: use Serialize derives consistently with existing model structs.
Applies: task creates `modules/fundamental/src/license/model/report.rs` matching the convention's `.rs` module scope.

## Acceptance Criteria
- [ ] LicenseReport struct serializes to JSON matching the documented API contract
- [ ] LicenseGroup includes a `compliant` boolean flag
- [ ] PackageLicenseInfo includes a `transitive` boolean to distinguish direct vs transitive dependencies
- [ ] ComplianceSummary provides aggregate counts for quick compliance assessment

## Test Requirements
- [ ] Unit test: LicenseReport serializes to expected JSON structure with groups and summary
- [ ] Unit test: empty groups list produces valid JSON with zero-count summary

## Dependencies
- Depends on: Task 1 — License policy model (for module structure)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}
