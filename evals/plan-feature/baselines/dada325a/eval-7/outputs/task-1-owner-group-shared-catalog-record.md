# Task 1 — Add ownerGroup to the shared Service Catalog record across all writers and readers

**Summary:** TC-9007: Add ownerGroup to Service Catalog records (store, all population paths, summary API, report)
**Labels:** ai-generated-jira
**Priority:** Major (inherited from Feature)
**Fix Versions:** (omitted — Feature has none)
**Epic:** TC-9007: Service Catalog ownerGroup

> Status: pending scope approval. See "Scope conflict" in impact-map.md. If the user
> chooses onboarding-only scope, remove `scheduled_sync.py`, `fallback_import.py`,
> `on_demand_refresh.py` and their tests from this task. Those paths then stay unresolved
> in the impact map, and AC1 and AC2 of the Feature are not claimed as satisfied.

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns
each service (TC-9007). Onboarding (registration) is where `ownerGroup` is first
collected. The record is shared, though, and is also written by scheduled provider sync,
fallback import and on-demand refresh (`POST /api/catalog/refresh`). Two readers present
it: the summary API and the downloadable report.

The Feature's acceptance criteria require that:
- every record has `ownerGroup` after creation **or update**
- both readers show it **regardless of how the record was populated**
- updates keep the current value unless a new one is supplied

So this task changes the schema, all four writers and both readers in one coherent
change. The writers keep the value through one shared merge rule in the store. Delivering
it as a single task matches the stakeholder's wish for a small plan and keeps `main`
consistent: the schema and validation never land ahead of the writers that must honor
them.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the record schema; add one merge helper (keep the existing value unless a new non-empty value is supplied); validate on write that the merged record has `ownerGroup` (fail closed)
- `src/workflows/registration.py` — accept and persist `ownerGroup` during initial onboarding
- `src/workflows/scheduled_sync.py` — route record updates through the store merge helper so a scheduled refresh keeps the existing `ownerGroup`
- `src/workflows/fallback_import.py` — map `ownerGroup` from exported data when present; otherwise keep the existing value through the merge helper
- `src/api/on_demand_refresh.py` — `POST /api/catalog/refresh`: keep the existing `ownerGroup` unless the request supplies a new value; use the merge helper
- `src/api/catalog_summary.py` — include `ownerGroup` in summary API record output
- `src/reports/catalog_export.py` — include `ownerGroup` in the downloadable report (this also makes it available to `fallback_import.py` on re-import)
- `tests/catalog/test_store.py` — schema, merge and validation tests
- `tests/workflows/test_registration.py` — onboarding persists `ownerGroup`
- `tests/workflows/test_scheduled_sync.py` — sync keeps `ownerGroup`; existing sync behavior and IDs unchanged
- `tests/workflows/test_fallback_import.py` — import carries or keeps `ownerGroup`; existing import behavior and IDs unchanged
- `tests/api/test_on_demand_refresh.py` — refresh keeps or overrides `ownerGroup`; existing refresh behavior and IDs unchanged
- `tests/api/test_catalog_summary.py` — summary shows `ownerGroup` for records from each population path
- `tests/reports/test_catalog_export.py` — report shows `ownerGroup` for records from each population path

## API Changes
- Catalog summary API (`src/api/catalog_summary.py`) — MODIFY: each record in the response includes `ownerGroup` (additive field)
- `POST /api/catalog/refresh` — MODIFY: optional `ownerGroup` in the request. If omitted, the stored value is kept; if supplied (non-empty), it replaces the stored value. The response record includes `ownerGroup`
- Registration input (`src/workflows/registration.py`) — MODIFY: accepts `ownerGroup` at onboarding

## Implementation Notes
- **Shared-artifact rule:** put the `ownerGroup` persistence logic in one place, the
  persistence helpers in `src/catalog/store.py`. Expose one merge function that all four
  writers call (for example, `merge_owner_group(existing, incoming)` or an equivalent
  option on the existing upsert/save helper). Do not write per-writer copies of the
  preserve logic. A writer that skips the helper is exactly the bug this task prevents.
- **Merge semantics:** `incoming.ownerGroup` non-empty → use it. Otherwise → keep
  `existing.ownerGroup`. Never overwrite a stored value with `None` or an empty string.
