# Task 1 — Add ownerGroup to Service Catalog records across all population paths and displays

- **Issue type:** Task
- **Parent (Epic):** TC-9007: Service Catalog ownerGroup
- **Labels:** ai-generated-jira
- **Priority:** Major (inherited from TC-9007)
- **Fix Versions:** omitted (TC-9007 has none)
- **Links:** TC-9007 incorporates the parent Epic

---

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service (TC-9007). Every Service Catalog record must have an `ownerGroup` after it is created or updated. The summary API and the downloadable report must show `ownerGroup` no matter how the record was populated.

The onboarding (registration) flow is the main place where `ownerGroup` is collected. But four repository paths write the same shared record: registration, scheduled sync, fallback import, and on-demand refresh. The acceptance criteria apply to the shared artifact, so this task covers every writer and both consumers. Covering only registration would not meet TC-9007 AC1/AC2. A refresh, sync, or fallback import could drop the value, and the summary and report would then show it blank.

The scope was kept to a single task because all writers persist through one helper in `src/catalog/store.py`. The stakeholder may still limit this to onboarding only (see the TC-9007 impact map, "Scope conflict"). If so, the three non-onboarding writers and their tests must be removed from this task, and AC1/AC2 must be marked unresolved on the Feature.

## Files to Modify
- `src/catalog/store.py` — add the `ownerGroup` field to the catalog record schema. Add preserve-on-update merge logic to the persistence helpers. Refuse to persist a record whose resulting `ownerGroup` is missing or empty.
- `src/workflows/registration.py` — accept `ownerGroup` during initial registration and persist it on the new record.
- `src/workflows/scheduled_sync.py` — when updating records from provider metadata, keep the existing `ownerGroup`. Write a provider-supplied value only when it is non-empty.
- `src/workflows/fallback_import.py` — when loading previously exported service data, keep the existing `ownerGroup` for records that already exist. Import `ownerGroup` when the export contains one. Older exports without it must not clear the value.
- `src/api/on_demand_refresh.py` — `POST /api/catalog/refresh` keeps the current `ownerGroup` unless the request supplies a new non-empty value.
- `src/api/catalog_summary.py` — include `ownerGroup` in each summary record.
- `src/reports/catalog_export.py` — add an `ownerGroup` column/field to the downloadable report.
- `tests/catalog/test_store.py` — tests for the schema field, the preserve/override merge, and fail-closed persistence.
- `tests/workflows/test_registration.py` — test that a registered record carries `ownerGroup`.
- `tests/workflows/test_scheduled_sync.py` — tests that sync keeps or overrides `ownerGroup` correctly and does not change IDs.
- `tests/workflows/test_fallback_import.py` — tests for fallback import with and without `ownerGroup` in the export.
- `tests/api/test_on_demand_refresh.py` — tests for refresh with and without a new `ownerGroup`.
- `tests/api/test_catalog_summary.py` — test that the summary shows `ownerGroup` for records from each population path.
- `tests/reports/test_catalog_export.py` — test that the report shows `ownerGroup` for records from each population path.

## API Changes
- `GET` catalog summary endpoint (served by `src/api/catalog_summary.py`) — MODIFY: each record in the response gains an `ownerGroup` string field.
- `POST /api/catalog/refresh` — MODIFY: accepts an optional `ownerGroup` in the request. When it is absent, the current value is kept.
- Registration input (`src/workflows/registration.py`) — MODIFY: accepts `ownerGroup` for new services.

## Implementation Notes
- **Single merge point.** Put the preserve-unless-supplied logic in the shared persistence helper in `src/catalog/store.py`, not in each writer. The rule: the resulting `ownerGroup` is the supplied value when it is non-empty, otherwise the existing stored value. Then registration, scheduled sync, fallback import, and on-demand refresh all get the same update semantics, and none of them can silently overwrite with `None` or `""`.
- **Fail-closed gate.** The same helper in `src/catalog/store.py` must raise a validation error, not write, when the merged `ownerGroup` would be missing or empty. A writer that calls it must surface the error. Scheduled sync and fallback import must count or log the record as failed and must not report success with a blank owner. The main silent-success risk: a refresh or sync payload without `ownerGroup` ends with a "successful" write that blanks the owner, or with a new record that has none. Both violate AC1.
- **Writer enumeration (cross-cutting change).** The record contract change reaches every writer of the shared artifact. Each writer has its own acceptance criterion and test below:
  1. `src/workflows/registration.py` — creation (primary)
  2. `src/workflows/scheduled_sync.py` — scheduled/background update
  3. `src/workflows/fallback_import.py` — fallback/recovery create/replace
  4. `src/api/on_demand_refresh.py` — on-demand/API update
