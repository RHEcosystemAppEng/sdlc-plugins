# Task 1 — Add `ownerGroup` to the shared Service Catalog record schema with preserve-on-update semantics

**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has no fixVersions)
**Parent / Epic:** TC-9007: Owner group capture (if Epic type available)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so that every record can carry the group that owns the service (TC-9007). The Service Catalog in `src/catalog/store.py` is the single shared source of service records read by the summary API and the downloadable report, so the field must be defined once here and reused by the onboarding writer (Task 2) and the display consumers (Tasks 3, 4).

The persistence helpers must also implement the Feature requirement that updates to a service record preserve the current `ownerGroup` unless a new value is supplied.

**Scope note (TC-9007 scope conflict):** per stakeholder instruction this task covers the shared schema and persistence helpers only. Other writers of the catalog record are excluded from this plan and are listed as unresolved paths in the TC-9007 impact map. This task does not by itself guarantee that "every Service Catalog record has an `ownerGroup` value after creation or update" — that criterion remains UNRESOLVED pending clarification.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the catalog record schema; make create/persist helpers accept it; make update helpers preserve the existing value when the update omits it (or supplies `None`/empty)
- `tests/catalog/test_store.py` — add persistence tests for `ownerGroup` creation, preservation on update, replacement on update, and unchanged stable IDs

## Implementation Notes
- Define `ownerGroup` alongside the existing record fields in the catalog record schema in `src/catalog/store.py`; follow the existing field declaration and serialization pattern used by the other record attributes in that module.
- Preserve-on-update: in the existing update/upsert helper(s) in `src/catalog/store.py`, merge the incoming update over the stored record so that an absent (or `None`) `ownerGroup` keeps the stored value, while a supplied non-empty value replaces it. Do not change how stable record IDs are computed or assigned.
- Reading pre-existing records that were persisted before this change must not fail: treat a missing `ownerGroup` as an explicit, documented sentinel (e.g., `None`) on read so consumers (Tasks 3, 4) can render it deterministically. Do not invent a placeholder owner.
- Keep the change additive — no renames or removals of existing fields — so existing catalog population behavior is unchanged (Feature AC: "Existing catalog population behavior and stable IDs remain unchanged").
- Do not modify any other writer module; those are explicitly out of scope for this plan (see TC-9007 impact map, "Unresolved impact-map paths").
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits; footer `Implements <task-key>`; `--trailer="Assisted-by: Claude Code"`.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post PR link on the Jira task.
  - §5 Code change rules: change only the files listed above (5.1); inspect `src/catalog/store.py` before modifying (5.2); reuse existing persistence helpers rather than adding parallel ones (5.4); trace the field through create → persist → read (5.6).
  - §1.4/1.5: keep changes scoped to this task; inspect code before modifying.

## Reuse Candidates
- `src/catalog/store.py` — existing record schema and persistence/update helpers; extend them instead of adding a new persistence path for `ownerGroup`
- `tests/catalog/test_store.py` — existing persistence test fixtures/patterns; extend for the new field

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes an `ownerGroup` field
- [ ] Creating a record through the store helpers with an `ownerGroup` persists and returns that value
- [ ] Updating a record without supplying `ownerGroup` preserves the previously stored `ownerGroup`
- [ ] Updating a record with a new `ownerGroup` value replaces the stored value
- [ ] Reading a record persisted before this change does not error and yields the documented missing-value sentinel
- [ ] Stable record IDs and existing fields are unchanged by the schema addition and by updates

## Test Requirements
- [ ] `tests/catalog/test_store.py`: create a record with `ownerGroup` and assert it round-trips through persistence
- [ ] `tests/catalog/test_store.py`: update a record without `ownerGroup` and assert the original value is preserved
- [ ] `tests/catalog/test_store.py`: update a record with a new `ownerGroup` and assert it is replaced
- [ ] `tests/catalog/test_store.py`: load a legacy record lacking `ownerGroup` and assert the read succeeds with the sentinel value
- [ ] `tests/catalog/test_store.py`: assert the stable ID of a record is identical before and after an update (regression for Feature AC on stable IDs)

## Verification Commands
- `pytest tests/catalog/test_store.py` — all tests pass

## Dependencies
- None
