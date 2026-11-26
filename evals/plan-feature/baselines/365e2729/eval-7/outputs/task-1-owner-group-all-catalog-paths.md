# Task 1 — Add `ownerGroup` to Service Catalog records across all population paths and readers

**Summary:** TC-9007: Add ownerGroup to Service Catalog records (store, all writers, summary API, report)
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** omitted (TC-9007 has none)
**Status:** Draft, pending stakeholder confirmation that the scope covers all writers (see impact map, "Clarification requested")

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service, and show it in the catalog summary API and the downloadable report.

The Service Catalog is a shared artifact. Registration (onboarding) is not its only writer. Scheduled provider sync, fallback import and the on-demand refresh API all create or update the same records. The feature's acceptance criteria require `ownerGroup` to be present "after creation or update" and to be displayed "regardless of how that record was populated". So this task covers the shared store, all four writers and both readers. Changing only the onboarding flow would let sync, refresh or fallback import drop the field or never set it.

This is one task, as the stakeholder requested. Each per-path change is small: carry or preserve one field through the shared store helpers.

Feature: TC-9007.

## Files to Modify
- `src/catalog/store.py`: add `ownerGroup` to the shared catalog record schema. Persistence helpers must merge updates so an existing `ownerGroup` is kept when the incoming data does not supply one. Reject writes that would leave `ownerGroup` empty.
- `src/workflows/registration.py`: collect `ownerGroup` during initial registration and persist it on the new record.
- `src/workflows/scheduled_sync.py`: when a scheduled run updates a record, keep the existing `ownerGroup`, or apply a provider-supplied value if one exists. Never clear it.
- `src/workflows/fallback_import.py`: carry `ownerGroup` from previously exported data. If the export lacks it and a record already exists, keep the existing value. If neither is available, use the confirmed behavior (proposed: fail closed and report the record as an import error).
- `src/api/on_demand_refresh.py`: accept an optional `ownerGroup` in the `POST /api/catalog/refresh` payload. Keep the existing value when it is omitted.
- `src/api/catalog_summary.py`: include `ownerGroup` in each record of the summary response.
- `src/reports/catalog_export.py`: add an `ownerGroup` column/field to the downloadable report.
- `tests/catalog/test_store.py`: tests for the schema field, update-merge semantics and rejection of empty `ownerGroup`.
- `tests/workflows/test_registration.py`: tests for persisting `ownerGroup` at onboarding.
- `tests/workflows/test_scheduled_sync.py`: tests that sync preserves or updates `ownerGroup` and leaves IDs stable.
- `tests/workflows/test_fallback_import.py`: tests that fallback import carries or preserves `ownerGroup` and handles a missing value.
- `tests/api/test_on_demand_refresh.py`: tests for the refresh API with and without `ownerGroup`.
- `tests/api/test_catalog_summary.py`: tests that the summary API returns `ownerGroup`.
- `tests/reports/test_catalog_export.py`: tests that the report includes `ownerGroup`.

## API Changes
- `POST /api/catalog/refresh`: MODIFY. The request accepts an optional `ownerGroup` string. When omitted, the record's existing `ownerGroup` is preserved. The response and record shape gain `ownerGroup`. The change is additive and not breaking.
- Catalog summary API (served by `src/api/catalog_summary.py`): MODIFY. Each record in the response gains an `ownerGroup` field (additive).

## Implementation Notes
- **Single source of truth for the field contract:** define `ownerGroup` once in the record schema in `src/catalog/store.py`. Put the "preserve unless a new value is supplied" merge rule in the store's existing persistence/update helper, not in each writer. Each of W1–W4 then goes through the same helper, so the four writers cannot diverge. If a writer currently bypasses the helper and writes records directly, route it through the helper. Do not duplicate the merge logic.
- **Writer path map (all must be covered; the shared-artifact criteria are not met by the onboarding writer alone):**
  - W1 `src/workflows/registration.py`: primary create. Supplies `ownerGroup`.
  - W2 `src/workflows/scheduled_sync.py`: scheduled update. Make sure the provider-to-record mapping does not rebuild the record from provider fields only, which would drop `ownerGroup`.
  - W3 `src/workflows/fallback_import.py`: fallback/recovery. Older exports may lack `ownerGroup`. Handle that through the store merge plus the confirmed missing-value behavior.
  - W4 `src/api/on_demand_refresh.py`: on-demand operator API. Optional input, preserved when omitted.
