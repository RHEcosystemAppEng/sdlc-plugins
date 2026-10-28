## Repository
catalog-service

## Target Branch
main

## Description
Add an `ownerGroup` field to the shared Service Catalog record schema and propagate it through all four catalog population paths (registration, scheduled sync, fallback import, on-demand refresh) and both consumers (summary API, downloadable report). The field is collected during initial onboarding registration and preserved on subsequent updates unless a new value is explicitly supplied. Existing catalog population behavior and stable record IDs must remain unchanged.

The Service Catalog record is a shared artifact: four distinct workflows write it and two consumers read it. All writers must persist `ownerGroup` so that both consumers can display it regardless of which path populated the record.

## Files to Modify
- `src/catalog/store.py` — add `ownerGroup` field to the shared catalog record schema and persistence helpers
- `src/workflows/registration.py` — collect and persist `ownerGroup` during initial onboarding registration
- `src/workflows/scheduled_sync.py` — preserve existing `ownerGroup` unless a new value is supplied during scheduled sync
- `src/workflows/fallback_import.py` — persist `ownerGroup` from imported data during fallback import
- `src/api/on_demand_refresh.py` — preserve existing `ownerGroup` unless a new value is supplied during on-demand refresh
- `src/api/catalog_summary.py` — include `ownerGroup` in summary API responses
- `src/reports/catalog_export.py` — include `ownerGroup` in downloadable report output
- `tests/catalog/test_store.py` — add persistence tests for `ownerGroup` field
- `tests/workflows/test_registration.py` — add tests for `ownerGroup` collection during registration
- `tests/workflows/test_scheduled_sync.py` — add tests for `ownerGroup` preservation and update during scheduled sync
- `tests/workflows/test_fallback_import.py` — add tests for `ownerGroup` persistence from imported data
- `tests/api/test_on_demand_refresh.py` — add tests for `ownerGroup` preservation and update during on-demand refresh
- `tests/api/test_catalog_summary.py` — add tests for `ownerGroup` display in summary API responses
- `tests/reports/test_catalog_export.py` — add tests for `ownerGroup` display in downloadable report output

## API Changes
- `GET /api/catalog/summary` (or equivalent summary endpoint) — MODIFY: response includes `ownerGroup` field for each catalog record
- `POST /api/catalog/refresh` — MODIFY: accepts optional `ownerGroup` in request; preserves existing value when not supplied

## Implementation Notes
- Start with the schema change in `src/catalog/store.py`. All four writer paths and both consumer paths depend on this shared record schema. The `ownerGroup` field should be additive — existing records without it must remain valid (use a sensible default or allow null for backward compatibility).
- **Registration path** (`src/workflows/registration.py`): This is the primary onboarding path where `ownerGroup` is first collected. Persist `ownerGroup` as part of the initial catalog record creation via `store.py` helpers.
- **Scheduled sync path** (`src/workflows/scheduled_sync.py`): When synchronizing metadata from the provider, preserve the current `ownerGroup` value unless the provider supplies a new one. Do not overwrite an existing value with null or empty. Follow the same persistence helpers in `store.py`.
- **Fallback import path** (`src/workflows/fallback_import.py`): When loading previously exported service data, read the `ownerGroup` from the import payload and persist it. The exported data format must include the field. Follow the same persistence helpers in `store.py`.
- **On-demand refresh path** (`src/api/on_demand_refresh.py`): Same update-preservation semantics as scheduled sync — preserve the current `ownerGroup` unless the refresh request supplies a new value. Follow the same persistence helpers in `store.py`.
- **Summary API consumer** (`src/api/catalog_summary.py`): Read `ownerGroup` from the catalog record and include it in the API response. This is read-only — no write logic needed.
- **Report consumer** (`src/reports/catalog_export.py`): Read `ownerGroup` from the catalog record and include it in the report output. This is read-only — no write logic needed.
- Ensure stable record IDs are not altered by the schema change. The `ownerGroup` addition must not change ID generation or record identity semantics.
- Each writer path must be tested independently to verify correct `ownerGroup` handling, including the preserve-on-update semantics for the sync and refresh paths.
- Both consumers must be validated with records produced by each of the four writer paths to confirm `ownerGroup` displays correctly regardless of population origin.

