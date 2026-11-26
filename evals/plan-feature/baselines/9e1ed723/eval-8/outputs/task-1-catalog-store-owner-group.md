# Task 1 — Add ownerGroup to the shared Service Catalog record schema

**Summary:** TC-9007: Add ownerGroup field to Service Catalog record schema and persistence
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (none; the Feature has no fixVersions)
**Epic group (by-sub-feature, pending approval):** Owner group capture

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so each service record can carry its owning group. This is the foundation for TC-9007: onboarding writes the field (Task 2), and the summary API (Task 3) and downloadable report (Task 4) read it. The persistence helpers must keep the current `ownerGroup` on update when the caller does not supply a new value, as the Feature requires.

Scope note: the stakeholder limited this Feature to onboarding and display. Other catalog population paths are listed as an unresolved scope conflict in the TC-9007 impact map and are not part of this task.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema and persistence helpers; add preserve-on-update semantics

## Implementation Notes
- `src/catalog/store.py` holds the shared catalog record schema and persistence helpers. Add `ownerGroup` there so every writer and reader uses the same contract instead of each module defining its own field.
- Make the field additive: existing persisted records without `ownerGroup` must still load (treat a missing value as absent/`None`) so current readers and writers keep working after this task merges on its own (direct-to-main).
- Update semantics: in the store's update/upsert helper, merge `ownerGroup` so an update with no `ownerGroup` (key absent or `None`) keeps the stored value, and an update with a new non-empty value replaces it. Do not change how the record identifier is assigned or looked up. Stable IDs must not change (Feature AC).
- Do not change existing population behavior of the store helpers beyond adding the field.
- Constraints (docs/constraints.md): §2 commits reference TC task ID, Conventional Commits, `Assisted-by:` trailer; §3 PR targets `main` with `--base main`, PR link posted to Jira; §5.1 only touch files listed here; §5.4 reuse existing store helpers rather than adding parallel persistence code; §5.6 trace the field through input → persistence → read.

## Reuse Candidates
- `src/catalog/store.py` — existing shared schema and persistence helpers. Extend them instead of adding a new persistence path.

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes an `ownerGroup` field
- [ ] Records persisted before this change (no `ownerGroup`) still load without error
- [ ] Updating a record without supplying `ownerGroup` keeps the stored `ownerGroup` value
- [ ] Updating a record with a new `ownerGroup` value replaces the stored value
- [ ] Record identifiers are unchanged by create and update operations

## Test Requirements
- [ ] `tests/catalog/test_store.py`: creating a record with `ownerGroup` persists it and reads it back
- [ ] `tests/catalog/test_store.py`: updating a record without `ownerGroup` keeps the existing value
- [ ] `tests/catalog/test_store.py`: updating a record with a new `ownerGroup` replaces the value
- [ ] `tests/catalog/test_store.py`: a legacy record with no `ownerGroup` loads successfully
- [ ] `tests/catalog/test_store.py`: regression check that the record ID is stable across create and update

## Dependencies
- None
