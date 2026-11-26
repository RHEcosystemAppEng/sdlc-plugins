<!-- SYNTHETIC TEST DATA — task where a validated value has no later generic merge path -->

# Mock Jira Task

**Key**: TC-9213
**Summary**: Add validated risk classification to the advisory summary builder
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `risk_classification` field to the advisory summary built by
`AdvisoryService::build_summary()`. Only `critical`, `high`, `medium` and `low` are
valid values; anything else must be rejected before the summary is returned.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add the validated
  `risk_classification` field to `build_summary()`
- `modules/fundamental/src/advisory/model/summary.rs` — add the `risk_classification`
  field to `AdvisorySummary`

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the summary builder

## API Changes
- (none)

## Implementation Notes
- `AdvisoryService::build_summary()` in `modules/fundamental/src/advisory/service/advisory.rs`
  populates the `AdvisorySummary` struct field by field and returns it; it performs no
  further merge, bulk update, or generic write after the struct is populated
- Validate `risk_classification` against the allowed set and return `AppError` with
  `.context()` on an invalid value, matching `common/src/error.rs`
- Response and model types follow the struct patterns in `modules/fundamental/src/advisory/model/`

## Acceptance Criteria
- [ ] `build_summary()` rejects a `risk_classification` outside the allowed set
- [ ] A summary built with a valid classification always carries that value

## Test Requirements
- [ ] Test that each allowed classification is accepted and lands in the summary
- [ ] Test that a disallowed classification is rejected

## Dependencies
- Depends on: None
