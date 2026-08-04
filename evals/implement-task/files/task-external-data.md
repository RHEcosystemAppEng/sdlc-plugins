<!-- SYNTHETIC TEST DATA — task description testing defensive property access on data from external modules -->

# Mock Jira Task

**Key**: TC-9211
**Summary**: Add vulnerability summary extractor for advisory digest emails
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add a vulnerability summary extractor that processes advisory data from the ingestor
module's output and produces a digest suitable for email notifications. The extractor
reads `AdvisoryIngestResult` records produced by `IngestorService::ingest_advisory()`
and extracts CVE identifiers, affected package counts, and severity breakdowns.

The `AdvisoryIngestResult` struct contains optional and nullable fields:
- `cves: Option<Vec<String>>` — list of CVE identifiers; may be `None` when the advisory has no CVE references
- `affected_packages: Option<Vec<AffectedPackage>>` — packages impacted; may be `None` for advisories without package-level detail
- `severity_counts: Option<HashMap<String, u32>>` — counts per severity level; may be `None` when severity metadata is absent

The extractor must handle all nullable fields gracefully without panicking.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `extract_vulnerability_summary()` method to AdvisoryService

## Files to Create
- `modules/fundamental/src/advisory/model/vulnerability_summary.rs` — VulnerabilitySummary output struct
- `tests/api/advisory_summary.rs` — integration tests for the extractor

## Implementation Notes
- The `AdvisoryIngestResult` is defined in `modules/ingestor/src/service/mod.rs` — its fields use `Option<T>` for all aggregate data
- Follow the existing service method pattern in `advisory.rs` — methods return `Result<T, AppError>`
- The output `VulnerabilitySummary` struct should have non-optional fields with sensible defaults: `cve_count: u32`, `cve_list: Vec<String>`, `affected_package_count: u32`, `severity_breakdown: HashMap<String, u32>`
- When `cves` is `None`, use an empty `Vec` and set `cve_count` to 0
- When `affected_packages` is `None`, set `affected_package_count` to 0
- When `severity_counts` is `None`, use an empty `HashMap`

## Acceptance Criteria
- [ ] `extract_vulnerability_summary()` produces a valid summary from a fully-populated AdvisoryIngestResult
- [ ] `extract_vulnerability_summary()` handles None values for cves, affected_packages, and severity_counts without panicking
- [ ] VulnerabilitySummary fields are always populated (non-optional) with sensible defaults for missing data
- [ ] cve_count matches the length of the cve_list

## Test Requirements
- [ ] Test extraction with fully-populated AdvisoryIngestResult (all fields Some)
- [ ] Test extraction with all-None fields (cves=None, affected_packages=None, severity_counts=None) — should return zeroed summary
- [ ] Test extraction with mixed Some/None fields — each None field defaults independently
- [ ] Test that cve_count is consistent with cve_list.len()

## Dependencies
- Depends on: None