- **Readers:** `src/api/catalog_summary.py` and `src/reports/catalog_export.py` read the stored field. Do not compute or default `ownerGroup` in the readers. They must show exactly what the store holds, so the display is the same for every population path.
- **Fail closed on a missing value (do not succeed silently):** the store must not persist a record whose `ownerGroup` is empty or missing after the merge. Raise a validation error from the store's write helper in `src/catalog/store.py`. W3 should catch it per record and report or log the record as failed, not save a blank value. Confirm the exact missing-value behavior with the stakeholder before merging (the alternative is a documented placeholder).
- **Stable IDs and existing behavior (AC3):** do not change how record IDs are derived or matched in any writer. Only add the field and the merge rule. Existing population behavior (which records are created, updated or skipped) must not change.
- Repository paths come from the feature's repository table. Inspect each file before changing it to confirm the exact helper and symbol names (no code intelligence was available during planning).
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits. The footer references the Jira task (for example `Implements TC-XXXX`). Include an `Assisted-by:` trailer.
  - §3 PR rules: branch named after the Jira task ID. Run `gh pr create --base main`. Post the PR link as a comment on the Jira task.
  - §5 Code change rules: change only the files listed above. Inspect before modifying. Reuse the store helpers instead of duplicating merge logic (§5.4). Trace the field through the full lifecycle, from every writer to the store to both readers (§5.6). Check parity across the four sibling writers (§5.8).
  - §1.4–1.6 implement-task scope: no unrelated refactoring. Ask for clarification if anything in this description is incomplete.

## Reuse Candidates
- `src/catalog/store.py` (existing record schema and persistence/update helpers): extend these for the `ownerGroup` field and the preserve-on-update merge, so all writers share one implementation.
- `tests/catalog/test_store.py` (existing persistence test fixtures): reuse them to build records with and without `ownerGroup` in the writer and reader tests.

## Acceptance Criteria
- [ ] The shared catalog record schema in `src/catalog/store.py` includes `ownerGroup`, and the store rejects (raises a validation error for) any write that would leave `ownerGroup` empty or missing.
- [ ] Registration (`src/workflows/registration.py`) persists the supplied `ownerGroup` on newly created records.
- [ ] Scheduled sync (`src/workflows/scheduled_sync.py`) keeps a record's existing `ownerGroup` when the provider does not supply one, and applies a supplied value when it does.
- [ ] Fallback import (`src/workflows/fallback_import.py`) carries `ownerGroup` from exported data, keeps the existing value when the export lacks it, and does not silently save a record without `ownerGroup` (it reports the record per the confirmed missing-value behavior).
- [ ] `POST /api/catalog/refresh` (`src/api/on_demand_refresh.py`) accepts an optional `ownerGroup`, applies it when supplied, and keeps the existing value when omitted.
- [ ] The summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for records populated through each of registration, scheduled sync, fallback import and on-demand refresh.
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for records populated through each of the four paths.
- [ ] Record IDs and existing create/update/skip behavior are unchanged on all four writer paths.

## Test Requirements
- [ ] `tests/catalog/test_store.py`: saving a record with `ownerGroup` round-trips it. An update without `ownerGroup` keeps the existing value. An update with a new value replaces it. A write that leaves `ownerGroup` empty raises a validation error (fail-closed).
- [ ] `tests/workflows/test_registration.py`: registering a service with `ownerGroup` stores it. The record ID is the same as before the change.
- [ ] `tests/workflows/test_scheduled_sync.py`: syncing an existing record whose provider data lacks `ownerGroup` keeps the stored value. Provider data with `ownerGroup` updates it. The record ID is unchanged after sync.
- [ ] `tests/workflows/test_fallback_import.py`: an import from an export containing `ownerGroup` stores it. An import over an existing record from an export without `ownerGroup` keeps the existing value. An import of a new record with no `ownerGroup` available does not create a blank record and is reported as failed. Record IDs are unchanged.
- [ ] `tests/api/test_on_demand_refresh.py`: a refresh with `ownerGroup` updates it. A refresh without `ownerGroup` keeps the existing value. The record ID is unchanged.
- [ ] `tests/api/test_catalog_summary.py`: the summary response includes `ownerGroup`, checked for records seeded through each population path (registration, sync, fallback import, refresh), parameterized if sibling tests use that pattern.
- [ ] `tests/reports/test_catalog_export.py`: the report includes the `ownerGroup` column/value for records seeded through each population path.

## Documentation Updates
- API documentation for `POST /api/catalog/refresh` and the catalog summary response (wherever the repository documents them): add the `ownerGroup` field and the preserve-when-omitted semantics. Broader operator documentation is handled in Task 2.

## Dependencies
- None
