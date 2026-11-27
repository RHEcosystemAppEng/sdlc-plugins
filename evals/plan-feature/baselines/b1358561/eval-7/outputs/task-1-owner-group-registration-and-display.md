# Task 1: Add ownerGroup to Service Catalog records for registration, summary API, and report

**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**fixVersions**: (none; the Feature has none)
**Parent / Links**: TC-9007 incorporates this task

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service (TC-9007). This task covers the stakeholder-approved onboarding scope:
- the shared record schema and persistence helpers
- the initial registration workflow, which collects and stores `ownerGroup`
- the two read paths that present records: the summary API and the downloadable report

**Scope limitation (open scope conflict on TC-9007):** the Service Catalog has three more writers:
- `src/workflows/scheduled_sync.py`
- `src/workflows/fallback_import.py`
- `src/api/on_demand_refresh.py`

They are outside this task's scope until the stakeholder approves expanding it. This task alone does **not** satisfy the Feature criteria "every record has an `ownerGroup` after creation or update" and "displayed regardless of how the record was populated". Those criteria stay open on TC-9007 (see the impact map comment). Do not mark them as met in the PR.

## Files to Modify
- `src/catalog/store.py`: add `ownerGroup` to the shared catalog record schema. Persistence helpers must store and return it. On update, keep the existing `ownerGroup` when the incoming update does not supply one.
- `src/workflows/registration.py`: accept `ownerGroup` during initial registration and persist it on the new catalog record.
- `src/api/catalog_summary.py`: include `ownerGroup` in each record returned by the summary API.
- `src/reports/catalog_export.py`: include an `ownerGroup` column/field in the downloadable report.
- `tests/catalog/test_store.py`: persistence and preserve-on-update tests.
- `tests/workflows/test_registration.py`: registration tests for `ownerGroup`.
- `tests/api/test_catalog_summary.py`: summary API tests for `ownerGroup`.
- `tests/reports/test_catalog_export.py`: report export tests for `ownerGroup`.

## API Changes
- Catalog summary API: MODIFY. Each record in the response gains an `ownerGroup` field. This is additive; existing fields and record IDs are unchanged.
- Registration input: MODIFY. Registration accepts an `ownerGroup` value for the new record.

## Implementation Notes
- Define `ownerGroup` once, in the shared record schema in `src/catalog/store.py`. Registration, the summary API and the export must all use that definition, not their own copies of the field. This keeps one catalog contract for every writer and reader.
- Put the preserve-on-update rule in the `store.py` persistence helper (merge: incoming value if supplied, otherwise the stored value) rather than in a single workflow. That way any future in-scope writer gets the behavior. **Do not modify** `scheduled_sync.py`, `fallback_import.py` or `on_demand_refresh.py` in this task. Their coverage is an open scope question on TC-9007.
- Stable IDs: do not change how record IDs are generated or keyed in `store.py` or `registration.py`. Adding `ownerGroup` must not change identity or upsert matching.
- Existing records with no `ownerGroup`: the summary API and export must render a missing value deterministically (for example, an empty value or null) and must not raise an error. Do not backfill or invent values in this task.
- `catalog_summary.py` and `catalog_export.py` both read catalog records. Read `ownerGroup` from the record returned by the `store.py` helpers instead of re-deriving it.
- Constraints (docs/constraints.md):
  - §1.4 / §5.1: change only the files listed above.
  - §5.2: inspect each file before modifying it.
  - §5.4: reuse the existing store helpers; do not duplicate them.
  - §5.6: trace `ownerGroup` from registration input through store to the summary API and export.
  - §5.8: compare against sibling writers for parity and report any gaps instead of silently fixing them, since they are out of scope.
  - §5.11–5.13: add a doc comment to each new test and given/when/then comments to non-trivial tests.
  - §2.1–2.3: Conventional Commits, a Jira footer `Implements <task-key>`, and an `Assisted-by:` trailer.
  - §3.1–3.3: name the branch after the task key, open the PR with `--base main`, and post the PR link to Jira.

## Reuse Candidates
- `src/catalog/store.py`: existing shared schema and persistence helpers. Extend them; do not add a parallel record model.
- `tests/catalog/test_store.py`: existing persistence test patterns for the new field and merge tests.
- `tests/workflows/test_registration.py`, `tests/api/test_catalog_summary.py`, `tests/reports/test_catalog_export.py`: existing fixtures and patterns to extend.

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`, and the persistence helpers store and return it.
- [ ] Updating a record through the `store.py` helpers without an `ownerGroup` keeps the stored value. Supplying a new value replaces it.
- [ ] A service registered through `src/workflows/registration.py` is persisted with the supplied `ownerGroup`.
- [ ] The catalog summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for each record.
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for each record.
- [ ] Record IDs and existing registration, summary and export behavior are unchanged apart from the new field.
- [ ] Records with no stored `ownerGroup` render without errors in both the summary API and the report.
- [ ] The PR description states that the Feature criteria covering all population paths (sync, fallback import, on-demand refresh) are **not** addressed by this task and remain open on TC-9007.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: a record round-trips `ownerGroup` through persistence.
- [ ] `tests/catalog/test_store.py`: an update without `ownerGroup` keeps the stored value; an update with a new `ownerGroup` replaces it.
- [ ] `tests/catalog/test_store.py`: the stable ID is unchanged after an update that touches `ownerGroup`.
- [ ] `tests/workflows/test_registration.py`: registration persists the supplied `ownerGroup`, and existing registration assertions (including ID assignment) still pass.
- [ ] `tests/api/test_catalog_summary.py`: the summary response includes `ownerGroup` for a registered record, and a record with no `ownerGroup` renders without error.
- [ ] `tests/reports/test_catalog_export.py`: the exported report includes `ownerGroup` for a registered record, and a record with no `ownerGroup` exports without error.

## Documentation Updates
- Covered by Task 2 (catalog record contract documentation).

## Dependencies
- None
