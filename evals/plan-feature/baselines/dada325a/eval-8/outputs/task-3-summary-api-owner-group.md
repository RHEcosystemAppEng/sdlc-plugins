# Task 3 — Show ownerGroup in the catalog summary API

**Summary:** TC-9007: Expose `ownerGroup` in the catalog summary API
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Epic group (by-sub-feature, pending approval):** TC-9007: Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` to the catalog summary API output so users can see who owns each service (TC-9007 MVP requirement: "The catalog summary API ... show[s] `ownerGroup`"). The value is read from the shared Service Catalog record.

Note: the Feature criterion "display `ownerGroup` for a record regardless of how that record was populated" is **unresolved** in the TC-9007 impact map — this task renders whatever value the shared record holds, but does not guarantee records populated by scheduled sync, fallback import, or on-demand refresh carry a value (those paths are out of scope pending stakeholder clarification).

## Files to Modify
- `src/api/catalog_summary.py` — include the record's `ownerGroup` in the summary response
- `tests/api/test_catalog_summary.py` — add tests asserting `ownerGroup` appears in the response

## API Changes
- Catalog summary API — MODIFY: each record in the response includes an `ownerGroup` field (additive; existing fields unchanged)

## Implementation Notes
- `src/api/catalog_summary.py` already reads catalog records from `src/catalog/store.py`; add `ownerGroup` to the existing serialization of each record rather than issuing an additional lookup.
- Records persisted without `ownerGroup` must serialize to `null`/empty rather than raising.
- Additive response change only — do not rename or remove existing fields.
- Follow the existing test structure in `tests/api/test_catalog_summary.py`.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits, `Implements TC-<task-key>` footer, `Assisted-by:` trailer.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link to the Jira task.
  - §5 Code change rules: limit changes to Files to Modify; inspect before modifying; reuse existing record serialization (§5.4); compare parity with the report consumer in Task 4 (§5.8).
  - §1 Skill scope rules applicable to implement-task.

## Reuse Candidates
- `src/catalog/store.py` — shared record read helpers that now return `ownerGroup`

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each record that has one
- [ ] A record without `ownerGroup` is returned with an empty/null `ownerGroup` and no error
- [ ] Existing summary API fields are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: a record created with `ownerGroup` returns that value in the summary response
- [ ] `tests/api/test_catalog_summary.py`: a record without `ownerGroup` returns null/empty without error
- [ ] `tests/api/test_catalog_summary.py`: existing response fields are still present and unchanged

## Documentation Updates
- Summary API documentation — add the `ownerGroup` field to the response description

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