- **Fail-closed validation (fail-open risk):** a record silently stored without an
  `ownerGroup` would make the summary API and report "succeed" while showing nothing. The
  store write helper in `src/catalog/store.py` must raise or return an explicit error when
  the merged record has no `ownerGroup`. It must not persist an empty value.
  - This is the gate for registration, and for sync, import or refresh creating a record
    that does not exist yet.
  - The source of `ownerGroup` for records first created by non-registration paths is an
    open question in the impact map. Confirm it before finalizing the guard behavior for
    those paths: provider field, sentinel, or reject.
- **Stable IDs and population behavior (AC3):** do not change how any writer chooses or
  derives record IDs, matching keys, or which records it touches. The only behavior
  change is carrying or keeping `ownerGroup`.
- **Export/import round trip:** the field name and format that
  `src/reports/catalog_export.py` writes must be the same one
  `src/workflows/fallback_import.py` reads. Otherwise a fallback import after an export
  will blank owner groups. Exports created before this change have no `ownerGroup` field;
  import must treat that as "not supplied" and keep the stored value.
- **Readers:** `src/api/catalog_summary.py` and `src/reports/catalog_export.py` read the
  field from the shared record and must not re-derive it per population path.
- **Constraints (docs/constraints.md):**
  - §2 Commit rules: Conventional Commits; footer `Implements <task-key>`; `Assisted-by:` trailer.
  - §3 PR rules: branch named after the task issue ID; `gh pr create --base main`; post the PR link on the Jira task.
  - §5 Code change rules:
    - Change only the files listed above (5.1).
    - Inspect code before modifying it (5.2).
    - Reuse the store helpers instead of duplicating merge logic (5.4).
    - Trace `ownerGroup` through every input → store → output path before committing (5.6).
    - Check that all four writers handle it the same way (5.8).
- No Serena instance and no CONVENTIONS.md are available for catalog-service. Before
  editing, inspect the existing symbols in `src/catalog/store.py` (record schema,
  save/upsert helpers) and follow their existing patterns.

## Reuse Candidates
- `src/catalog/store.py` (existing persistence helpers) — the shared write path every writer already uses; extend it with the merge/validation rule instead of adding logic to each writer
- `tests/catalog/test_store.py` (existing persistence test fixtures) — reuse record fixtures and builders to construct "existing record with ownerGroup" setups for writer tests

## Acceptance Criteria
- [ ] The Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`
- [ ] Registration (`src/workflows/registration.py`) persists the supplied `ownerGroup` on initial onboarding
- [ ] Scheduled sync (`src/workflows/scheduled_sync.py`) keeps the existing `ownerGroup` when refreshing a record that has one
- [ ] Fallback import (`src/workflows/fallback_import.py`) uses `ownerGroup` from exported data when present, and otherwise keeps the existing value
- [ ] On-demand refresh (`POST /api/catalog/refresh`, `src/api/on_demand_refresh.py`) keeps the existing `ownerGroup` unless the request supplies a new non-empty value, in which case the new value is stored
- [ ] The store rejects (fails closed on) any write whose merged record would have no `ownerGroup`, instead of persisting an empty value
- [ ] The summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for records from registration, scheduled sync, fallback import and on-demand refresh
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for records from all four population paths
- [ ] Existing population behavior and stable record IDs are unchanged for all four writers

## Test Requirements
- [ ] `tests/catalog/test_store.py`: merge helper keeps the existing value when incoming is missing or empty, and overrides when incoming is non-empty
- [ ] `tests/catalog/test_store.py`: a write whose merged record has no `ownerGroup` is rejected and nothing is persisted (fail-closed path)
- [ ] `tests/workflows/test_registration.py`: onboarding with `ownerGroup` persists it; onboarding without it is rejected
- [ ] `tests/workflows/test_scheduled_sync.py`: sync of an existing record with `ownerGroup` leaves it unchanged; the record ID and other synced fields behave as before
- [ ] `tests/workflows/test_fallback_import.py`: import of export data containing `ownerGroup` restores it; import of a legacy export without `ownerGroup` keeps the stored value; IDs unchanged
- [ ] `tests/api/test_on_demand_refresh.py`: refresh without `ownerGroup` keeps it; refresh with a new `ownerGroup` updates it; IDs unchanged
- [ ] `tests/api/test_catalog_summary.py`: summary output includes `ownerGroup` for records populated through each of the four writers
- [ ] `tests/reports/test_catalog_export.py`: report output includes `ownerGroup` for records populated through each of the four writers, and export → fallback import round-trip keeps `ownerGroup`

## Dependencies
- None
