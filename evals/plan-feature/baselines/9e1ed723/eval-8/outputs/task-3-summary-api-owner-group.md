# Task 3 — Show ownerGroup in the catalog summary API

**Summary:** TC-9007: Expose ownerGroup in the catalog summary API
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (none; the Feature has no fixVersions)
**Epic group (by-sub-feature, pending approval):** Owner group display

## Repository
catalog-service

## Target Branch
main

## Description
Add `ownerGroup` to each record returned by the catalog summary API, read from the shared Service Catalog record. This covers part of the Feature requirement "The catalog summary API and downloadable report show `ownerGroup`".

Scope note: this task makes the summary API read and return the field. Records written by catalog paths outside the approved onboarding-and-display scope may not have `ownerGroup` populated. That gap is recorded as unresolved in the TC-9007 impact map, so this task alone does not satisfy the "regardless of how that record was populated" criterion.

## Files to Modify
- `src/api/catalog_summary.py` — include `ownerGroup` from the catalog record in the summary response

## API Changes
- Catalog summary API — MODIFY: each record in the response gains an `ownerGroup` field (string, or `null` when the stored record has none)

## Implementation Notes
- `src/api/catalog_summary.py` reads catalog records for the summary API. Read `ownerGroup` from the record returned by the shared store in `src/catalog/store.py`. Do not re-derive it or query a separate source.
- Make the change additive. Existing response fields and their order/shape stay the same.
- For records with no stored `ownerGroup` (legacy records), return an explicit `null` rather than omitting the key, so consumers see a consistent contract and missing data is visible instead of hidden.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR to `main` with `--base main`; §5.1 file scope; §5.4 reuse the store's record accessors; §5.8 keep parity with the report output in Task 4 (same field name `ownerGroup`, same null handling).

## Reuse Candidates
- `src/catalog/store.py` — shared record schema/accessors with `ownerGroup` (from Task 1)

## Acceptance Criteria
- [ ] The summary API response includes `ownerGroup` for each catalog record that has one stored
- [ ] Records without a stored `ownerGroup` return `ownerGroup: null` and the request does not fail
- [ ] All existing summary API fields are unchanged

## Test Requirements
- [ ] `tests/api/test_catalog_summary.py`: a record created via registration with an `ownerGroup` appears in the summary with that value
- [ ] `tests/api/test_catalog_summary.py`: a legacy record without `ownerGroup` returns `ownerGroup: null`
- [ ] `tests/api/test_catalog_summary.py`: regression check that existing response fields and record IDs are unchanged

## Documentation Updates
- Summary API reference documentation (location to be confirmed in the repository) — document the new `ownerGroup` response field

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record schema
