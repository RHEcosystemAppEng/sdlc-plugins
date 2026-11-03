# Task 1 — Add `ownerGroup` to the Service Catalog record schema and persistence helpers

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**Fix Versions**: (omitted — TC-9007 has no fixVersions)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so every record can carry the group that owns the service. This is the shared-artifact change for TC-9007. Registration (Task 2) writes the field, and the summary API (Task 3) and downloadable report (Task 4) read it. The store's update helper must keep the record's current `ownerGroup` when an update does not supply a new value (TC-9007 Requirement 3). Existing population behavior and stable record IDs must stay the same.

**Scope note:** The stakeholder limited TC-9007 to onboarding and display. Other writers also populate the shared Service Catalog record, and whether those writers are covered is an open scope question recorded in the TC-9007 impact map. This task therefore does not by itself satisfy the Feature-level criterion "every record has an `ownerGroup` after creation or update" for every population path.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema; accept and persist it in the create helper; keep the existing value in the update helper when the incoming value is absent
- `tests/catalog/test_store.py` — add persistence and update-semantics tests for `ownerGroup`

## Implementation Notes
- `src/catalog/store.py` holds the shared catalog record schema and persistence helpers. Add `ownerGroup` next to the existing record fields and follow the same pattern for declaring and serializing them. Do not change how record IDs are generated or assigned.
- Update semantics: when an update payload has no `ownerGroup`, or it is `None`, keep the stored value. When a non-empty value is supplied, replace it. Put this merge in the store update helper so later callers inherit it, instead of duplicating it in each caller.
- Records already stored without `ownerGroup` must still load: read a missing field as absent/`None` instead of raising, so the summary API and report keep working on existing data.
- Do not modify any workflow or API module other than the store in this task.
- Constraints (docs/constraints.md):
  - §1.4/§1.5/§1.6: keep changes scoped to this task, inspect the code before modifying it, and stop to ask if this description is incomplete.
  - §2.1–2.3: Conventional Commits, `Implements TC-<task-key>` footer, `--trailer="Assisted-by: Claude Code"`.
  - §3.1–3.3: branch named after the task's Jira key, PR link posted to Jira, `gh pr create --base main`.
  - §5.1–5.8: only the listed files, no duplicated logic, trace the data flow through create, update, and read, and check parity with sibling fields.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema field definitions and create/update persistence helpers. Extend them; do not add a parallel record type.

## Acceptance Criteria
- [ ] The Service Catalog record schema includes an `ownerGroup` field
- [ ] Creating a record with an `ownerGroup` persists it, and it reads back unchanged
- [ ] Updating a record without supplying `ownerGroup` keeps the existing value
- [ ] Updating a record with a new `ownerGroup` replaces the stored value
- [ ] Record IDs are unchanged by create and update operations that involve `ownerGroup`
- [ ] Stored records that predate the field still load without error

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it round-trips through persistence
- [ ] `tests/catalog/test_store.py`: update a record without `ownerGroup` and assert the previous value is kept
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert the new value is stored
- [ ] `tests/catalog/test_store.py`: assert the record ID stays the same across create and update
- [ ] `tests/catalog/test_store.py`: load a record stored without `ownerGroup` and assert it loads without error
- [ ] Existing tests in `tests/catalog/test_store.py` still pass

## Dependencies
- None
