<!-- SYNTHETIC TEST DATA — task description testing symbol deduplication behavior: constant already exists in sibling module -->

# Mock Jira Task

**Key**: TC-9210
**Summary**: Add severity-sorted remediation list to SBOM risk report
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity-sorted remediation list to the SBOM risk report endpoint. The list
should sort advisories by severity (Critical > High > Medium > Low > None) and return
them in descending severity order. The advisory module already defines a severity
ordering constant `SEVERITY_ORDER` in `modules/fundamental/src/advisory/service/advisory.rs`
that maps severity strings to numeric sort weights.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add severity-sorted remediation list builder to SbomService
- `modules/fundamental/src/sbom/endpoints/get.rs` — include remediation list in SBOM details response

## Files to Create
- `tests/api/sbom_remediation.rs` — integration tests for severity-sorted remediation list

## Implementation Notes
- The advisory module's `advisory.rs` service file defines `SEVERITY_ORDER: &[&str] = &["critical", "high", "medium", "low", "none"]` — reuse this constant for sorting instead of redefining it
- Follow the existing pattern in `sbom/service/sbom.rs` for fetching related advisories
- The remediation list maps each advisory to a `RemediationItem { advisory_id, severity, title, fix_version }` struct
- Sort using the `SEVERITY_ORDER` constant as the sort key — position in the array determines priority

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id} response includes a `remediations` field with severity-sorted list
- [ ] Advisories are sorted Critical > High > Medium > Low > None
- [ ] The severity ordering uses the existing `SEVERITY_ORDER` constant from the advisory module — no duplicate definition
- [ ] RemediationItem struct includes advisory_id, severity, title, and fix_version fields

## Test Requirements
- [ ] Test that remediation list is sorted by severity (Critical first, None last)
- [ ] Test that SBOM with no advisories returns empty remediation list
- [ ] Test that multiple advisories of the same severity maintain stable ordering

## Dependencies
- Depends on: None
