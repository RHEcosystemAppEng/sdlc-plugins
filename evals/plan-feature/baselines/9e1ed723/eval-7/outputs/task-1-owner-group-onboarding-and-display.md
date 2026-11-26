# Task 1 — Add ownerGroup to Service Catalog records for onboarding, summary API, and report

**Summary:** TC-9007: Add ownerGroup to catalog schema, registration, summary API, and report
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9007)
**Fix Versions:** (omitted — TC-9007 has none)
**Parent:** Epic "TC-9007: Owner group on Service Catalog records" if a level-1 type is discovered; otherwise none (Feature "Incorporates" link)

## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record so users can see who owns each service (TC-9007). This task covers the shared schema/persistence layer, the initial onboarding (registration) writer, and both consumers (summary API and downloadable report).

**Scope limitation — read before implementing:** this task covers only the onboarding-focused scope requested by the stakeholder. TC-9007's acceptance criteria also apply to records created or updated by scheduled sync (`src/workflows/scheduled_sync.py`), fallback import (`src/workflows/fallback_import.py`), and on-demand refresh (`src/api/on_demand_refresh.py`). Those paths are an **unresolved scope conflict** recorded in the TC-9007 impact map and are pending a stakeholder decision. This task alone does **not** satisfy the criteria "every record has an `ownerGroup` after creation or update" or "displayed regardless of how the record was populated". Do not modify those writers in this task.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` to the shared catalog record schema; make the persistence/update helpers keep the stored `ownerGroup` when an update does not supply one
- `src/workflows/registration.py` — accept `ownerGroup` during initial registration and persist it on the created record
- `src/api/catalog_summary.py` — include `ownerGroup` in each record of the summary API response
- `src/reports/catalog_export.py` — include an `ownerGroup` column/field in the downloadable report
- `tests/catalog/test_store.py` — schema and preservation tests
- `tests/workflows/test_registration.py` — onboarding tests
- `tests/api/test_catalog_summary.py` — summary API display tests
- `tests/reports/test_catalog_export.py` — report display tests

## API Changes
- Catalog summary API — MODIFY: each record in the response gains an additive `ownerGroup` field (no existing fields removed or renamed)

## Implementation Notes
- Define `ownerGroup` once in the shared record schema in `src/catalog/store.py`; do not add per-consumer ad-hoc lookups. Both `src/api/catalog_summary.py` and `src/reports/catalog_export.py` already read records from the shared catalog, so they should read the new field from the record returned by the store.
- Put the "preserve unless a new value is supplied" rule in the store's update/persistence helper (`src/catalog/store.py`) rather than in `registration.py`, so the rule lives in one place. Note: this alone does not prove other writers preserve the value — whether `scheduled_sync.py`, `fallback_import.py`, and `on_demand_refresh.py` route through this helper (vs. replacing whole records) is part of the unresolved scope conflict and must not be assumed covered.
- Registration must require (or validate) an `ownerGroup` value at onboarding so newly created records always have one; reject registration with a missing/empty `ownerGroup` rather than silently storing an empty value.
- Consumers must render the field exactly as stored; define and test explicit behavior for legacy records that have no `ownerGroup` (e.g., render empty/`null` consistently rather than raising), since records populated by out-of-scope writers may lack the field until the scope conflict is resolved.
- Keep record IDs and existing registration behavior unchanged — `ownerGroup` is additive.
- Constraints (docs/constraints.md): §2.1–2.3 commits reference TC task key, use Conventional Commits, include `Assisted-by:` trailer; §3.1–3.3 branch named after the task key, PR uses `--base main`, PR link posted on the Jira task; §5.1 keep changes to the files listed above (do not touch the out-of-scope writers); §5.4 reuse existing store helpers; §5.6 trace the field through input (registration) → persistence (store) → output (summary API, report); §5.8 compare summary API and export for parity on how a missing `ownerGroup` is handled; §1.4 no unrelated refactoring.

## Reuse Candidates
- `src/catalog/store.py` — existing shared record schema and persistence helpers; extend these instead of adding a parallel owner-group store
- `src/api/catalog_summary.py` / `src/reports/catalog_export.py` — existing record-to-output mapping; extend the existing mapping with `ownerGroup` so both consumers stay in parity

## Acceptance Criteria
- [ ] The shared Service Catalog record schema in `src/catalog/store.py` includes `ownerGroup`
- [ ] A service registered via `src/workflows/registration.py` is persisted with the supplied `ownerGroup`
- [ ] Registration with a missing or empty `ownerGroup` is rejected (no record stored without an owner group via onboarding)
- [ ] The store update helper preserves the existing `ownerGroup` when an update does not supply one, and replaces it when a new value is supplied
- [ ] The summary API (`src/api/catalog_summary.py`) returns `ownerGroup` for each record
- [ ] The downloadable report (`src/reports/catalog_export.py`) includes `ownerGroup` for each record
- [ ] Record IDs and existing registration/population behavior are unchanged
- [ ] (Not covered by this task — pending scope decision) `ownerGroup` presence/preservation for records created or updated by scheduled sync, fallback import, and on-demand refresh

## Test Requirements
- [ ] `tests/catalog/test_store.py`: a record round-trips with `ownerGroup`; an update without `ownerGroup` preserves the stored value; an update with a new `ownerGroup` replaces it; record ID is unchanged across update
- [ ] `tests/workflows/test_registration.py`: registering a service stores the provided `ownerGroup`; registration without `ownerGroup` is rejected; existing registration assertions (IDs, other fields) still pass
- [ ] `tests/api/test_catalog_summary.py`: summary response includes `ownerGroup` for a registered record; legacy record without `ownerGroup` is handled per the defined behavior
- [ ] `tests/reports/test_catalog_export.py`: export includes `ownerGroup` for a registered record; legacy record without `ownerGroup` is handled per the same defined behavior as the summary API

## Documentation Updates
- Catalog record/API documentation in the repository — document the new `ownerGroup` field in the record schema and summary API response (detailed operator docs are handled by the documentation task)

## Dependencies
- None
