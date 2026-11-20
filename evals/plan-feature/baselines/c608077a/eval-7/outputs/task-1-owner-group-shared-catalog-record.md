# Task 1 — Add ownerGroup to the shared Service Catalog record across all population paths and consumers

**Summary**: TC-9007: Add ownerGroup to the shared Service Catalog record across all population paths and consumers
**Issue type**: Task
**Parent (Epic)**: E1 — TC-9007: Service Catalog ownerGroup
**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**fixVersions**: omitted (TC-9007 has none)

---

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to Service Catalog records so users can see who owns each service (TC-9007). The Service Catalog record is a **shared artifact**. It is defined in `src/catalog/store.py` and written by four workflows: initial registration (onboarding), scheduled provider sync, fallback import, and on-demand refresh (`POST /api/catalog/refresh`). Two consumers read it: the summary API and the downloadable report.

The Feature's acceptance criteria apply to every record, whichever path populated it. Updating only the onboarding flow is therefore not enough. Records created or refreshed by sync, fallback import, or on-demand refresh would lack `ownerGroup`, or would lose an existing value. This task applies one `ownerGroup` contract in the shared store, connects it to every writer, and shows the field in both consumers. Existing population behavior and stable record IDs stay unchanged.

The stakeholder asked for a small plan. This stays a single task because the change is one additive field on one shared schema. Each writer needs only a small, uniform change.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the record schema. Add `UNASSIGNED_OWNER_GROUP` default. Add a shared resolution helper (supplied value > existing value > default on create). Add a fail-closed guard so no record is persisted without a non-empty `ownerGroup`.
- `src/workflows/registration.py` — accept `ownerGroup` during onboarding and persist it on the created record.
- `src/workflows/scheduled_sync.py` — route record writes through the store's `ownerGroup` resolution. New records get a value. Updates preserve the existing value unless a new one is supplied.
- `src/workflows/fallback_import.py` — route imported records through the same resolution. Legacy exports without `ownerGroup` get the default on create. Re-imports over existing records preserve the existing value.
- `src/api/on_demand_refresh.py` — accept an optional `ownerGroup` in the refresh request. Preserve the existing value when it is not supplied.
- `src/api/catalog_summary.py` — include `ownerGroup` in each summary record.
- `src/reports/catalog_export.py` — include an `ownerGroup` column/field in the downloadable report.
- `tests/catalog/test_store.py` — schema, resolution helper, and fail-closed guard tests.
- `tests/workflows/test_registration.py` — onboarding persists `ownerGroup`.
- `tests/workflows/test_scheduled_sync.py` — sync create/update `ownerGroup` behavior and stable IDs.
- `tests/workflows/test_fallback_import.py` — fallback import `ownerGroup` behavior (including legacy exports) and stable IDs.
- `tests/api/test_on_demand_refresh.py` — refresh `ownerGroup` preservation/override and stable IDs.
- `tests/api/test_catalog_summary.py` — summary shows `ownerGroup` for records from every population path.
- `tests/reports/test_catalog_export.py` — report shows `ownerGroup` for records from every population path.

