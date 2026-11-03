# Task 1 — Add ownerGroup to Service Catalog records across all population paths and readers

**Summary:** TC-9007: Add ownerGroup to Service Catalog records across all writers and readers
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — Feature has none)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service. The field is shown in the catalog summary API and the downloadable report.

Initial registration (onboarding) is the main place `ownerGroup` is collected. But the Service Catalog record is a shared artifact with four population paths:

- registration;
- scheduled synchronization;
- fallback import;
- on-demand refresh (`POST /api/catalog/refresh`).

The TC-9007 acceptance criteria apply to every record, "after creation or update" and "regardless of how that record was populated". So this task covers the shared schema, every writer and both readers. Each writer must create records with `ownerGroup` and keep the current value on update. Existing population behavior and stable IDs must stay unchanged.

The plan keeps this as one task to match the stakeholder's request for a small plan. Each per-path change is small and additive.

Reference: TC-9007.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the record schema. Reject a missing or empty `ownerGroup` on persist. Merge on update so the stored `ownerGroup` stays when the incoming value is absent.
- `src/workflows/registration.py` — collect `ownerGroup` during initial registration and persist it on the new record.
- `src/workflows/scheduled_sync.py` — keep the existing `ownerGroup` when synchronizing provider metadata. Set `ownerGroup` on records this path creates.
- `src/workflows/fallback_import.py` — carry `ownerGroup` from previously exported data when present, otherwise keep the stored value. Set `ownerGroup` on records this path creates.
- `src/api/on_demand_refresh.py` — keep `ownerGroup` on refresh unless the request supplies a new value.
- `src/api/catalog_summary.py` — include `ownerGroup` for each record in the summary response.
- `src/reports/catalog_export.py` — include `ownerGroup` in the downloadable report.
- `tests/catalog/test_store.py` — schema, validation and update-merge tests.
- `tests/workflows/test_registration.py` — registration tests for `ownerGroup`.
- `tests/workflows/test_scheduled_sync.py` — preservation, creation and stable-ID tests for sync.
- `tests/workflows/test_fallback_import.py` — carry-over, preservation, creation and stable-ID tests for fallback import.
- `tests/api/test_on_demand_refresh.py` — preservation, override and stable-ID tests for refresh.
- `tests/api/test_catalog_summary.py` — summary API display tests.
- `tests/reports/test_catalog_export.py` — report display tests.