- **Consumers.** `src/api/catalog_summary.py` and `src/reports/catalog_export.py` read the shared record. Read `ownerGroup` from the stored record. Do not derive it from any writer-specific data, so the display does not depend on which path populated the record.
- **Stable IDs and existing behavior (AC3).** Do not change how record IDs are generated or matched in any writer. Do not change which fields the sync, import, and refresh paths already update. Only add `ownerGroup` handling.
- **Open question carried from the impact map.** A record first created by sync, import, or refresh without an `ownerGroup` is rejected by the fail-closed gate by default. If the stakeholder approves a default owner-group value instead, apply it only in the store helper.
- Constraints (docs/constraints.md):
  - §1.4 / §5.1: keep changes to the files listed above.
  - §5.2: inspect each file before modifying it.
  - §5.4: reuse the existing persistence helpers in `src/catalog/store.py`; do not duplicate the persistence logic in each writer.
  - §5.6: trace `ownerGroup` from input to store to summary/report for every population path.
  - §5.8: keep the four writers consistent in error handling and logging for the new field.
  - §2.1–2.3: Conventional Commits, Jira ID footer, `Assisted-by:` trailer.
  - §3.1–3.3: branch named after the task ID, PR link posted to Jira, `gh pr create --base main`.

## Reuse Candidates
- `src/catalog/store.py` (shared persistence helpers) — the single place to add the field, the merge, and validation. All four writers already persist through it.
- `tests/catalog/test_store.py` — existing persistence test fixtures to extend for the merge and fail-closed cases.
- Existing per-path test modules (`tests/workflows/test_*.py`, `tests/api/test_*.py`, `tests/reports/test_catalog_export.py`) — reuse their record fixtures. Do not create new fixture modules.

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`.
- [ ] Registration (`src/workflows/registration.py`) persists the supplied `ownerGroup` on newly created records.
- [ ] Scheduled sync (`src/workflows/scheduled_sync.py`) keeps the existing `ownerGroup` when provider data has none, and applies a provider-supplied non-empty value.
- [ ] Fallback import (`src/workflows/fallback_import.py`) keeps the existing `ownerGroup` when the export lacks it, and imports `ownerGroup` when the export contains it.
- [ ] On-demand refresh (`POST /api/catalog/refresh`, `src/api/on_demand_refresh.py`) keeps the current `ownerGroup` unless a new non-empty value is supplied, and then applies it.
- [ ] Fail-closed: the store refuses to persist any record whose resulting `ownerGroup` would be missing or empty. The calling writer reports a failure and never reports a successful write with a blank owner.
- [ ] The summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for records populated by registration, scheduled sync, fallback import, and on-demand refresh.
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for records populated by registration, scheduled sync, fallback import, and on-demand refresh.
- [ ] Record IDs and existing population behavior for all four writers are unchanged.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: updating a record without `ownerGroup` keeps the stored value. Updating with a new non-empty value replaces it.
- [ ] `tests/catalog/test_store.py` (fail-closed): persisting a record with no existing and no supplied `ownerGroup`, or with an empty string, raises a validation error and writes nothing.
- [ ] `tests/workflows/test_registration.py`: a registered service record contains the supplied `ownerGroup`.
- [ ] `tests/workflows/test_scheduled_sync.py`: a sync run with provider data that has no `ownerGroup` keeps the existing value. A run with a provider value updates it. Record IDs are unchanged after sync.
- [ ] `tests/workflows/test_scheduled_sync.py` (fail-closed): a sync that would create a record with no `ownerGroup` reports that record as failed and does not report success.
- [ ] `tests/workflows/test_fallback_import.py`: importing a legacy export without `ownerGroup` keeps existing values. Importing an export with `ownerGroup` sets it. Record IDs are unchanged.
- [ ] `tests/api/test_on_demand_refresh.py`: `POST /api/catalog/refresh` without `ownerGroup` keeps the current value. With a new value, it updates the value. A refresh that would leave the owner empty returns an error status, not success.
- [ ] `tests/api/test_catalog_summary.py`: the summary shows `ownerGroup` for records populated by each of the four paths.
- [ ] `tests/reports/test_catalog_export.py`: the report shows `ownerGroup` for records populated by each of the four paths.
- [ ] Existing tests in all seven test modules still pass unchanged (regression check for existing population behavior and stable IDs).

## Documentation Updates
- API documentation for the catalog summary and `POST /api/catalog/refresh` — note the new `ownerGroup` field and the preserve-unless-supplied semantics (full narrative docs are in Task 2).

## Dependencies
- None