## API Changes
- `GET` catalog summary API (served by `src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` string field. Additive change.
- `POST /api/catalog/refresh` — MODIFY: request accepts an optional `ownerGroup`. When omitted, the record's existing `ownerGroup` is preserved. Response, if it returns the record, includes `ownerGroup`.
- Downloadable catalog report (`src/reports/catalog_export.py`) — MODIFY: adds an `ownerGroup` column/field.

## Implementation Notes
- **One contract, enforced in the shared store.** Put the `ownerGroup` resolution in `src/catalog/store.py` next to the existing persistence helpers. Do not re-implement it in each workflow. Every writer must persist through that path:
  1. If the writer supplies a non-empty `ownerGroup`, use it.
  2. Else, if the record already exists with an `ownerGroup`, keep it (update preservation, Feature Requirement 3).
  3. Else (a new record with no supplied value), use `UNASSIGNED_OWNER_GROUP = "unassigned"`.
- **Default value is an assumption pending stakeholder confirmation.** The default was chosen because the Feature does not say what non-onboarding paths should use (see the impact map's Open question). Keep it as one named constant so a later change touches one place.
- **Cross-cutting call-site enumeration.** The repository inventory lists four writers to the shared record. All four are in scope, with one acceptance criterion each:
  - `src/workflows/registration.py` (primary onboarding)
  - `src/workflows/scheduled_sync.py` (scheduled/background)
  - `src/workflows/fallback_import.py` (fallback/recovery)
  - `src/api/on_demand_refresh.py` (on-demand/API)

  Before you start, search `src/` for any other caller of the store's write/persist helpers. If you find another writer, stop and flag it on TC-9007. Do not change files outside this list (constraint 5.1).
- **Fail-closed guard against silent empty values.** The Feature requires every record to have an `ownerGroup` after creation or update. The main failure mode is silent: a writer persists `None`/`""`, or an update overwrites a value with empty. That would make the summary and report show a blank and still pass. Add a guard in the store's persist helper that raises when the resolved `ownerGroup` is missing or empty. A test covers it (see Test Requirements).
- **Preserve existing behavior and stable IDs (AC3).** Do not change how IDs are derived or how existing fields are merged in any writer. The `ownerGroup` change must be additive to each writer's existing logic.
- **Fallback import.** Previously exported data predates this field. Missing `ownerGroup` in an import payload must not raise. It resolves via the rules above.
- **Consumers.** `src/api/catalog_summary.py` and `src/reports/catalog_export.py` should read `ownerGroup` straight from the stored record. Do not derive it per population path. That keeps the display independent of how the record was populated.
- **Verify the code before changing it.** The `catalog-service` structure in this task comes from the Feature's repository inventory, not from code analysis (no Serena instance; the repo is not in the Repository Registry). Inspect each file before modifying it (constraint 5.2), and use the store's existing helper names.
- Constraints that apply (from `docs/constraints.md`):
  - §1.4/§1.5: keep changes scoped to this task, and inspect code before modifying it.
  - §2.1–2.3: Conventional Commits, `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3.1–3.3: branch named after the task's Jira key, PR link posted to the Jira task, and `gh pr create --base main`.
  - §5.1–5.8: scope to the listed files, no duplicated logic (reuse the store helper), trace the data flow end to end (writer → store → summary/report), and parity across sibling writers (all four apply the same contract).
  - §5.9–5.13: prefer parameterized tests across the four writer paths when the project already uses them, add a doc comment on every new test, and add given-when-then comments on non-trivial tests.

## Reuse Candidates
- `src/catalog/store.py` — existing shared record schema and persistence helpers. Extend them with `ownerGroup` resolution so all four writers reuse one implementation.
- `tests/catalog/test_store.py` — existing persistence test fixtures. Reuse them to build records for the writer and consumer tests.

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`.
- [ ] Registration (`src/workflows/registration.py`): a newly registered record stores the `ownerGroup` collected during onboarding.
- [ ] Scheduled sync (`src/workflows/scheduled_sync.py`): records created by sync have a non-empty `ownerGroup`. Records updated by sync keep their existing `ownerGroup` unless sync supplies a new value.
- [ ] Fallback import (`src/workflows/fallback_import.py`): imported records have a non-empty `ownerGroup`, including legacy exports without the field. Importing over an existing record keeps its `ownerGroup` unless the import supplies a new value.
- [ ] On-demand refresh (`POST /api/catalog/refresh`, `src/api/on_demand_refresh.py`): refresh keeps the existing `ownerGroup` when none is supplied, and applies a supplied non-empty value.
- [ ] Summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for every record, whether it came from registration, sync, fallback import, or on-demand refresh.
- [ ] Downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for every record, whether it came from registration, sync, fallback import, or on-demand refresh.
- [ ] Fail-closed: the store refuses to persist a record whose resolved `ownerGroup` is missing or empty, so no writer can silently store a blank value.
- [ ] Stable IDs and existing population behavior are unchanged for all four writers.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: resolution helper tests. Supplied value wins. Existing value is kept on update when none is supplied. Default is applied only on create with no supplied value. An empty-string supplied value does not overwrite an existing value.
- [ ] `tests/catalog/test_store.py`: fail-closed test. Persisting a record whose resolved `ownerGroup` is missing or empty raises and stores nothing.
- [ ] `tests/workflows/test_registration.py`: registration with an `ownerGroup` persists it on the created record.
- [ ] `tests/workflows/test_scheduled_sync.py`: sync creates a new record with a non-empty `ownerGroup`. Sync updating a registered record keeps its `ownerGroup`. The record ID is unchanged after sync.
- [ ] `tests/workflows/test_fallback_import.py`: import of a legacy export without `ownerGroup` yields the default. Import over an existing record keeps its `ownerGroup`. Record IDs are unchanged.
- [ ] `tests/api/test_on_demand_refresh.py`: refresh without `ownerGroup` keeps the existing value. Refresh with a new `ownerGroup` updates it. The record ID is unchanged.
- [ ] `tests/api/test_catalog_summary.py`: with records populated through each of the four paths, the summary response includes the correct `ownerGroup` for every record.
- [ ] `tests/reports/test_catalog_export.py`: with records populated through each of the four paths, the report includes the correct `ownerGroup` for every record.
- [ ] Existing tests in all seven test files pass unchanged, except where a test asserts the exact record or response shape and must now include `ownerGroup`.

## Verification Commands
- `pytest tests/catalog tests/workflows tests/api tests/reports` — all tests pass.

## Dependencies
- None