## API Changes
- `GET` catalog summary API (`src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` field. This is additive.
- `POST /api/catalog/refresh` — MODIFY: the request may include an optional `ownerGroup`. If it is omitted, the stored `ownerGroup` stays unchanged.

## Implementation Notes
- **Single source of truth.** Put the `ownerGroup` rules in the shared persistence helpers in `src/catalog/store.py`:
  - validation: required and non-empty;
  - update merge: keep the stored value when the incoming value is absent or `None`.
  
  All four writers should go through these helpers. Do not re-implement the preserve logic in each workflow.
- **Writer enumeration.** All four writers below populate the same record. Each one needs its own change and test.
  1. `src/workflows/registration.py`
  2. `src/workflows/scheduled_sync.py`
  3. `src/workflows/fallback_import.py`
  4. `src/api/on_demand_refresh.py`
- **Reader enumeration.** Both readers need the field: `src/api/catalog_summary.py` and `src/reports/catalog_export.py`. Readers should take `ownerGroup` from the stored catalog record, not from the writer that populated it. That way the display does not depend on which path populated the record.
- **Fail-closed gate (fail-open risk).** A writer could persist an empty or `None` `ownerGroup` without any error. The record would look complete but show a blank owner. Put the guard in the `src/catalog/store.py` persist/save helper. It raises a validation error instead of storing a record without a non-empty `ownerGroup`. The update-merge step runs before validation, so updates that omit `ownerGroup` still pass when a stored value exists.
- **Preserve existing behavior.** Do not change:
  - the sync schedule;
  - provider field mapping, except to leave `ownerGroup` alone;
  - fallback trigger conditions;
  - refresh request handling for other fields;
  - stable ID generation or assignment on any path.
- **Open question: `ownerGroup` source for records not created by registration.** Records first created by scheduled sync, fallback import or refresh need some source for `ownerGroup`. Options are provider metadata, the exported data's field, the refresh request, or a documented placeholder such as `unassigned`. Confirm with the stakeholder before implementing. Apply one consistent rule across P2–P4.
- **Legacy records.** Records persisted before this change may have no `ownerGroup`. The ACs cover records after creation or update, so there is no backfill. Readers must handle a missing value without raising, for example by rendering it empty.
- **Repository analysis caveat.** No Serena instance or source access was available during planning. The paths above come from the TC-9007 repository structure. Inspect the existing helpers in `src/catalog/store.py` before you change anything (constraint 5.2).
- **Constraints (docs/constraints.md):**
  - §1.4: keep changes scoped to this task.
  - §2.1–2.3: Conventional Commits, `Implements <task-key>` footer, `Assisted-by: Claude Code` trailer.
  - §3.1–3.3: branch named after the task issue ID; post the PR link on the Jira task; `gh pr create --base main`.
  - §5.1–5.8: only the listed files; inspect before modifying; reuse the store helpers; trace the `ownerGroup` data flow from input → store → summary/report for every writer; parity across sibling writers.

## Reuse Candidates
- `src/catalog/store.py` (record schema and persistence helpers) — the shared write path every producer uses. Extend these helpers with `ownerGroup` validation and update-merge instead of adding per-workflow logic.
- `src/api/catalog_summary.py` / `src/reports/catalog_export.py` — both read records the same way. Reuse one field-serialization approach for both.

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`.
- [ ] Persisting a record with a missing or empty `ownerGroup` fails with a validation error rather than storing a blank owner (fail closed).
- [ ] Registration (`src/workflows/registration.py`) collects `ownerGroup` and the created record stores it.
- [ ] Scheduled synchronization (`src/workflows/scheduled_sync.py`) keeps an existing record's `ownerGroup`, and records it creates have a non-empty `ownerGroup`.
- [ ] Fallback import (`src/workflows/fallback_import.py`) carries over `ownerGroup` from exported data when present and otherwise keeps the stored value. Records it creates have a non-empty `ownerGroup`.
- [ ] On-demand refresh (`POST /api/catalog/refresh`, `src/api/on_demand_refresh.py`) keeps the current `ownerGroup` when the request does not supply one, and applies a supplied value.
- [ ] The catalog summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for records populated by each of the four paths.
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for records populated by each of the four paths.
- [ ] Existing population behavior and stable IDs are unchanged on registration, scheduled sync, fallback import and on-demand refresh.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: a record with `ownerGroup` round-trips through persistence.
- [ ] `tests/catalog/test_store.py`: persisting with a missing, `None` or empty `ownerGroup` raises a validation error (fail-closed path).
- [ ] `tests/catalog/test_store.py`: an update without `ownerGroup` keeps the stored value, and an update with a new value replaces it.
- [ ] `tests/workflows/test_registration.py`: registering a service stores the supplied `ownerGroup`, and the stable ID is assigned as before.
- [ ] `tests/workflows/test_scheduled_sync.py`: syncing an existing record keeps its `ownerGroup` and stable ID. A sync-created record has a non-empty `ownerGroup`. Other synced fields update as before.
- [ ] `tests/workflows/test_fallback_import.py`: importing exported data with `ownerGroup` stores it. Importing data without `ownerGroup` keeps the existing value. Stable IDs are unchanged.
- [ ] `tests/api/test_on_demand_refresh.py`: `POST /api/catalog/refresh` without `ownerGroup` keeps the stored value. With `ownerGroup`, it updates the value. The stable ID is unchanged.
- [ ] `tests/api/test_catalog_summary.py`: the summary response includes `ownerGroup` for records created via registration and records last written by sync, fallback import and refresh. A legacy record without `ownerGroup` does not error.
- [ ] `tests/reports/test_catalog_export.py`: the report includes `ownerGroup` for records from each population path. A legacy record without `ownerGroup` does not error.

## Dependencies
- None