## Reuse Candidates
- `src/catalog/store.py` — existing persistence helpers for creating and updating catalog records; extend these to handle `ownerGroup` rather than adding separate persistence logic

## Acceptance Criteria
- [ ] `src/catalog/store.py` schema includes `ownerGroup` field with persistence support
- [ ] `src/workflows/registration.py` collects and persists `ownerGroup` during initial registration
- [ ] `src/workflows/scheduled_sync.py` preserves existing `ownerGroup` unless a new value is supplied
- [ ] `src/workflows/fallback_import.py` persists `ownerGroup` from imported data
- [ ] `src/api/on_demand_refresh.py` preserves existing `ownerGroup` unless a new value is supplied
- [ ] `src/api/catalog_summary.py` includes `ownerGroup` in summary API responses
- [ ] `src/reports/catalog_export.py` includes `ownerGroup` in downloadable report output
- [ ] Summary API shows `ownerGroup` for records populated via registration
- [ ] Summary API shows `ownerGroup` for records populated via scheduled sync
- [ ] Summary API shows `ownerGroup` for records populated via fallback import
- [ ] Summary API shows `ownerGroup` for records populated via on-demand refresh
- [ ] Downloadable report shows `ownerGroup` for records populated via any of the four writer paths
- [ ] Existing catalog population behavior remains unchanged (no regressions in registration, sync, import, or refresh)
- [ ] Stable record IDs remain unchanged after adding `ownerGroup` to the schema
- [ ] Existing records without `ownerGroup` continue to function correctly

## Test Requirements
- [ ] `tests/catalog/test_store.py`: verify `ownerGroup` can be persisted and retrieved from the catalog store
- [ ] `tests/catalog/test_store.py`: verify existing records without `ownerGroup` remain valid (backward compatibility)
- [ ] `tests/catalog/test_store.py`: verify stable record IDs are unchanged after adding `ownerGroup`
- [ ] `tests/workflows/test_registration.py`: verify `ownerGroup` is collected and stored during initial registration
- [ ] `tests/workflows/test_registration.py`: verify registration without `ownerGroup` still succeeds (if field is optional)
- [ ] `tests/workflows/test_scheduled_sync.py`: verify existing `ownerGroup` is preserved when sync does not supply a new value
- [ ] `tests/workflows/test_scheduled_sync.py`: verify `ownerGroup` is updated when sync supplies a new value
- [ ] `tests/workflows/test_fallback_import.py`: verify `ownerGroup` is loaded from import data and persisted
- [ ] `tests/workflows/test_fallback_import.py`: verify import handles records without `ownerGroup` gracefully
- [ ] `tests/api/test_on_demand_refresh.py`: verify existing `ownerGroup` is preserved when refresh does not supply a new value
- [ ] `tests/api/test_on_demand_refresh.py`: verify `ownerGroup` is updated when refresh supplies a new value
- [ ] `tests/api/test_catalog_summary.py`: verify summary API response includes `ownerGroup` for a record created via registration
- [ ] `tests/api/test_catalog_summary.py`: verify summary API response includes `ownerGroup` for records created via each of the four writer paths
- [ ] `tests/reports/test_catalog_export.py`: verify report output includes `ownerGroup` for a record created via registration
- [ ] `tests/reports/test_catalog_export.py`: verify report output includes `ownerGroup` for records created via each of the four writer paths

## Documentation Updates
- Document the shared catalog record contract including the new `ownerGroup` field
- Document that catalog records may be populated through four paths: registration, scheduled sync, fallback import, on-demand refresh
- Document the update-preservation semantics for `ownerGroup` (preserved unless a new value is explicitly supplied)

## Dependencies
- None
